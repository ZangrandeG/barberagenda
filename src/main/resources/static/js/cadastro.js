"use strict";

(() => {
    const form = document.getElementById("form-cadastro-cliente");
    const botao = document.getElementById("botao-cadastrar-cliente");
    const mensagem = document.getElementById("mensagem-cadastro");
    const proximoPasso = document.getElementById("proximo-passo");
    const linkAgendar = document.getElementById("link-agendar-apos-cadastro");
    const mapaErros = { nome: "erro-nome-cliente", telefone: "erro-telefone-cliente", email: "erro-email-cliente" };

    form.addEventListener("submit", async (evento) => {
        evento.preventDefault();
        Tela.errosCampos({}, mapaErros);
        Tela.mensagem(mensagem, "", "");
        proximoPasso.classList.add("oculto");
        botao.disabled = true;

        const dados = {
            nome: document.getElementById("campo-nome-cliente").value,
            telefone: document.getElementById("campo-telefone-cliente").value,
            email: document.getElementById("campo-email-cliente").value,
        };

        try {
            const cliente = await Api.post("/api/clientes", dados);
            Tela.mensagem(mensagem, "Cadastro realizado com sucesso! Código do cliente: " + cliente.id + ".", "sucesso");
            linkAgendar.href = "/agendar.html?email=" + encodeURIComponent(cliente.email);
            proximoPasso.classList.remove("oculto");
            form.reset();
        } catch (erro) {
            Tela.errosCampos(erro.campos, mapaErros);
            Tela.mensagem(mensagem, erro.message, "erro");
        } finally {
            botao.disabled = false;
        }
    });
})();
