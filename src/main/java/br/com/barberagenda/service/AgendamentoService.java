package br.com.barberagenda.service;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.List;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import br.com.barberagenda.dto.AgendamentoRequest;
import br.com.barberagenda.exception.ConflitoException;
import br.com.barberagenda.exception.RecursoNaoEncontradoException;
import br.com.barberagenda.exception.RegraNegocioException;
import br.com.barberagenda.model.Agendamento;
import br.com.barberagenda.model.Barbeiro;
import br.com.barberagenda.model.Cliente;
import br.com.barberagenda.model.Servico;
import br.com.barberagenda.model.StatusAgendamento;
import br.com.barberagenda.repository.AgendamentoRepository;
import br.com.barberagenda.repository.BarbeiroRepository;
import br.com.barberagenda.repository.ClienteRepository;
import br.com.barberagenda.repository.ServicoRepository;

@Service
public class AgendamentoService {

    public static final int LIMITE_AGENDAMENTOS_ATIVOS = 3;

    private static final int TENTATIVAS_CODIGO_UNICO = 5;
    private static final String NAO_ENCONTRADO_PARA_CLIENTE =
            "Agendamento não encontrado para o código de acesso e o e-mail informados.";

    private final AgendamentoRepository agendamentoRepository;
    private final ClienteRepository clienteRepository;
    private final BarbeiroRepository barbeiroRepository;
    private final ServicoRepository servicoRepository;
    private final RegrasAgendamento regras;
    private final GeradorCodigoAcesso geradorCodigo;

    public AgendamentoService(AgendamentoRepository agendamentoRepository,
                              ClienteRepository clienteRepository,
                              BarbeiroRepository barbeiroRepository,
                              ServicoRepository servicoRepository,
                              RegrasAgendamento regras,
                              GeradorCodigoAcesso geradorCodigo) {
        this.agendamentoRepository = agendamentoRepository;
        this.clienteRepository = clienteRepository;
        this.barbeiroRepository = barbeiroRepository;
        this.servicoRepository = servicoRepository;
        this.regras = regras;
        this.geradorCodigo = geradorCodigo;
    }

    /**
     * Cria um agendamento. Ordem das verificações:
     * cliente/barbeiro/serviço existentes (404) → barbeiro e serviço ativos, RN-10 (400) →
     * RN-06, RN-04 e RN-05 (400) → limite de agendamentos ativos, RN-08 (409) →
     * sobreposição de horário do barbeiro, RN-07 (409).
     */
    @Transactional
    public Agendamento agendar(AgendamentoRequest pedido) {
        Cliente cliente = clienteRepository.findByEmailIgnoreCase(pedido.emailCliente())
                .orElseThrow(() -> new RecursoNaoEncontradoException(
                        "Cliente não encontrado para o e-mail informado. Faça o cadastro antes de agendar."));
        Barbeiro barbeiro = barbeiroRepository.buscarComBloqueio(pedido.barbeiroId())
                .orElseThrow(() -> new RecursoNaoEncontradoException("Barbeiro não encontrado."));
        Servico servico = servicoRepository.findById(pedido.servicoId())
                .orElseThrow(() -> new RecursoNaoEncontradoException("Serviço não encontrado."));

        validarAtivos(barbeiro, servico);

        LocalDateTime inicio = pedido.dataHoraInicio();
        regras.validarHorario(inicio, servico.getDuracaoMinutos());

        long ativos = agendamentoRepository.countByClienteIdAndStatus(cliente.getId(), StatusAgendamento.AGENDADO);
        if (ativos >= LIMITE_AGENDAMENTOS_ATIVOS) {
            throw new ConflitoException("O cliente já possui " + LIMITE_AGENDAMENTOS_ATIVOS
                    + " agendamentos ativos, que é o limite permitido.");
        }

        LocalDateTime fim = inicio.plusMinutes(servico.getDuracaoMinutos());
        if (agendamentoRepository.existeSobreposicao(barbeiro.getId(), inicio, fim)) {
            throw new ConflitoException("O barbeiro já possui agendamento nesse horário.");
        }

        Agendamento agendamento = new Agendamento(gerarCodigoUnico(), cliente, barbeiro, servico, inicio,
                StatusAgendamento.AGENDADO, regras.agora());
        return agendamentoRepository.save(agendamento);
    }

