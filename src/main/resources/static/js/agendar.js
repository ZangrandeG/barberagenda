"use strict";

(() => {
    const form = document.getElementById("form-agendamento");
    const campoEmail = document.getElementById("campo-email-agendamento");
    const campoBarbeiro = document.getElementById("campo-barbeiro");
    const campoServico = document.getElementById("campo-servico");
    const campoData = document.getElementById("campo-data");
    const botaoBuscar = document.getElementById("botao-buscar-horarios");
    const botaoConfirmar = document.getElementById("botao-confirmar-agendamento");
    const tituloHorarios = document.getElementById("titulo-horarios");
    const listaHorarios = document.getElementById("lista-horarios");
    const mensagemHorarios = document.getElementById("mensagem-horarios");
    const mensagem = document.getElementById("mensagem-agendamento");
    const resumo = document.getElementById("resumo-agendamento");
    const mapaErros = {
        emailCliente: "erro-email-agendamento",
        barbeiroId: "erro-barbeiro",
        servicoId: "erro-servico",
        data: "erro-data",
        dataHoraInicio: "erro-horario",
    };

    let horarioSelecionado = null;

    function limparHorarios() {
        horarioSelecionado = null;
        listaHorarios.replaceChildren();
        tituloHorarios.classList.add("oculto");
        Tela.mensagem(mensagemHorarios, "", "");
        botaoConfirmar.disabled = true;
    }

    function preencherOpcoes(select, itens, rotulo) {
        itens.forEach((item) => {
            const opcao = document.createElement("option");
            opcao.value = item.id;
            opcao.textContent = rotulo(item);
            select.appendChild(opcao);
        });
    }

    async function carregarCatalogo() {
        try {
            const [barbeiros, servicos] = await Promise.all([Api.get("/api/barbeiros"), Api.get("/api/servicos")]);
            preencherOpcoes(campoBarbeiro, barbeiros, (b) => b.nome);
            preencherOpcoes(campoServico, servicos,
                (s) => s.nome + " — " + s.duracaoMinutos + " min — " + Tela.dinheiro(s.preco));
        } catch (erro) {
            Tela.mensagem(mensagem, "Não foi possível carregar barbeiros e serviços: " + erro.message, "erro");
        }
    }

    function validarSelecao() {
        const campos = {};
        if (!campoBarbeiro.value) campos.barbeiroId = "Selecione um barbeiro.";
        if (!campoServico.value) campos.servicoId = "Selecione um serviço.";
        if (!campoData.value) campos.data = "Informe a data.";
        Tela.errosCampos(campos, mapaErros);
        return Object.keys(campos).length === 0;
    }

    async function buscarHorarios() {
        limparHorarios();
        Tela.mensagem(mensagem, "", "");
        if (!validarSelecao()) return;

        const parametros = new URLSearchParams({
            barbeiroId: campoBarbeiro.value,
            servicoId: campoServico.value,
            data: campoData.value,
        });
        try {
            const resposta = await Api.get("/api/horarios-disponiveis?" + parametros);
            tituloHorarios.classList.remove("oculto");
            if (resposta.horarios.length === 0) {
                Tela.mensagem(mensagemHorarios, "Nenhum horário disponível para a data selecionada.", "info");
                return;
            }
            resposta.horarios.forEach((horario) => {
                const botao = Tela.botao(horario, "horario-" + horario);
                botao.dataset.horario = horario;
                botao.setAttribute("aria-pressed", "false");
                botao.addEventListener("click", () => selecionarHorario(botao));
                listaHorarios.appendChild(botao);
            });
        } catch (erro) {
            Tela.errosCampos(erro.campos, mapaErros);
            Tela.mensagem(mensagemHorarios, erro.message, "erro");
        }
    }

    function selecionarHorario(botao) {
        listaHorarios.querySelectorAll("button").forEach((b) => {
            b.classList.remove("selecionado");
            b.setAttribute("aria-pressed", "false");
        });
        botao.classList.add("selecionado");
        botao.setAttribute("aria-pressed", "true");
        horarioSelecionado = botao.dataset.horario;
        botaoConfirmar.disabled = false;
    }

    function mostrarResumo(agendamento) {
        document.getElementById("codigo-acesso").textContent = agendamento.codigoAcesso;
        document.getElementById("resumo-barbeiro").textContent = agendamento.barbeiroNome;
        document.getElementById("resumo-servico").textContent = agendamento.servicoNome;
        document.getElementById("resumo-data-hora").textContent = Tela.dataHora(agendamento.dataHoraInicio);
        document.getElementById("resumo-status").textContent = agendamento.status;
        resumo.classList.remove("oculto");
    }

    form.addEventListener("submit", async (evento) => {
        evento.preventDefault();
        Tela.mensagem(mensagem, "", "");
        resumo.classList.add("oculto");
        if (!horarioSelecionado) {
            Tela.errosCampos({ dataHoraInicio: "Selecione um horário." }, mapaErros);
            return;
        }
        botaoConfirmar.disabled = true;
        const pedido = {
            emailCliente: campoEmail.value,
            barbeiroId: Number(campoBarbeiro.value),
            servicoId: Number(campoServico.value),
            dataHoraInicio: campoData.value + "T" + horarioSelecionado + ":00",
        };
        try {
            const agendamento = await Api.post("/api/agendamentos", pedido);
            Tela.errosCampos({}, mapaErros);
            Tela.mensagem(mensagem,
                "Agendamento realizado com sucesso! Código de acesso: " + agendamento.codigoAcesso + ".", "sucesso");
            mostrarResumo(agendamento);
            limparHorarios();
        } catch (erro) {
            Tela.errosCampos(erro.campos, mapaErros);
            Tela.mensagem(mensagem, erro.message, "erro");
            botaoConfirmar.disabled = false;
        }
    });

    botaoBuscar.addEventListener("click", buscarHorarios);
    [campoBarbeiro, campoServico, campoData].forEach((campo) => campo.addEventListener("change", limparHorarios));

    campoData.min = Tela.dataLocal(0);
    campoData.max = Tela.dataLocal(30);
    const emailInformado = new URLSearchParams(window.location.search).get("email");
    if (emailInformado) campoEmail.value = emailInformado;
    carregarCatalogo();
})();
