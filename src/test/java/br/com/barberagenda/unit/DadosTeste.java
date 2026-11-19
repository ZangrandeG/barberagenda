package br.com.barberagenda.unit;

import java.math.BigDecimal;
import java.time.Clock;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.ZoneId;

import br.com.barberagenda.dto.AgendamentoRequest;
import br.com.barberagenda.model.Agendamento;
import br.com.barberagenda.model.Barbeiro;
import br.com.barberagenda.model.Cliente;
import br.com.barberagenda.model.Servico;
import br.com.barberagenda.model.StatusAgendamento;

/**
 * Dados fictícios e relógio fixo compartilhados pelos testes de unidade.
 * "Agora" é quarta-feira, 18/11/2026, 10:00 (America/Sao_Paulo), o que torna os testes de data reproduzíveis.
 */
final class DadosTeste {

    static final ZoneId FUSO = ZoneId.of("America/Sao_Paulo");
    static final LocalDateTime AGORA = LocalDateTime.of(2026, 11, 18, 10, 0);
    static final Clock RELOGIO = Clock.fixed(AGORA.atZone(FUSO).toInstant(), FUSO);

    static final LocalDate HOJE = AGORA.toLocalDate();          // quarta-feira
    static final LocalDate ONTEM = HOJE.minusDays(1);           // terça-feira
    static final LocalDate DF1 = LocalDate.of(2026, 11, 19);    // quinta-feira
    static final LocalDate DF3 = LocalDate.of(2026, 11, 21);    // sábado
    static final LocalDate DOMINGO = LocalDate.of(2026, 11, 22);
    static final LocalDate D_MAIS_30 = HOJE.plusDays(30);       // 18/12/2026, sexta-feira
    static final LocalDate D_MAIS_31 = HOJE.plusDays(31);       // 19/12/2026, sábado

    static final String EMAIL = "ana.rocha@exemplo.com";

    private DadosTeste() {
    }

    static Cliente cliente() {
        return new Cliente("Ana Beatriz Rocha", "14991110001", EMAIL, AGORA);
    }

    static Barbeiro barbeiro(boolean ativo) {
        return new Barbeiro("Rafael Tesoura", ativo);
    }

    static Servico servico(int duracaoMinutos, boolean ativo) {
        return new Servico("Serviço de teste", duracaoMinutos, new BigDecimal("45.00"), ativo);
    }

    static AgendamentoRequest pedido(LocalDateTime inicio) {
        return new AgendamentoRequest(EMAIL, 1L, 2L, inicio);
    }

    static Agendamento agendamento(LocalDateTime inicio, int duracaoMinutos, StatusAgendamento status) {
        return new Agendamento("TESTE234", cliente(), barbeiro(true), servico(duracaoMinutos, true), inicio, status, AGORA);
    }
}
