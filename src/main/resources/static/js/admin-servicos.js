"use strict";

(() => {
    const form = document.getElementById("form-servico");
    const titulo = document.getElementById("titulo-form-servico");
    const campoId = document.getElementById("campo-id-servico");
    const campoNome = document.getElementById("campo-nome-servico");
    const campoDuracao = document.getElementById("campo-duracao-servico");
    const campoPreco = document.getElementById("campo-preco-servico");
    const campoAtivo = document.getElementById("campo-ativo-servico");
    const botaoCancelarEdicao = document.getElementById("botao-cancelar-edicao-servico");
    const mensagem = document.getElementById("mensagem-servico");
    const corpoTabela = document.querySelector("#tabela-servicos tbody");
    const mapaErros = {
        nome: "erro-nome-servico",
        duracaoMinutos: "erro-duracao-servico",
        preco: "erro-preco-servico",
    };

    function modoInclusao() {
        form.reset();
        campoId.value = "";
        campoAtivo.checked = true;
        titulo.textContent = "Novo serviço";
        botaoCancelarEdicao.classList.add("oculto");
        Tela.errosCampos({}, mapaErros);
    }

    function modoEdicao(servico) {
        campoId.value = servico.id;
        campoNome.value = servico.nome;
        campoDuracao.value = servico.duracaoMinutos;
        campoPreco.value = servico.preco;
        campoAtivo.checked = servico.ativo;
        titulo.textContent = "Editar serviço #" + servico.id;
        botaoCancelarEdicao.classList.remove("oculto");
        Tela.errosCampos({}, mapaErros);
        campoNome.focus();
    }

    /** Campo vazio vira null para que a API informe "obrigatório"; caso contrário envia o número. */
    function numeroOuNulo(valor) {
        return valor === "" ? null : Number(valor);
    }

    async function excluir(servico, botao) {
        if (botao.dataset.confirmar !== "sim") {
            botao.dataset.confirmar = "sim";
            botao.textContent = "Confirmar exclusão";
            return;
        }
        try {
            await Api.excluir("/api/admin/servicos/" + servico.id);
            Tela.mensagem(mensagem, "Serviço excluído.", "sucesso");
            await carregar();
        } catch (erro) {
            Admin.tratarErro(erro, mensagem);
            botao.dataset.confirmar = "";
            botao.textContent = "Excluir";
        }
    }

    async function carregar() {
        try {
            const servicos = await Api.get("/api/admin/servicos");
            corpoTabela.replaceChildren();
            servicos.forEach((s) => {
                const linha = document.createElement("tr");
                linha.dataset.testid = "linha-servico-" + s.id;
                Tela.celula(linha, s.id);
                Tela.celula(linha, s.nome);
                Tela.celula(linha, s.duracaoMinutos + " min");
                Tela.celula(linha, Tela.dinheiro(s.preco));
                Tela.celula(linha, "").appendChild(
                    Tela.etiqueta(s.ativo ? "Ativo" : "Inativo", s.ativo ? "ativo" : "inativo"));
                const acoes = document.createElement("div");
                acoes.className = "acoes";
                const editar = Tela.botao("Editar", "editar-servico-" + s.id, "secundario");
                editar.addEventListener("click", () => modoEdicao(s));
                const remover = Tela.botao("Excluir", "excluir-servico-" + s.id, "perigo");
                remover.addEventListener("click", () => excluir(s, remover));
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
        const dados = {
            nome: campoNome.value,
            duracaoMinutos: numeroOuNulo(campoDuracao.value),
            preco: numeroOuNulo(campoPreco.value),
            ativo: campoAtivo.checked,
        };
        const id = campoId.value;
        try {
            if (id) {
                await Api.put("/api/admin/servicos/" + id, dados);
                Tela.mensagem(mensagem, "Serviço atualizado.", "sucesso");
            } else {
                const novo = await Api.post("/api/admin/servicos", dados);
                Tela.mensagem(mensagem, "Serviço cadastrado (código " + novo.id + ").", "sucesso");
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
