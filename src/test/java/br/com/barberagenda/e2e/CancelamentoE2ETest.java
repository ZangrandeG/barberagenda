package br.com.barberagenda.e2e;

import static org.assertj.core.api.Assertions.assertThat;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import br.com.barberagenda.e2e.pages.PaginaAgendamento;
import br.com.barberagenda.e2e.pages.PaginaConsulta;

@DisplayName("E2E — consulta e cancelamento pelo cliente (RF-05)")
class CancelamentoE2ETest extends TesteE2EBase {

    @Test
    @DisplayName("CT-023 + CT-025 / RF-05 — consulta com código em minúsculas, cancela e o horário volta a ficar livre")
    void deveConsultarECancelarAgendamentoLiberandoOHorario() {
        PaginaConsulta consulta = new PaginaConsulta(driver, espera, baseUrl()).abrir()
                .consultar("semente6", "eduarda.costa@exemplo.com");

        assertThat(consulta.detalhe("codigo")).isEqualTo("SEMENTE6");
        assertThat(consulta.detalhe("status")).isEqualTo("AGENDADO");
        String dataHora = consulta.detalhe("data-hora");               // ex.: 23/11/2026 16:00
        assertThat(dataHora).endsWith("16:00");

        consulta.cancelar();

        assertThat(consulta.mensagem()).isEqualTo("Agendamento cancelado com sucesso.");
        assertThat(consulta.botaoCancelarVisivel()).isFalse();

        LocalDate data = LocalDate.parse(dataHora.substring(0, 10), DateTimeFormatter.ofPattern("dd/MM/yyyy"));
        PaginaAgendamento agendamento = new PaginaAgendamento(driver, espera, baseUrl()).abrir()
                .escolher(null, "Carlos Navalha", "Sobrancelha", data);
        assertThat(agendamento.horariosDisponiveis()).contains("16:00");
    }
}
