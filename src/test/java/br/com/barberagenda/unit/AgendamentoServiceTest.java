package br.com.barberagenda.unit;

import static br.com.barberagenda.unit.DadosTeste.DF1;
import static br.com.barberagenda.unit.DadosTeste.DF3;
import static br.com.barberagenda.unit.DadosTeste.EMAIL;
import static br.com.barberagenda.unit.DadosTeste.RELOGIO;
import static br.com.barberagenda.unit.DadosTeste.agendamento;
import static br.com.barberagenda.unit.DadosTeste.barbeiro;
import static br.com.barberagenda.unit.DadosTeste.cliente;
import static br.com.barberagenda.unit.DadosTeste.pedido;
import static br.com.barberagenda.unit.DadosTeste.servico;
import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyLong;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import br.com.barberagenda.exception.ConflitoException;
import br.com.barberagenda.exception.RecursoNaoEncontradoException;
import br.com.barberagenda.exception.RegraNegocioException;
import br.com.barberagenda.model.Agendamento;
import br.com.barberagenda.model.StatusAgendamento;
import br.com.barberagenda.repository.AgendamentoRepository;
import br.com.barberagenda.repository.BarbeiroRepository;
import br.com.barberagenda.repository.ClienteRepository;
import br.com.barberagenda.repository.ServicoRepository;
import br.com.barberagenda.service.AgendamentoService;
import br.com.barberagenda.service.GeradorCodigoAcesso;
import br.com.barberagenda.service.RegrasAgendamento;

@ExtendWith(MockitoExtension.class)
@DisplayName("AgendamentoService — criação, conflitos, consulta e mudança de status")
class AgendamentoServiceTest {

    private static final LocalDateTime INICIO_VALIDO = DF3.atTime(10, 0);

    @Mock
    private AgendamentoRepository agendamentoRepository;
    @Mock
    private ClienteRepository clienteRepository;
    @Mock
    private BarbeiroRepository barbeiroRepository;
    @Mock
    private ServicoRepository servicoRepository;
    @Mock
    private GeradorCodigoAcesso geradorCodigo;

    private AgendamentoService service;

    @BeforeEach
    void criarServico() {
        service = new AgendamentoService(agendamentoRepository, clienteRepository, barbeiroRepository,
                servicoRepository, new RegrasAgendamento(RELOGIO), geradorCodigo);
    }

    /** Cliente, barbeiro e serviço existentes; barbeiro e serviço com a situação informada. */
    private void prepararCadastros(boolean barbeiroAtivo, boolean servicoAtivo) {
        when(clienteRepository.findByEmailIgnoreCase(EMAIL)).thenReturn(Optional.of(cliente()));
        when(barbeiroRepository.buscarComBloqueio(1L)).thenReturn(Optional.of(barbeiro(barbeiroAtivo)));
        when(servicoRepository.findById(2L)).thenReturn(Optional.of(servico(30, servicoAtivo)));
    }

    @Test
    @DisplayName("CT-019 / RF-04 — recusa agendamento sobreposto a outro do mesmo barbeiro")
    void deveRejeitarAgendamentoQuandoHorarioConflitaComOutroDoMesmoBarbeiro() {
        prepararCadastros(true, true);
        when(agendamentoRepository.countByClienteIdAndStatus(any(), eq(StatusAgendamento.AGENDADO))).thenReturn(0L);
        when(agendamentoRepository.existeSobreposicao(any(), eq(INICIO_VALIDO), eq(INICIO_VALIDO.plusMinutes(30))))
                .thenReturn(true);

        assertThatThrownBy(() -> service.agendar(pedido(INICIO_VALIDO)))
                .isInstanceOf(ConflitoException.class)
                .hasMessage("O barbeiro já possui agendamento nesse horário.");
        verify(agendamentoRepository, never()).save(any());
    }

    @Test
    @DisplayName("CT-021 / RF-04 — recusa o 4º agendamento quando o cliente já tem 3 ativos")
    void deveRejeitarQuartoAgendamentoAtivoDoCliente() {
        prepararCadastros(true, true);
        when(agendamentoRepository.countByClienteIdAndStatus(any(), eq(StatusAgendamento.AGENDADO))).thenReturn(3L);

        assertThatThrownBy(() -> service.agendar(pedido(INICIO_VALIDO)))
                .isInstanceOf(ConflitoException.class)
                .hasMessage("O cliente já possui 3 agendamentos ativos, que é o limite permitido.");
        verify(agendamentoRepository, never()).save(any());
    }

