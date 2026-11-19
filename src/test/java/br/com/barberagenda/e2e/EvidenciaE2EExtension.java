package br.com.barberagenda.e2e;

import java.io.IOException;
import java.io.UncheckedIOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;

import org.junit.jupiter.api.extension.AfterTestExecutionCallback;
import org.junit.jupiter.api.extension.ExtensionContext;
import org.openqa.selenium.OutputType;
import org.openqa.selenium.TakesScreenshot;
import org.openqa.selenium.WebDriver;

/**
 * Salva uma captura de tela ao final de cada teste de interface, logo após o método de teste
 * (antes de o navegador ser fechado): target/selenium-evidencias/Classe_metodo_<navegador>_<janela>_OK|FALHA.png.
 * Em caso de falha, a captura mostra o estado da tela no momento do erro.
 */
class EvidenciaE2EExtension implements AfterTestExecutionCallback {

    static final Path PASTA = Path.of("target", "selenium-evidencias");

    @Override
    public void afterTestExecution(ExtensionContext contexto) {
        Object instancia = contexto.getRequiredTestInstance();
        if (!(instancia instanceof TesteE2EBase teste) || teste.driver() == null) {
            return;
        }
        WebDriver driver = teste.driver();
        String situacao = contexto.getExecutionException().isPresent() ? "FALHA" : "OK";
        String nome = String.format("%s_%s_%s_%s_%s.png", contexto.getRequiredTestClass().getSimpleName(),
                contexto.getRequiredTestMethod().getName(), System.getProperty("navegador", "chrome"),
                System.getProperty("janela", "1366x768"), situacao);
        try {
            Files.createDirectories(PASTA);
            Path captura = ((TakesScreenshot) driver).getScreenshotAs(OutputType.FILE).toPath();
            Files.copy(captura, PASTA.resolve(nome), StandardCopyOption.REPLACE_EXISTING);
        } catch (IOException erro) {
            throw new UncheckedIOException("Não foi possível salvar a captura " + nome, erro);
        }
    }
}
