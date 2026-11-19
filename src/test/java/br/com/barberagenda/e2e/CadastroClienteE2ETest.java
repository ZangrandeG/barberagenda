package br.com.barberagenda.e2e;

import static org.assertj.core.api.Assertions.assertThat;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import br.com.barberagenda.e2e.pages.PaginaCadastro;

@DisplayName("E2E — cadastro de cliente (RF-01)")
class CadastroClienteE2ETest extends TesteE2EBase {

    @Test
    @DisplayName("CT-001 / RF-01 — cadastro com dados válidos mostra sucesso, código e atalho para agendar")
    void deveCadastrarClientePelaTela() {
        PaginaCadastro pagina = new PaginaCadastro(driver, espera, baseUrl()).abrir()
                .cadastrar("Marina Lopes Teixeira", "14988776655", "marina.e2e." + System.nanoTime() + "@exemplo.com");

        assertThat(pagina.mensagem()).matches("Cadastro realizado com sucesso! Código do cliente: \\d+\\.");
        assertThat(pagina.linkParaAgendarVisivel()).isTrue();
    }

    @Test
    @DisplayName("CT-003 / RF-01 — nome com 2 caracteres é recusado com mensagem no campo")
    void deveRecusarNomeCurtoPelaTela() {
        PaginaCadastro pagina = new PaginaCadastro(driver, espera, baseUrl()).abrir()
                .cadastrar("Al", "14988776655", "nome.curto@exemplo.com");

        assertThat(pagina.erroNome()).isEqualTo("O nome deve ter entre 3 e 60 caracteres.");
        assertThat(pagina.mensagem()).isEqualTo("Existem campos inválidos.");
        assertThat(pagina.linkParaAgendarVisivel()).isFalse();
    }
}
