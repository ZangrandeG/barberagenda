"use strict";

(() => {
    const form = document.getElementById("form-login");
    const botao = document.getElementById("botao-entrar");
    const mensagem = document.getElementById("mensagem-login");

    const parametros = new URLSearchParams(window.location.search);
    if (parametros.has("saiu")) {
        Tela.mensagem(mensagem, "Você saiu da área administrativa.", "info");
    }

    form.addEventListener("submit", async (evento) => {
        evento.preventDefault();
        Tela.mensagem(mensagem, "", "");
        botao.disabled = true;

        const corpo = new URLSearchParams({
            username: document.getElementById("campo-usuario").value,
            password: document.getElementById("campo-senha").value,
        });
        const cabecalhos = { "Content-Type": "application/x-www-form-urlencoded", Accept: "application/json" };
        const tokenCsrf = Api.lerCookie("XSRF-TOKEN");
        if (tokenCsrf) cabecalhos["X-XSRF-TOKEN"] = tokenCsrf;

        try {
            const resposta = await fetch("/admin/login", {
                method: "POST",
                headers: cabecalhos,
                body: corpo,
                credentials: "same-origin",
            });
            if (resposta.ok) {
                window.location.href = "/admin/index.html";
                return;
            }
            const dados = await resposta.json().catch(() => null);
            Tela.mensagem(mensagem, (dados && dados.mensagem) || "Não foi possível entrar.", "erro");
        } catch (e) {
            Tela.mensagem(mensagem, "Não foi possível conectar ao servidor.", "erro");
        } finally {
            botao.disabled = false;
        }
    });
})();
