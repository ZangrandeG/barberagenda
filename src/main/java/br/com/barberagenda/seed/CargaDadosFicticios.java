package br.com.barberagenda.seed;

import java.math.BigDecimal;
import java.time.Clock;
import java.time.DayOfWeek;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.List;

import org.springframework.context.annotation.Profile;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

import br.com.barberagenda.model.Agendamento;
import br.com.barberagenda.model.Barbeiro;
import br.com.barberagenda.model.Cliente;
import br.com.barberagenda.model.Servico;
import br.com.barberagenda.model.StatusAgendamento;
import br.com.barberagenda.repository.AgendamentoRepository;
import br.com.barberagenda.repository.BarbeiroRepository;
import br.com.barberagenda.repository.ClienteRepository;
import br.com.barberagenda.repository.ServicoRepository;

/**
 * Massa de dados FICTÍCIA para desenvolvimento e testes (perfis dev e test).
 * Nomes, telefones e e-mails (@exemplo.com) são inventados.
 * As datas dos agendamentos são relativas ao dia atual, para que a massa continue válida em qualquer data.
 */
@Component
@Profile({"dev", "test"})
public class CargaDadosFicticios {

    private final BarbeiroRepository barbeiroRepository;
    private final ServicoRepository servicoRepository;
    private final ClienteRepository clienteRepository;
    private final AgendamentoRepository agendamentoRepository;
    private final Clock relogio;

    public CargaDadosFicticios(BarbeiroRepository barbeiroRepository, ServicoRepository servicoRepository,
                               ClienteRepository clienteRepository, AgendamentoRepository agendamentoRepository,
                               Clock relogio) {
        this.barbeiroRepository = barbeiroRepository;
        this.servicoRepository = servicoRepository;
        this.clienteRepository = clienteRepository;
        this.agendamentoRepository = agendamentoRepository;
        this.relogio = relogio;
    }

    /** Apaga barbeiros, serviços, clientes e agendamentos e carrega a massa inicial novamente. */
    @Transactional
    public ResumoCarga recarregar() {
        agendamentoRepository.deleteAllInBatch();
        clienteRepository.deleteAllInBatch();
        servicoRepository.deleteAllInBatch();
        barbeiroRepository.deleteAllInBatch();
        return carregar();
    }

    @Transactional
    public ResumoCarga carregar() {
        LocalDateTime agora = LocalDateTime.now(relogio);

        Barbeiro carlos = new Barbeiro("Carlos Navalha", true);
        Barbeiro rafael = new Barbeiro("Rafael Tesoura", true);
        Barbeiro diego = new Barbeiro("Diego Máquina", false);
        barbeiroRepository.saveAll(List.of(carlos, rafael, diego));

        Servico corte = new Servico("Corte de cabelo", 30, new BigDecimal("45.00"), true);
        Servico barba = new Servico("Barba", 30, new BigDecimal("30.00"), true);
        Servico corteBarba = new Servico("Corte e barba", 60, new BigDecimal("70.00"), true);
        Servico sobrancelha = new Servico("Sobrancelha", 15, new BigDecimal("15.00"), true);
        Servico relaxamento = new Servico("Relaxamento capilar", 90, new BigDecimal("80.00"), false);
        servicoRepository.saveAll(List.of(corte, barba, corteBarba, sobrancelha, relaxamento));

        List<Cliente> clientes = List.of(
                new Cliente("Ana Beatriz Rocha", "14991110001", "ana.rocha@exemplo.com", agora),
                new Cliente("Bruno Henrique Lima", "14991110002", "bruno.lima@exemplo.com", agora),
                new Cliente("Camila Souza Prado", "1432220003", "camila.prado@exemplo.com", agora),
                new Cliente("Daniel Ferreira Alves", "14991110004", "daniel.alves@exemplo.com", agora),
                new Cliente("Eduarda Martins Costa", "14991110005", "eduarda.costa@exemplo.com", agora),
                new Cliente("Felipe Augusto Nunes", "1432220006", "felipe.nunes@exemplo.com", agora),
                new Cliente("Gabriela Ramos Teixeira", "14991110007", "gabriela.teixeira@exemplo.com", agora),
                new Cliente("Heitor Campos Moreira", "14991110008", "heitor.moreira@exemplo.com", agora),
                new Cliente("Isabela Duarte Pires", "1432220009", "isabela.pires@exemplo.com", agora),
                new Cliente("João Victor Mendes", "14991110010", "joao.mendes@exemplo.com", agora));
        clienteRepository.saveAll(clientes);

        LocalDate hoje = agora.toLocalDate();
        LocalDate amanhaUtil = diaDeFuncionamento(hoje, 1);
        LocalDate depoisUtil = diaDeFuncionamento(hoje, 2);
        LocalDate anteriorUtil = diaDeFuncionamento(hoje, -1);

        // Códigos de acesso FIXOS apenas na massa fictícia (dev/test), para facilitar testes manuais.
        // Agendamentos criados pela API recebem códigos aleatórios.
        List<Agendamento> agendamentos = List.of(
                new Agendamento("SEMENTE2", clientes.get(0), carlos, corte, amanhaUtil.atTime(10, 0),
                        StatusAgendamento.AGENDADO, agora),
                new Agendamento("SEMENTE3", clientes.get(1), rafael, corteBarba, amanhaUtil.atTime(14, 0),
                        StatusAgendamento.AGENDADO, agora),
                new Agendamento("SEMENTE4", clientes.get(2), carlos, barba, depoisUtil.atTime(9, 30),
                        StatusAgendamento.CANCELADO, agora),
                new Agendamento("SEMENTE5", clientes.get(3), rafael, corte, anteriorUtil.atTime(11, 0),
                        StatusAgendamento.CONCLUIDO, agora),
                new Agendamento("SEMENTE6", clientes.get(4), carlos, sobrancelha, depoisUtil.atTime(16, 0),
                        StatusAgendamento.AGENDADO, agora));
        agendamentoRepository.saveAll(agendamentos);

        return new ResumoCarga(3, 5, clientes.size(), agendamentos.size());
    }

    /** Avança (ou recua, se negativo) a quantidade indicada de dias de funcionamento (segunda a sábado). */
    private static LocalDate diaDeFuncionamento(LocalDate base, int deslocamento) {
        int passo = deslocamento >= 0 ? 1 : -1;
        int restantes = Math.abs(deslocamento);
        LocalDate data = base;
        while (restantes > 0) {
            data = data.plusDays(passo);
            if (data.getDayOfWeek() != DayOfWeek.SUNDAY) {
                restantes--;
            }
        }
        return data;
    }
}
