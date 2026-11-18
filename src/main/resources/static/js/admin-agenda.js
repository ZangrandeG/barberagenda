"use strict";

(() => {
    const form = document.getElementById("form-agenda");
    const campoBarbeiro = document.getElementById("campo-barbeiro-agenda");
    const campoData = document.getElementById("campo-data-agenda");
    const mensagem = document.getElementById("mensagem-agenda");
    const corpoTabela = document.querySelector("#tabela-agenda tbody");

    async function concluir(agendamento, botao) {
        botao.disabled = true;
        try {
            await Api.patch("/api/admin/agendamentos/" + agendamento.id + "/concluir");
            Tela.mensagem(mensagem, "Atendimento #" + agendamento.id + " marcado como concluído.", "sucesso");
            await carregar();
        } catch (erro) {
            Admin.tratarErro(erro, mensagem);
            botao.disabled = false;
        }
    }

    async function carregar() {
        if (!campoBarbeiro.value || !campoData.value) {
            Tela.mensagem(mensagem, "Selecione o barbeiro e a data.", "erro");
            return;
        }
        const parametros = new URLSearchParams({ barbeiroId: campoBarbeiro.value, data: campoData.value });
        try {
            const agenda = await Api.get("/api/admin/agenda?" + parametros);
            corpoTabela.replaceChildren();
            if (agenda.length === 0) {
                Tela.mensagem(mensagem, "Nenhum agendamento para " + Tela.data(campoData.value) + ".", "info");
                return;
            }
            agenda.forEach((a) => {
                const linha = document.createElement("tr");
                linha.dataset.testid = "linha-agendamento-" + a.id;
                Tela.celula(linha, a.id);
                Tela.celula(linha, Tela.hora(a.dataHoraInicio) + " – " + Tela.hora(a.dataHoraFim));
                Tela.celula(linha, a.clienteNome);
                Tela.celula(linha, a.servicoNome);
                const status = Tela.celula(linha, "");
                status.dataset.testid = "status-agendamento-" + a.id;
                status.appendChild(Tela.etiqueta(a.status, a.status));
                const acoes = Tela.celula(linha, "");
                if (a.status === "AGENDADO") {
                    const botao = Tela.botao("Concluir", "concluir-agendamento-" + a.id);
                    botao.addEventListener("click", () => concluir(a, botao));
                    acoes.appendChild(botao);
                }
                corpoTabela.appendChild(linha);
            });
        } catch (erro) {
            corpoTabela.replaceChildren();
            Admin.tratarErro(erro, mensagem);
        }
    }

    form.addEventListener("submit", (evento) => {
        evento.preventDefault();
        Tela.mensagem(mensagem, "", "");
        carregar();
    });

    campoData.value = Tela.dataLocal(0);
    Admin.carregarBarbeirosEm(campoBarbeiro).catch((erro) => Admin.tratarErro(erro, mensagem));
})();
