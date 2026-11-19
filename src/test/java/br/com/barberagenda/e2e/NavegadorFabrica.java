package br.com.barberagenda.e2e;

import org.openqa.selenium.Dimension;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.firefox.FirefoxOptions;

/**
 * Cria o navegador dos testes. Propriedades de sistema (opcionais):
 * -Dnavegador=chrome|firefox (padrão chrome), -Djanela=LARGURAxALTURA (padrão 1366x768),
 * -Dheadless=true|false (padrão true). O driver é obtido automaticamente pelo Selenium Manager.
 */
final class NavegadorFabrica {

    private NavegadorFabrica() {
    }

    static WebDriver criar() {
        String navegador = System.getProperty("navegador", "chrome").toLowerCase();
        boolean semJanela = Boolean.parseBoolean(System.getProperty("headless", "true"));
        String[] tamanho = System.getProperty("janela", "1366x768").toLowerCase().split("x");
        Dimension dimensao = new Dimension(Integer.parseInt(tamanho[0]), Integer.parseInt(tamanho[1]));

        WebDriver driver;
        if ("firefox".equals(navegador)) {
            FirefoxOptions opcoes = new FirefoxOptions();
            if (semJanela) {
                opcoes.addArguments("-headless");
            }
            driver = new FirefoxDriver(opcoes);
        } else {
            ChromeOptions opcoes = new ChromeOptions();
            if (semJanela) {
                opcoes.addArguments("--headless=new");
            }
            opcoes.addArguments("--window-size=" + dimensao.getWidth() + "," + dimensao.getHeight(), "--lang=pt-BR");
            driver = new ChromeDriver(opcoes);
        }
        driver.manage().window().setSize(dimensao);
        return driver;
    }
}
