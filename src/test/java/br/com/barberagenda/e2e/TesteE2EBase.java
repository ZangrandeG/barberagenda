package br.com.barberagenda.e2e;

import java.time.DayOfWeek;
import java.time.Duration;
import java.time.LocalDate;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.extension.ExtendWith;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.server.LocalServerPort;
import org.springframework.test.context.ActiveProfiles;

import br.com.barberagenda.seed.CargaDadosFicticios;

/**
 * Base dos testes de sistema/interface (Selenium). Sobe a aplicação completa no perfil "test"
 * (H2 em memória) em uma porta aleatória, restaura a massa fictícia e abre um navegador novo antes de cada teste.
 * Executar com: ./mvnw test -Pe2e
 */
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@ActiveProfiles("test")
@Tag("e2e")
@ExtendWith(EvidenciaE2EExtension.class)
abstract class TesteE2EBase {

    @LocalServerPort
    private int porta;

    @Autowired
    private CargaDadosFicticios carga;

    protected WebDriver driver;
    protected WebDriverWait espera;

    @BeforeEach
    void prepararNavegador() {
        carga.recarregar();
        driver = NavegadorFabrica.criar();
        espera = new WebDriverWait(driver, Duration.ofSeconds(10));
    }

    @AfterEach
    void fecharNavegador() {
        if (driver != null) {
            driver.quit();
        }
    }

    protected String baseUrl() {
        return "http://localhost:" + porta;
    }

    /** Data de agendamento longe dos agendamentos da massa: 7 dias à frente, pulando domingo. */
    protected static LocalDate dataLivre() {
        LocalDate data = LocalDate.now().plusDays(7);
        return data.getDayOfWeek() == DayOfWeek.SUNDAY ? data.plusDays(1) : data;
    }

    WebDriver driver() {
        return driver;
    }
}