    @Test
    @DisplayName("CT-021 / RF-04 — aceita o 3º agendamento ativo e grava status, término e código de acesso")
    void deveAceitarTerceiroAgendamentoAtivoDoCliente() {
        prepararCadastros(true, true);
        when(agendamentoRepository.countByClienteIdAndStatus(any(), eq(StatusAgendamento.AGENDADO))).thenReturn(2L);
        when(agendamentoRepository.existeSobreposicao(any(), any(), any())).thenReturn(false);
        when(geradorCodigo.gerar()).thenReturn("K7Q2M9XD");
        when(agendamentoRepository.save(any(Agendamento.class))).thenAnswer(invocacao -> invocacao.getArgument(0));

        Agendamento criado = service.agendar(pedido(INICIO_VALIDO));

        assertThat(criado.getStatus()).isEqualTo(StatusAgendamento.AGENDADO);
        assertThat(criado.getDataHoraFim()).isEqualTo(INICIO_VALIDO.plusMinutes(30));
        assertThat(criado.getCodigoAcesso()).isEqualTo("K7Q2M9XD");
    }

    @Test
    @DisplayName("CT-017 / RF-03 — recusa agendamento com barbeiro inativo")
    void deveRejeitarAgendamentoComBarbeiroInativo() {
        prepararCadastros(false, true);

        assertThatThrownBy(() -> service.agendar(pedido(INICIO_VALIDO)))
                .isInstanceOf(RegraNegocioException.class)
                .hasMessage("O barbeiro selecionado está inativo.");
        verify(agendamentoRepository, never()).save(any());
    }

    @Test
    @DisplayName("CT-017 / RF-03 — recusa agendamento com serviço inativo")
    void deveRejeitarAgendamentoComServicoInativo() {
        prepararCadastros(true, false);

        assertThatThrownBy(() -> service.agendar(pedido(INICIO_VALIDO)))
                .isInstanceOf(RegraNegocioException.class)
                .hasMessage("O serviço selecionado está inativo.");
        verify(agendamentoRepository, never()).save(any());
    }

    @Test
    @DisplayName("CT-018 / RF-03 — recusa agendamento de e-mail não cadastrado")
    void deveRejeitarAgendamentoDeClienteNaoCadastrado() {
        when(clienteRepository.findByEmailIgnoreCase(EMAIL)).thenReturn(Optional.empty());

        assertThatThrownBy(() -> service.agendar(pedido(INICIO_VALIDO)))
                .isInstanceOf(RecursoNaoEncontradoException.class)
                .hasMessage("Cliente não encontrado para o e-mail informado. Faça o cadastro antes de agendar.");
    }

    @Test
    @DisplayName("CT-008 / RF-02 — não oferece horários que se sobrepõem a agendamento do barbeiro (14:00–15:00)")
    void naoDeveOferecerHorariosOcupadosPeloBarbeiro() {
        when(barbeiroRepository.findById(1L)).thenReturn(Optional.of(barbeiro(true)));
        when(servicoRepository.findById(2L)).thenReturn(Optional.of(servico(30, true)));
        when(agendamentoRepository.buscarDoBarbeiroNoPeriodo(anyLong(), any(), any()))
                .thenReturn(List.of(agendamento(DF1.atTime(14, 0), 60, StatusAgendamento.AGENDADO)));

        List<LocalDateTime> horarios = service.horariosDisponiveis(1L, 2L, DF1);

        assertThat(horarios).doesNotContain(DF1.atTime(14, 0), DF1.atTime(14, 30));
        assertThat(horarios).contains(DF1.atTime(13, 30), DF1.atTime(15, 0));
        assertThat(horarios).hasSize(18);
    }

    @Test
    @DisplayName("CT-025 / RF-05 — agendamento cancelado não ocupa o horário")
    void deveOferecerHorarioDeAgendamentoCancelado() {
        when(barbeiroRepository.findById(1L)).thenReturn(Optional.of(barbeiro(true)));
        when(servicoRepository.findById(2L)).thenReturn(Optional.of(servico(30, true)));
        when(agendamentoRepository.buscarDoBarbeiroNoPeriodo(anyLong(), any(), any()))
                .thenReturn(List.of(agendamento(DF1.atTime(16, 0), 30, StatusAgendamento.CANCELADO)));

        assertThat(service.horariosDisponiveis(1L, 2L, DF1)).contains(DF1.atTime(16, 0)).hasSize(20);
    }

    @Test
    @DisplayName("CT-025 / RF-05 — cliente cancela agendamento ativo informando código e e-mail")
    void deveCancelarAgendamentoAtivoDoCliente() {
        Agendamento ativo = agendamento(DF1.atTime(16, 0), 30, StatusAgendamento.AGENDADO);
        when(agendamentoRepository.findByCodigoAcesso("TESTE234")).thenReturn(Optional.of(ativo));

        Agendamento cancelado = service.cancelarPeloCliente("teste234", "ANA.ROCHA@EXEMPLO.COM");

        assertThat(cancelado.getStatus()).isEqualTo(StatusAgendamento.CANCELADO);
    }

