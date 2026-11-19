package br.com.barberagenda.e2e;

import static org.assertj.core.api.Assertions.assertThat;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import br.com.barberagenda.e2e.pages.PaginaAdmin;

@DisplayName("E2E — login do administrador e cadastro de serviço (RF-06, RF-07)")
class AdminServicoE2ETest extends TesteE2EBase {

    @Test
    @DisplayName("CT-027 + CT-030 / RF-06, RF-07 — área restrita exige login; admin cadastra serviço no limite mínimo e sai")
    void deveEntrarCadastrarServicoESair() {
        PaginaAdmin admin = new PaginaAdmin(driver, espera, baseUrl()).abrirAreaRestrita();
        assertThat(admin.urlAtual()).endsWith("/admin/login.html");

        admin.entrar("admin", "admin123");                 // credencial fictícia (perfil test)
        assertThat(admin.usuarioLogado()).isEqualTo("Usuário: admin");

        admin.abrirServicos().cadastrarServico("Acabamento", "15", "1");
        assertThat(admin.mensagemServico()).matches("Serviço cadastrado \\(código \\d+\\)\\.");
        assertThat(admin.linhaDaTabela("Acabamento")).contains("15 min").contains("R$ 1,00").contains("Ativo");

        admin.sair();
        assertThat(admin.mensagemLogin()).isEqualTo("Você saiu da área administrativa.");
    }
}
