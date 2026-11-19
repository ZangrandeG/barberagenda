package br.com.barberagenda.e2e.pages;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

/** Tela de consulta e cancelamento (/consulta.html). */
public class PaginaConsulta extends Pagina {

    public PaginaConsulta(WebDriver driver, WebDriverWait espera, String baseUrl) {
        super(driver, espera, baseUrl);
    }

    public PaginaConsulta abrir() {
        driver.get(baseUrl + "/consulta.html");
        return this;
    }

    public PaginaConsulta consultar(String codigo, String email) {
        digitar("campo-codigo-acesso", codigo);
        digitar("campo-email-consulta", email);
        clicar("botao-consultar");
        espera.until(ExpectedConditions.visibilityOfElementLocated(By.id("detalhes-agendamento")));
        return this;
    }

    public String detalhe(String campo) {
        return textoQuandoPreenchido("detalhe-" + campo);
    }

    public PaginaConsulta cancelar() {
        clicar("botao-cancelar-agendamento");
        clicar("botao-confirmar-cancelamento");
        espera.until(ExpectedConditions.textToBe(By.id("detalhe-status"), "CANCELADO"));
        return this;
    }

    public String mensagem() {
        return textoQuandoPreenchido("mensagem-consulta");
    }

    public boolean botaoCancelarVisivel() {
        return visivel("botao-cancelar-agendamento");
    }
}
