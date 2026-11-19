package br.com.barberagenda.e2e;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.time.Duration;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.TimeoutException;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import br.com.barberagenda.e2e.pages.PaginaAgendamento;
import br.com.barberagenda.e2e.pages.PaginaCadastro;
import br.com.barberagenda.e2e.pages.PaginaConsulta;

@DisplayName("E2E não funcional — segurança básica na interface (RNF-02)")
class SegurancaE2ETest extends TesteE2EBase {

    private static final String NOME_COM_HTML = "<img src=x onerror=alert('xss')>";

    @Test
    @DisplayName("TNF-04 / RNF-02 — nome com HTML/script é exibido como texto e não é executado")
    void naoDeveExecutarHtmlDigitadoPeloUsuario() {
        String email = "xss." + System.nanoTime() + "@exemplo.com";
        new PaginaCadastro(driver, espera, baseUrl()).abrir().cadastrar(NOME_COM_HTML, "14988887777", email).mensagem();
        PaginaAgendamento agendamento = new PaginaAgendamento(driver, espera, baseUrl()).abrir()
                .escolher(email, "Carlos Navalha", "Barba", dataLivre()).confirmar("10:00");
        String codigo = agendamento.codigoAcesso();

        PaginaConsulta consulta = new PaginaConsulta(driver, espera, baseUrl()).abrir().consultar(codigo, email);

        assertThat(consulta.detalhe("cliente")).isEqualTo(NOME_COM_HTML);
        assertThat(driver.findElements(By.cssSelector("#detalhe-cliente img"))).isEmpty();
        assertThatThrownBy(() -> new WebDriverWait(driver, Duration.ofSeconds(2)).until(ExpectedConditions.alertIsPresent()))
                .isInstanceOf(TimeoutException.class);
    }
}
