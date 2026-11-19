package br.com.barberagenda.e2e.pages;

import java.time.LocalDate;
import java.util.List;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

/** Tela de agendamento (/agendar.html). */
public class PaginaAgendamento extends Pagina {

    public PaginaAgendamento(WebDriver driver, WebDriverWait espera, String baseUrl) {
        super(driver, espera, baseUrl);
    }

    public PaginaAgendamento abrir() {
        driver.get(baseUrl + "/agendar.html");
        return this;
    }

    public PaginaAgendamento escolher(String email, String barbeiro, String servico, LocalDate data) {
        if (email != null) {
            digitar("campo-email-agendamento", email);
        }
        selecionarPorPrefixo("campo-barbeiro", barbeiro);
        selecionarPorPrefixo("campo-servico", servico);
        definirData("campo-data", data);
        clicar("botao-buscar-horarios");
        espera.until(d -> !d.findElements(By.cssSelector("#lista-horarios button")).isEmpty()
                || !d.findElement(By.id("mensagem-horarios")).getText().isBlank());
        return this;
    }

    public List<String> horariosDisponiveis() {
        return driver.findElements(By.cssSelector("#lista-horarios button")).stream().map(WebElement::getText).toList();
    }

    public PaginaAgendamento confirmar(String horario) {
        espera.until(ExpectedConditions.elementToBeClickable(By.cssSelector("[data-testid='horario-" + horario + "']"))).click();
        clicar("botao-confirmar-agendamento");
        return this;
    }

    public String mensagem() {
        return textoQuandoPreenchido("mensagem-agendamento");
    }

    public String codigoAcesso() {
        return textoQuandoPreenchido("codigo-acesso");
    }

    public String resumo(String campo) {
        return textoQuandoPreenchido("resumo-" + campo);
    }
}
