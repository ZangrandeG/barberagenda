"""
Exporta os defeitos (issues com a etiqueta "defeito") do GitHub para:

  dados/defeitos.csv                          -> usado por gerar_artefatos.py (P05 e métricas)
  entrega/06_DEFEITOS/P07_Defeitos.csv        -> exportação completa (P07)
  entrega/06_DEFEITOS/P07_Relatorio_Defeitos.md -> relatório no modelo do Apêndice G

Requer o GitHub CLI autenticado (gh auth login). Uso:  python scripts/exportar_defeitos.py
"""
import csv
import datetime as dt
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / "entrega" / "06_DEFEITOS"
SEVERIDADE = {"critica": "Crítica", "alta": "Alta", "media": "Média", "baixa": "Baixa"}
PRIORIDADE = {"alta": "Alta", "media": "Média", "baixa": "Baixa"}
STATUS = {"novo": "Novo", "em-analise": "Em análise", "em-correcao": "Em correção",
          "pronto-para-reteste": "Pronto para reteste", "encerrado": "Encerrado", "reaberto": "Reaberto"}
CAMPOS_DADOS = ["id", "issue", "titulo", "requisito", "caso", "execucao", "severidade", "prioridade", "status",
                "data_abertura", "data_encerramento", "retestado", "reaberto", "responsavel"]


def gh():
    caminho = shutil.which("gh") or r"C:\Program Files\GitHub CLI\gh.exe"
    if not Path(caminho).exists() and not shutil.which("gh"):
        sys.exit("GitHub CLI (gh) não encontrado.")
    return caminho


def campo(corpo, nome):
    achado = re.search(rf"\*\*{nome}:\*\*\s*(.+)", corpo or "")
    valor = achado.group(1).strip() if achado else ""
    return "" if "xx" in valor or valor.startswith("<") else valor


def etiqueta(labels, prefixo, mapa):
    for nome in labels:
        if nome.startswith(prefixo):
            return mapa.get(nome[len(prefixo):], nome[len(prefixo):])
    return ""


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    saida = subprocess.run([gh(), "issue", "list", "--label", "defeito", "--state", "all", "--limit", "500", "--json",
                            "number,title,state,labels,createdAt,closedAt,url,body,assignees"],
                           cwd=RAIZ, capture_output=True, text=True, encoding="utf-8", check=True).stdout
    issues = sorted(json.loads(saida), key=lambda i: i["number"])
    linhas = []
    for i in issues:
        labels = [l["name"] for l in i["labels"]]
        status = etiqueta(labels, "status:", STATUS) or ("Encerrado" if i["state"] == "CLOSED" else "Novo")
        reaberto = "Sim" if "historico:reaberto" in labels else "Não"
        linhas.append({
            "id": f"D-{i['number']:02d}", "issue": i["url"], "titulo": i["title"],
            "requisito": campo(i["body"], "Requisito"), "caso": campo(i["body"], "Caso de teste"),
            "execucao": campo(i["body"], "Execução"),
            "severidade": etiqueta(labels, "severidade:", SEVERIDADE), "prioridade": etiqueta(labels, "prioridade:", PRIORIDADE),
            "status": status, "data_abertura": i["createdAt"][:10], "data_encerramento": (i["closedAt"] or "")[:10],
            "retestado": "Sim" if status in ("Encerrado", "Reaberto") or reaberto == "Sim" else "Não",
            "reaberto": reaberto,
            "responsavel": ", ".join(a["login"] for a in i["assignees"]) or campo(i["body"], "Responsável"),
            "_corpo": i["body"] or "",
        })

    with open(RAIZ / "dados" / "defeitos.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS_DADOS, extrasaction="ignore")
        w.writeheader()
        w.writerows(linhas)

    SAIDA.mkdir(parents=True, exist_ok=True)
    with open(SAIDA / "P07_Defeitos.csv", "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS_DADOS, extrasaction="ignore", delimiter=";")
        w.writeheader()
        w.writerows(linhas)

    hoje = dt.date.today().isoformat()
    md = ["# P07 — Registro de defeitos", "",
          f"> Exportado do GitHub Issues em {hoje} por `scripts/exportar_defeitos.py` (etiqueta `defeito`).",
          "> Fonte oficial: https://github.com/ZangrandeG/barberagenda/issues?q=label%3Adefeito", ""]
    if not linhas:
        md += [f"Nenhum defeito registrado até {hoje}.", ""]
    else:
        md += ["| ID | Título | Requisito | Caso | Severidade | Prioridade | Status | Reaberto |", "|---|---|---|---|---|---|---|---|"]
        md += [f"| [{l['id']}]({l['issue']}) | {l['titulo']} | {l['requisito']} | {l['caso']} | {l['severidade']} | "
               f"{l['prioridade']} | {l['status']} | {l['reaberto']} |" for l in linhas]
        for l in linhas:
            md += ["", f"## {l['id']} — {l['titulo']}", "",
                   f"Issue: {l['issue']} — Severidade: {l['severidade']} — Prioridade: {l['prioridade']} — "
                   f"Status: {l['status']} — Aberto em {l['data_abertura']}"
                   + (f", encerrado em {l['data_encerramento']}" if l["data_encerramento"] else ""), "",
                   l["_corpo"].strip(), ""]
    (SAIDA / "P07_Relatorio_Defeitos.md").write_text("\n".join(md), encoding="utf-8")
    print(f"{len(linhas)} defeito(s) exportado(s): dados/defeitos.csv e entrega/06_DEFEITOS/")


if __name__ == "__main__":
    main()
