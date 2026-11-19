package br.com.barberagenda.e2e.pages;

import java.time.LocalDate;

import org.openqa.selenium.By;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.Select;
import org.openqa.selenium.support.ui.WebDriverWait;

/** Comportamento comum dos Page Objects: localização por id/data-testid e esperas explícitas (sem Thread.sleep). */
public abstract class Pagina {

    protected final WebDriver driver;
    protected final WebDriverWait espera;
    protected final String baseUrl;

    protected Pagina(WebDriver driver, WebDriverWait espera, String baseUrl) {
        this.driver = driver;
        this.espera = espera;
        this.baseUrl = baseUrl;
    }

    protected WebElement elemento(String id) {
        return espera.until(ExpectedConditions.visibilityOfElementLocated(By.id(id)));
    }

    protected void digitar(String id, String texto) {
        WebElement campo = elemento(id);
        campo.clear();
        campo.sendKeys(texto);
    }

    protected void clicar(String id) {
        espera.until(ExpectedConditions.elementToBeClickable(By.id(id))).click();
    }

    /** Espera o elemento ganhar texto (mensagens preenchidas pelo JavaScript após a resposta da API). */
    protected String textoQuandoPreenchido(String id) {
        WebElement alvo = driver.findElement(By.id(id));
        espera.until(d -> !alvo.getText().isBlank());
        return alvo.getText().trim();
    }

    /** Seleciona a opção cujo texto começa com o prefixo, esperando a lista ser carregada pela API. */
    protected void selecionarPorPrefixo(String id, String prefixo) {
        By opcao = By.xpath("//select[@id='" + id + "']/option[starts-with(normalize-space(.), '" + prefixo + "')]");
        WebElement alvo = espera.until(ExpectedConditions.presenceOfElementLocated(opcao));
        new Select(elemento(id)).selectByVisibleText(alvo.getText());
    }

    /** Campos type="date" variam conforme o idioma do navegador; o valor ISO é definido diretamente. */
    protected void definirData(String id, LocalDate data) {
        WebElement campo = elemento(id);
        ((JavascriptExecutor) driver).executeScript(
                "arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('change'));",
                campo, data.toString());
    }

    public boolean visivel(String id) {
        return !driver.findElements(By.id(id)).isEmpty() && driver.findElement(By.id(id)).isDisplayed();
    }

    public String urlAtual() {
        return driver.getCurrentUrl();
    }
}
