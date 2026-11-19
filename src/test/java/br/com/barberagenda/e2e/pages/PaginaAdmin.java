package br.com.barberagenda.e2e.pages;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

/** Área administrativa: login (/admin/login.html), painel e cadastro de serviços (/admin/servicos.html). */
public class PaginaAdmin extends Pagina {

    public PaginaAdmin(WebDriver driver, WebDriverWait espera, String baseUrl) {
        super(driver, espera, baseUrl);
    }

    public PaginaAdmin abrirAreaRestrita() {
        driver.get(baseUrl + "/admin/");
        return this;
    }

    public PaginaAdmin entrar(String usuario, String senha) {
        digitar("campo-usuario", usuario);
        digitar("campo-senha", senha);
        clicar("botao-entrar");
        espera.until(ExpectedConditions.urlContains("/admin/index.html"));
        return this;
    }

    public String usuarioLogado() {
        return textoQuandoPreenchido("usuario-logado");
    }

    public PaginaAdmin abrirServicos() {
        driver.get(baseUrl + "/admin/servicos.html");
        espera.until(ExpectedConditions.presenceOfElementLocated(By.cssSelector("#tabela-servicos tbody tr")));
        return this;
    }

    public PaginaAdmin cadastrarServico(String nome, String duracao, String preco) {
        digitar("campo-nome-servico", nome);
        digitar("campo-duracao-servico", duracao);
        digitar("campo-preco-servico", preco);
        clicar("botao-salvar-servico");
        return this;
    }

    public String mensagemServico() {
        return textoQuandoPreenchido("mensagem-servico");
    }

    public String linhaDaTabela(String nomeServico) {
        By linha = By.xpath("//table[@id='tabela-servicos']//tr[td[normalize-space(.)='" + nomeServico + "']]");
        return espera.until(ExpectedConditions.visibilityOfElementLocated(linha)).getText();
    }

    public PaginaAdmin sair() {
        clicar("botao-sair");
        espera.until(ExpectedConditions.urlContains("/admin/login.html"));
        return this;
    }

    public String mensagemLogin() {
        return textoQuandoPreenchido("mensagem-login");
    }
}
