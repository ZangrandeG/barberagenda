"use strict";

/* Comportamento comum das páginas administrativas: usuário logado, sair e sessão expirada. */
const Admin = (() => {
    function tratarErro(erro, elementoMensagem) {
        if (erro.status === 401) {
            window.location.href = "/admin/login.html";
            return;
        }
        Tela.mensagem(elementoMensagem, erro.message, "erro");
    }

    async function iniciar() {
        try {
            const sessao = await Api.get("/api/admin/sessao");
            document.getElementById("usuario-logado").textContent = "Usuário: " + sessao.login;
        } catch (erro) {
            if (erro.status === 401) window.location.href = "/admin/login.html";
        }
        document.getElementById("botao-sair").addEventListener("click", async () => {
            try {
                await Api.post("/admin/logout");
            } finally {
                window.location.href = "/admin/login.html?saiu";
            }
        });
    }

    async function carregarBarbeirosEm(select) {
        const barbeiros = await Api.get("/api/admin/barbeiros");
        barbeiros.forEach((b) => {
            const opcao = document.createElement("option");
            opcao.value = b.id;
            opcao.textContent = b.nome + (b.ativo ? "" : " (inativo)");
            select.appendChild(opcao);
        });
        return barbeiros;
    }

    return { iniciar, tratarErro, carregarBarbeirosEm };
})();

Admin.iniciar();
