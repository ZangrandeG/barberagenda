"use strict";

(() => {
    const form = document.getElementById("form-consulta");
    const campoCodigo = document.getElementById("campo-codigo-agendamento");
    const campoEmail = document.getElementById("campo-email-consulta");
    const mensagem = document.getElementById("mensagem-consulta");
    const detalhes = document.getElementById("detalhes-agendamento");
    const botaoCancelar = document.getElementById("botao-cancelar-agendamento");
    const confirmacao = document.getElementById("confirmacao-cancelamento");
    const botaoConfirmar = document.getElementById("botao-confirmar-cancelamento");
    const botaoDesistir = document.getElementById("botao-desistir-cancelamento");
    const mapaErros = { codigo: "erro-codigo-agendamento", email: "erro-email-consulta" };

    let consultado = null;

    function mostrar(agendamento) {
        consultado = agendamento;
        document.getElementById("detalhe-codigo").textContent = "#" + agendamento.id;
        document.getElementById("detalhe-cliente").textContent = agendamento.clienteNome;
        document.getElementById("detalhe-barbeiro").textContent = agendamento.barbeiroNome;
        document.getElementById("detalhe-servico").textContent =
            agendamento.servicoNome + " (" + agendamento.duracaoMinutos + " min)";
        document.getElementById("detalhe-data-hora").textContent = Tela.dataHora(agendamento.dataHoraInicio);
        document.getElementById("detalhe-preco").textContent = Tela.dinheiro(agendamento.preco);
        const status = document.getElementById("detalhe-status");
        status.replaceChildren(Tela.etiqueta(agendamento.status, agendamento.status));
        botaoCancelar.classList.toggle("oculto", agendamento.status !== "AGENDADO");
        confirmacao.classList.add("oculto");
        detalhes.classList.remove("oculto");
    }

    form.addEventListener("submit", async (evento) => {
        evento.preventDefault();
        Tela.mensagem(mensagem, "", "");
        detalhes.classList.add("oculto");
        const campos = {};
        if (!campoCodigo.value) campos.codigo = "Informe o código do agendamento.";
        if (!campoEmail.value.trim()) campos.email = "Informe o e-mail.";
        Tela.errosCampos(campos, mapaErros);
        if (Object.keys(campos).length) return;

        const url = "/api/agendamentos/" + encodeURIComponent(campoCodigo.value)
            + "?email=" + encodeURIComponent(campoEmail.value.trim());
        try {
            mostrar(await Api.get(url));
        } catch (erro) {
            Tela.mensagem(mensagem, erro.message, "erro");
        }
    });

    botaoCancelar.addEventListener("click", () => {
        confirmacao.classList.remove("oculto");
        botaoCancelar.classList.add("oculto");
    });

    botaoDesistir.addEventListener("click", () => {
        confirmacao.classList.add("oculto");
        botaoCancelar.classList.remove("oculto");
    });

    botaoConfirmar.addEventListener("click", async () => {
        botaoConfirmar.disabled = true;
        try {
            const atualizado = await Api.patch("/api/agendamentos/" + consultado.id + "/cancelar",
                { email: campoEmail.value.trim() });
            mostrar(atualizado);
            Tela.mensagem(mensagem, "Agendamento cancelado com sucesso.", "sucesso");
        } catch (erro) {
            Tela.mensagem(mensagem, erro.message, "erro");
        } finally {
            botaoConfirmar.disabled = false;
        }
    });
})();
