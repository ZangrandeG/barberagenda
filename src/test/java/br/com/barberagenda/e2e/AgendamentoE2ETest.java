package br.com.barberagenda.e2e;

import static org.assertj.core.api.Assertions.assertThat;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import br.com.barberagenda.e2e.pages.PaginaAgendamento;

@DisplayName("E2E — agendamento completo (RF-02, RF-03)")
class AgendamentoE2ETest extends TesteE2EBase {

    @Test
    @DisplayName("CT-010 / RF-03 — cliente escolhe barbeiro, serviço, data e horário e recebe o código de acesso")
    void deveAgendarHorarioPelaTela() {
        LocalDate data = dataLivre();
        PaginaAgendamento pagina = new PaginaAgendamento(driver, espera, baseUrl()).abrir()
                .escolher("camila.prado@exemplo.com", "Carlos Navalha", "Barba", data);

        assertThat(pagina.horariosDisponiveis()).startsWith("09:00").contains("11:00").endsWith("18:30");

        pagina.confirmar("11:00");

        assertThat(pagina.mensagem()).startsWith("Agendamento realizado com sucesso! Código de acesso:");
        assertThat(pagina.codigoAcesso()).matches("[A-HJKMNP-Z2-9]{8}");
        assertThat(pagina.resumo("barbeiro")).isEqualTo("Carlos Navalha");
        assertThat(pagina.resumo("servico")).isEqualTo("Barba");
        assertThat(pagina.resumo("data-hora")).isEqualTo(data.format(DateTimeFormatter.ofPattern("dd/MM/yyyy")) + " 11:00");
        assertThat(pagina.resumo("status")).isEqualTo("AGENDADO");
    }
}
