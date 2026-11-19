"""
P10 — Calcula as 8 métricas obrigatórias (manual, seção 9.13) a partir dos dados reais do projeto
(dados/casos.json, dados/testes_complementares.json, dados/requisitos.json, dados/execucoes.csv, dados/defeitos.csv),
gera os gráficos (PNG) e um JSON com os valores. As mesmas fórmulas estão na aba Métricas da planilha P05.
Uso:  python scripts/metricas.py
"""
import csv
import json
import sys
from collections import Counter
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
DADOS = RAIZ / "dados"
SAIDA = RAIZ / "entrega" / "11_METRICAS_E_QUALIDADE" / "metricas"
CORES = {"Aprovado": "#2e7d4f", "Reprovado": "#b23b3b", "Bloqueado": "#c98a1b", "Não executado": "#9e9e9e"}
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.spines.top": False, "axes.spines.right": False})


def ler_csv(nome):
    with open(DADOS / nome, encoding="utf-8", newline="") as f:
        return [l for l in csv.DictReader(f) if any((v or "").strip() for v in l.values())]


def pct(a, b):
    return round(100 * a / b, 1) if b else None


def salvar(fig, nome):
    fig.tight_layout()
    fig.savefig(SAIDA / nome, dpi=150)
    plt.close(fig)


def barras(nome, titulo, rotulos, valores, cores, eixo, limite=None):
    fig, ax = plt.subplots(figsize=(7, 3.6))
    barras_ = ax.bar(rotulos, valores, color=cores)
    ax.set_title(titulo, fontsize=12, loc="left")
    ax.set_ylabel(eixo)
    if limite:
        ax.set_ylim(0, limite)
    for b, v in zip(barras_, valores):
        ax.annotate(f"{v:g}", (b.get_x() + b.get_width() / 2, b.get_height()), ha="center", va="bottom", fontsize=10)
    salvar(fig, nome)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    SAIDA.mkdir(parents=True, exist_ok=True)
    casos = json.load(open(DADOS / "casos.json", encoding="utf-8"))
    compl = json.load(open(DADOS / "testes_complementares.json", encoding="utf-8"))
    todos = casos + compl
    requisitos = json.load(open(DADOS / "requisitos.json", encoding="utf-8"))
    execucoes, defeitos = ler_csv("execucoes.csv"), ler_csv("defeitos.csv")

    atual = {}
    for e in execucoes:  # resultado atual = execução mais recente de cada caso
        atual[e["caso"]] = e["resultado"]
    resultado = {c["id"]: atual.get(c["id"], "Não executado") for c in todos}
    planejados = len(todos)
    executados = sum(r in ("Aprovado", "Reprovado") for r in resultado.values())
    aprovados = sum(r == "Aprovado" for r in resultado.values())
    reprovados = sum(r == "Reprovado" for r in resultado.values())
    req_exec = [r["id"] for r in requisitos
                if any(r["id"] in c["requisitos"] and resultado[c["id"]] in ("Aprovado", "Reprovado") for c in todos)]
    cand = [c for c in todos if c["automacao"]["candidato"] == "Sim"]
    auto = [c for c in cand if c["automacao"].get("automatizado") == "Sim"]
    sev = Counter(d["severidade"] for d in defeitos)
    sta = Counter(d["status"] for d in defeitos)
    retest = sum(d["retestado"] == "Sim" for d in defeitos)
    reab = sum(d["reaberto"] == "Sim" for d in defeitos)

    m = {
        "casos_planejados": planejados, "casos_executados": executados, "aprovados": aprovados, "reprovados": reprovados,
        "por_resultado": dict(Counter(resultado.values())),
        "percentual_execucao": pct(executados, planejados), "taxa_aprovacao": pct(aprovados, executados),
        "taxa_reprovacao": pct(reprovados, executados),
        "requisitos_no_escopo": len(requisitos), "requisitos_com_teste_executado": len(req_exec),
        "requisitos_sem_teste_executado": [r["id"] for r in requisitos if r["id"] not in req_exec],
        "cobertura_requisitos": pct(len(req_exec), len(requisitos)),
        "casos_planejados_automacao": len(cand), "casos_automatizados": len(auto), "taxa_automacao": pct(len(auto), len(cand)),
        "defeitos_total": len(defeitos), "defeitos_por_severidade": {k: sev.get(k, 0) for k in ("Crítica", "Alta", "Média", "Baixa")},
        "defeitos_por_status": {k: sta.get(k, 0) for k in ("Novo", "Em análise", "Em correção", "Pronto para reteste", "Encerrado", "Reaberto")},
        "defeitos_retestados": retest, "defeitos_reabertos": reab, "taxa_reabertura": pct(reab, retest),
        "execucoes_registradas": len(execucoes),
    }
    (SAIDA / "metricas.json").write_text(json.dumps(m, ensure_ascii=False, indent=2), encoding="utf-8")

    ordem = ["Aprovado", "Reprovado", "Bloqueado", "Não executado"]
    barras("01_resultado_dos_casos.png", f"Resultado atual dos {planejados} casos planejados", ordem,
           [m["por_resultado"].get(k, 0) for k in ordem], [CORES[k] for k in ordem], "Casos")
    barras("02_indicadores_percentuais.png", "Indicadores percentuais (%)",
           ["Execução", "Aprovação", "Reprovação", "Cobertura de\nrequisitos", "Automação"],
           [m["percentual_execucao"], m["taxa_aprovacao"], m["taxa_reprovacao"], m["cobertura_requisitos"], m["taxa_automacao"]],
           ["#3a6ea5", "#2e7d4f", "#b23b3b", "#6a4c93", "#1f8a8a"], "%", 110)
    barras("03_defeitos_por_severidade.png", f"Defeitos por severidade (total: {len(defeitos)})",
           list(m["defeitos_por_severidade"]), list(m["defeitos_por_severidade"].values()),
           ["#7f1d1d", "#b23b3b", "#c98a1b", "#7a8b99"], "Defeitos", max(3, max(m["defeitos_por_severidade"].values()) + 1))
    barras("04_defeitos_por_status.png", f"Defeitos por status (total: {len(defeitos)})",
           [k.replace(" para ", "\npara ") for k in m["defeitos_por_status"]], list(m["defeitos_por_status"].values()),
           "#3a6ea5", "Defeitos", max(3, max(m["defeitos_por_status"].values()) + 1))

    for k, v in m.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
