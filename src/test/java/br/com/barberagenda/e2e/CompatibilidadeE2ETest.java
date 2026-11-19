package br.com.barberagenda.e2e;

import static org.assertj.core.api.Assertions.assertThat;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import org.openqa.selenium.By;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;

/**
 * Executado em cada combinação de navegador e janela (-Dnavegador, -Djanela). Junto com os demais testes E2E,
 * compõe o teste de compatibilidade TNF-07.
 */
@DisplayName("E2E não funcional — compatibilidade de layout (RNF-03)")
class CompatibilidadeE2ETest extends TesteE2EBase {

    @ParameterizedTest(name = "{0}")
    @CsvSource({
            "/index.html, link-agendar",
            "/cadastro.html, botao-cadastrar-cliente",
            "/agendar.html, botao-buscar-horarios",
            "/consulta.html, botao-consultar",
            "/admin/login.html, botao-entrar"})
    @DisplayName("TNF-07 / RNF-03 — página sem rolagem horizontal e com o botão principal visível")
    void devePaginaCaberNaLarguraDaJanela(String caminho, String idBotaoPrincipal) {
        driver.get(baseUrl() + caminho);
        WebElement botao = espera.until(ExpectedConditions.presenceOfElementLocated(By.id(idBotaoPrincipal)));
        ((JavascriptExecutor) driver).executeScript("arguments[0].scrollIntoView({block: 'center'});", botao);

        long larguraConteudo = (Long) ((JavascriptExecutor) driver).executeScript("return document.documentElement.scrollWidth;");
        long larguraJanela = (Long) ((JavascriptExecutor) driver).executeScript("return document.documentElement.clientWidth;");

        assertThat(larguraConteudo).as("largura do conteúdo x largura visível").isLessThanOrEqualTo(larguraJanela);
        assertThat(botao.isDisplayed()).isTrue();
        assertThat(botao.getSize().getWidth()).isPositive();
    }
}