    /**
     * Consulta feita pelo cliente: exige o código de acesso recebido no agendamento e o e-mail do cliente.
     * Código inexistente ou e-mail divergente geram a mesma resposta (404), sem indicar qual dos dois falhou.
     */
    @Transactional(readOnly = true)
    public Agendamento consultarPeloCliente(String codigoAcesso, String email) {
        return agendamentoRepository.findByCodigoAcesso(GeradorCodigoAcesso.normalizar(codigoAcesso))
                .filter(a -> a.getCliente().getEmail().equalsIgnoreCase(email.strip()))
                .orElseThrow(() -> new RecursoNaoEncontradoException(NAO_ENCONTRADO_PARA_CLIENTE));
    }

    /** Cancelamento feito pelo cliente. Somente agendamentos com status AGENDADO podem ser cancelados. */
    @Transactional
    public Agendamento cancelarPeloCliente(String codigoAcesso, String email) {
        Agendamento agendamento = consultarPeloCliente(codigoAcesso, email);
        if (!agendamento.isAgendado()) {
            throw new ConflitoException("Somente agendamentos com status AGENDADO podem ser cancelados.");
        }
        agendamento.cancelar();
        return agendamento;
    }

    /** Marcação de atendimento concluído (administrador). */
    @Transactional
    public Agendamento concluir(Long id) {
        Agendamento agendamento = agendamentoRepository.findById(id)
                .orElseThrow(() -> new RecursoNaoEncontradoException("Agendamento não encontrado."));
        if (!agendamento.isAgendado()) {
            throw new ConflitoException("Somente agendamentos com status AGENDADO podem ser concluídos.");
        }
        agendamento.concluir();
        return agendamento;
    }

    /** Agenda do barbeiro no dia (todos os status), em ordem de horário. */
    @Transactional(readOnly = true)
    public List<Agendamento> agendaDoDia(Long barbeiroId, LocalDate data) {
        if (!barbeiroRepository.existsById(barbeiroId)) {
            throw new RecursoNaoEncontradoException("Barbeiro não encontrado.");
        }
        return agendamentoRepository.buscarDoBarbeiroNoPeriodo(barbeiroId, data.atStartOfDay(),
                data.plusDays(1).atStartOfDay());
    }

    /** Horários de início livres para o barbeiro e o serviço na data informada. */
    @Transactional(readOnly = true)
    public List<LocalDateTime> horariosDisponiveis(Long barbeiroId, Long servicoId, LocalDate data) {
        Barbeiro barbeiro = barbeiroRepository.findById(barbeiroId)
                .orElseThrow(() -> new RecursoNaoEncontradoException("Barbeiro não encontrado."));
        Servico servico = servicoRepository.findById(servicoId)
                .orElseThrow(() -> new RecursoNaoEncontradoException("Serviço não encontrado."));
        validarAtivos(barbeiro, servico);

        List<Agendamento> ocupados = agendamentoRepository
                .buscarDoBarbeiroNoPeriodo(barbeiroId, data.atStartOfDay(), data.plusDays(1).atStartOfDay())
                .stream()
                .filter(Agendamento::isAgendado)
                .toList();

        int duracao = servico.getDuracaoMinutos();
        return regras.gerarHorariosDoDia(data, duracao).stream()
                .filter(inicio -> ocupados.stream().noneMatch(a -> sobrepoe(a, inicio, inicio.plusMinutes(duracao))))
                .toList();
    }

    private String gerarCodigoUnico() {
        for (int tentativa = 0; tentativa < TENTATIVAS_CODIGO_UNICO; tentativa++) {
            String codigo = geradorCodigo.gerar();
            if (!agendamentoRepository.existsByCodigoAcesso(codigo)) {
                return codigo;
            }
        }
        throw new IllegalStateException("Não foi possível gerar um código de acesso único.");
    }

    /** RN-10: somente barbeiros e serviços ativos podem receber agendamentos. */
    private static void validarAtivos(Barbeiro barbeiro, Servico servico) {
        if (!barbeiro.isAtivo()) {
            throw new RegraNegocioException("barbeiroId", "O barbeiro selecionado está inativo.");
        }
        if (!servico.isAtivo()) {
            throw new RegraNegocioException("servicoId", "O serviço selecionado está inativo.");
        }
    }

    private static boolean sobrepoe(Agendamento existente, LocalDateTime inicio, LocalDateTime fim) {
        return existente.getDataHoraInicio().isBefore(fim) && existente.getDataHoraFim().isAfter(inicio);
    }
}
