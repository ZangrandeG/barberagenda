package br.com.barberagenda.e2e.pages;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.support.ui.WebDriverWait;

/** Tela de cadastro de cliente (/cadastro.html). */
public class PaginaCadastro extends Pagina {

    public PaginaCadastro(WebDriver driver, WebDriverWait espera, String baseUrl) {
        super(driver, espera, baseUrl);
    }

    public PaginaCadastro abrir() {
        driver.get(baseUrl + "/cadastro.html");
        return this;
    }

    public PaginaCadastro cadastrar(String nome, String telefone, String email) {
        digitar("campo-nome-cliente", nome);
        digitar("campo-telefone-cliente", telefone);
        digitar("campo-email-cliente", email);
        clicar("botao-cadastrar-cliente");
        return this;
    }

    public String mensagem() {
        return textoQuandoPreenchido("mensagem-cadastro");
    }

    public String erroNome() {
        return textoQuandoPreenchido("erro-nome-cliente");
    }

    public boolean linkParaAgendarVisivel() {
        return visivel("link-agendar-apos-cadastro");
    }
}