    @Test
    @DisplayName("CT-024 / RF-05 — consulta com e-mail de outra pessoa é recusada como não encontrada")
    void deveRecusarConsultaComEmailDeOutroCliente() {
        Agendamento ativo = agendamento(DF1.atTime(16, 0), 30, StatusAgendamento.AGENDADO);
        when(agendamentoRepository.findByCodigoAcesso("TESTE234")).thenReturn(Optional.of(ativo));

        assertThatThrownBy(() -> service.consultarPeloCliente("TESTE234", "bruno.lima@exemplo.com"))
                .isInstanceOf(RecursoNaoEncontradoException.class)
                .hasMessage("Agendamento não encontrado para o código de acesso e o e-mail informados.");
    }

    @Test
    @DisplayName("CT-026 / RF-05 — recusa cancelar agendamento que já está cancelado")
    void deveRejeitarCancelamentoDeAgendamentoJaCancelado() {
        Agendamento cancelado = agendamento(DF1.atTime(16, 0), 30, StatusAgendamento.CANCELADO);
        when(agendamentoRepository.findByCodigoAcesso("TESTE234")).thenReturn(Optional.of(cancelado));

        assertThatThrownBy(() -> service.cancelarPeloCliente("TESTE234", EMAIL))
                .isInstanceOf(ConflitoException.class)
                .hasMessage("Somente agendamentos com status AGENDADO podem ser cancelados.");
    }

    // ---------------------------------------------------------------- TDD: RF-09 (antecedência mínima para cancelar)

    private static final String MSG_PRAZO_CANCELAMENTO =
            "O cancelamento só pode ser feito com no mínimo 2 horas de antecedência.";

    @org.junit.jupiter.params.ParameterizedTest(name = "início às {0} (agora = 10:00)")
    @org.junit.jupiter.params.provider.ValueSource(strings = {"11:59", "11:30", "10:30"})
    @DisplayName("RF-09 (TDD) / CT-036 — recusa cancelamento com menos de 2 horas de antecedência")
    void deveRejeitarCancelamentoComMenosDeDuasHorasDeAntecedencia(String horario) {
        Agendamento proximo = agendamento(DadosTeste.HOJE.atTime(java.time.LocalTime.parse(horario)), 30,
                StatusAgendamento.AGENDADO);
        when(agendamentoRepository.findByCodigoAcesso("TESTE234")).thenReturn(Optional.of(proximo));

        assertThatThrownBy(() -> service.cancelarPeloCliente("TESTE234", EMAIL))
                .hasMessage(MSG_PRAZO_CANCELAMENTO);
        assertThat(proximo.getStatus()).isEqualTo(StatusAgendamento.AGENDADO);
    }

    @Test
    @DisplayName("RF-09 (TDD) / CT-036 — aceita cancelamento com exatamente 2 horas de antecedência")
    void deveAceitarCancelamentoComExatamenteDuasHorasDeAntecedencia() {
        Agendamento limite = agendamento(DadosTeste.HOJE.atTime(12, 0), 30, StatusAgendamento.AGENDADO);
        when(agendamentoRepository.findByCodigoAcesso("TESTE234")).thenReturn(Optional.of(limite));

        assertThat(service.cancelarPeloCliente("TESTE234", EMAIL).getStatus()).isEqualTo(StatusAgendamento.CANCELADO);
    }

    @Test
    @DisplayName("CT-035 / RF-08 — recusa concluir agendamento cancelado")
    void deveRejeitarConclusaoDeAgendamentoCancelado() {
        Agendamento cancelado = agendamento(DF1.atTime(9, 30), 30, StatusAgendamento.CANCELADO);
        when(agendamentoRepository.findById(10L)).thenReturn(Optional.of(cancelado));

        assertThatThrownBy(() -> service.concluir(10L))
                .isInstanceOf(ConflitoException.class)
                .hasMessage("Somente agendamentos com status AGENDADO podem ser concluídos.");
        assertThat(cancelado.getStatus()).isEqualTo(StatusAgendamento.CANCELADO);
    }

    @Test
    @DisplayName("CT-034 / RF-08 — conclui agendamento ativo")
    void deveConcluirAgendamentoAtivo() {
        Agendamento ativo = agendamento(DF1.atTime(14, 0), 60, StatusAgendamento.AGENDADO);
        when(agendamentoRepository.findById(10L)).thenReturn(Optional.of(ativo));

        assertThat(service.concluir(10L).getStatus()).isEqualTo(StatusAgendamento.CONCLUIDO);
    }
}
