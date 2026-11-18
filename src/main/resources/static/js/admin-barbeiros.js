"use strict";

(() => {
    const form = document.getElementById("form-barbeiro");
    const titulo = document.getElementById("titulo-form-barbeiro");
    const campoId = document.getElementById("campo-id-barbeiro");
    const campoNome = document.getElementById("campo-nome-barbeiro");
    const campoAtivo = document.getElementById("campo-ativo-barbeiro");
    const botaoCancelarEdicao = document.getElementById("botao-cancelar-edicao-barbeiro");
    const mensagem = document.getElementById("mensagem-barbeiro");
    const corpoTabela = document.querySelector("#tabela-barbeiros tbody");
    const mapaErros = { nome: "erro-nome-barbeiro" };

    function modoInclusao() {
        form.reset();
        campoId.value = "";
        campoAtivo.checked = true;
        titulo.textContent = "Novo barbeiro";
        botaoCancelarEdicao.classList.add("oculto");
        Tela.errosCampos({}, mapaErros);
    }

    function modoEdicao(barbeiro) {
        campoId.value = barbeiro.id;
        campoNome.value = barbeiro.nome;
        campoAtivo.checked = barbeiro.ativo;
        titulo.textContent = "Editar barbeiro #" + barbeiro.id;
        botaoCancelarEdicao.classList.remove("oculto");
        Tela.errosCampos({}, mapaErros);
        campoNome.focus();
    }

    async function excluir(barbeiro, botao) {
        if (botao.dataset.confirmar !== "sim") {
            botao.dataset.confirmar = "sim";
            botao.textContent = "Confirmar exclusão";
            return;
        }
        try {
            await Api.excluir("/api/admin/barbeiros/" + barbeiro.id);
            Tela.mensagem(mensagem, "Barbeiro excluído.", "sucesso");
            await carregar();
        } catch (erro) {
            Admin.tratarErro(erro, mensagem);
            botao.dataset.confirmar = "";
            botao.textContent = "Excluir";
        }
    }

    async function carregar() {
        try {
            const barbeiros = await Api.get("/api/admin/barbeiros");
            corpoTabela.replaceChildren();
            barbeiros.forEach((b) => {
                const linha = document.createElement("tr");
                linha.dataset.testid = "linha-barbeiro-" + b.id;
                Tela.celula(linha, b.id);
                Tela.celula(linha, b.nome);
                Tela.celula(linha, "").appendChild(
                    Tela.etiqueta(b.ativo ? "Ativo" : "Inativo", b.ativo ? "ativo" : "inativo"));
                const acoes = document.createElement("div");
                acoes.className = "acoes";
                const editar = Tela.botao("Editar", "editar-barbeiro-" + b.id, "secundario");
                editar.addEventListener("click", () => modoEdicao(b));
                const remover = Tela.botao("Excluir", "excluir-barbeiro-" + b.id, "perigo");
                remover.addEventListener("click", () => excluir(b, remover));
                acoes.append(editar, remover);
                Tela.celula(linha, "").appendChild(acoes);
                corpoTabela.appendChild(linha);
            });
        } catch (erro) {
            Admin.tratarErro(erro, mensagem);
        }
    }

    form.addEventListener("submit", async (evento) => {
        evento.preventDefault();
        Tela.mensagem(mensagem, "", "");
        const dados = { nome: campoNome.value, ativo: campoAtivo.checked };
        const id = campoId.value;
        try {
            if (id) {
                await Api.put("/api/admin/barbeiros/" + id, dados);
                Tela.mensagem(mensagem, "Barbeiro atualizado.", "sucesso");
            } else {
                const novo = await Api.post("/api/admin/barbeiros", dados);
                Tela.mensagem(mensagem, "Barbeiro cadastrado (código " + novo.id + ").", "sucesso");
            }
            modoInclusao();
            await carregar();
        } catch (erro) {
            Tela.errosCampos(erro.campos, mapaErros);
            Admin.tratarErro(erro, mensagem);
        }
    });

    botaoCancelarEdicao.addEventListener("click", modoInclusao);
    carregar();
})();
