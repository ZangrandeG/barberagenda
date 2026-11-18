/*
 * Funções comuns às páginas: chamadas à API REST (fetch) e exibição de mensagens.
 * Todo texto vindo da API é inserido com textContent (nunca innerHTML), evitando execução de HTML/script.
 */
"use strict";

const Api = (() => {
    function lerCookie(nome) {
        const item = document.cookie.split("; ").find((c) => c.startsWith(nome + "="));
        return item ? decodeURIComponent(item.substring(nome.length + 1)) : null;
    }

    async function requisitar(metodo, url, corpo) {
        const opcoes = {
            method: metodo,
            headers: { Accept: "application/json" },
            credentials: "same-origin",
        };
        if (corpo !== undefined) {
            opcoes.headers["Content-Type"] = "application/json";
            opcoes.body = JSON.stringify(corpo);
        }
        const tokenCsrf = lerCookie("XSRF-TOKEN");
        if (tokenCsrf) {
            opcoes.headers["X-XSRF-TOKEN"] = tokenCsrf;
        }

        let resposta;
        try {
            resposta = await fetch(url, opcoes);
        } catch (e) {
            const erro = new Error("Não foi possível conectar ao servidor.");
            erro.status = 0;
            erro.campos = {};
            throw erro;
        }

        let dados = null;
        if (resposta.status !== 204) {
            const texto = await resposta.text();
            if (texto) {
                try {
                    dados = JSON.parse(texto);
                } catch (e) {
                    dados = null;
                }
            }
        }

        if (!resposta.ok) {
            const erro = new Error((dados && dados.mensagem) || "Erro " + resposta.status + ".");
            erro.status = resposta.status;
            erro.campos = (dados && dados.campos) || {};
            throw erro;
        }
        return dados;
    }

    return {
        lerCookie,
        get: (url) => requisitar("GET", url),
        post: (url, corpo) => requisitar("POST", url, corpo),
        put: (url, corpo) => requisitar("PUT", url, corpo),
        patch: (url, corpo) => requisitar("PATCH", url, corpo),
        excluir: (url) => requisitar("DELETE", url),
    };
})();

const Tela = (() => {
    const moeda = new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" });

    function mensagem(elemento, texto, tipo) {
        elemento.textContent = texto || "";
        elemento.className = "mensagem" + (texto ? " " + tipo : "");
    }

    /** Mostra erros por campo. "mapa" relaciona o nome do campo da API ao id do elemento de erro. */
    function errosCampos(campos, mapa) {
        Object.values(mapa).forEach((id) => {
            const el = document.getElementById(id);
            if (el) el.textContent = "";
        });
        Object.entries(campos || {}).forEach(([campo, texto]) => {
            const id = mapa[campo];
            const el = id && document.getElementById(id);
            if (el) el.textContent = texto;
        });
    }

    /** "2026-11-20T10:00:00" -> "20/11/2026 10:00" (sem conversão de fuso). */
    function dataHora(iso) {
        if (!iso) return "";
        const [data, hora] = iso.split("T");
        const [ano, mes, dia] = data.split("-");
        return dia + "/" + mes + "/" + ano + " " + hora.substring(0, 5);
    }

    /** "2026-11-20" -> "20/11/2026". */
    function data(iso) {
        if (!iso) return "";
        const [ano, mes, dia] = iso.split("-");
        return dia + "/" + mes + "/" + ano;
    }

    function hora(iso) {
        return iso ? iso.split("T")[1].substring(0, 5) : "";
    }

    function dinheiro(valor) {
        return moeda.format(Number(valor));
    }

    /** Data local do navegador no formato AAAA-MM-DD, deslocada em "dias". */
    function dataLocal(dias) {
        const d = new Date();
        d.setDate(d.getDate() + (dias || 0));
        const mes = String(d.getMonth() + 1).padStart(2, "0");
        const dia = String(d.getDate()).padStart(2, "0");
        return d.getFullYear() + "-" + mes + "-" + dia;
    }

    function celula(linha, texto) {
        const td = document.createElement("td");
        td.textContent = texto;
        linha.appendChild(td);
        return td;
    }

    function etiqueta(texto, classe) {
        const span = document.createElement("span");
        span.className = "etiqueta " + classe;
        span.textContent = texto;
        return span;
    }

    function botao(texto, testId, classe) {
        const b = document.createElement("button");
        b.type = "button";
        b.textContent = texto;
        if (testId) b.dataset.testid = testId;
        if (classe) b.className = classe;
        return b;
    }

    return { mensagem, errosCampos, dataHora, data, hora, dinheiro, dataLocal, celula, etiqueta, botao };
})();
