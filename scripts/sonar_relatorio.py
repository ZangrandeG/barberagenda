"""
Exporta o resultado da última análise do SonarQube (projeto barberagenda) para uma pasta de evidências:
  medidas.json, problemas.json e resumo.md

Uso:  python scripts/sonar_relatorio.py <pasta_destino> [--url http://localhost:9000]
Token: variável SONAR_TOKEN (token de análise/usuário do SonarQube local). Nunca versionar o token.
Ex.:  python scripts/sonar_relatorio.py entrega/11_METRICAS_E_QUALIDADE/sonar_baseline
"""
import argparse
import base64
import datetime as dt
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path

PROJETO = "barberagenda"
METRICAS = ["bugs", "vulnerabilities", "security_hotspots", "code_smells", "coverage", "line_coverage",
            "branch_coverage", "duplicated_lines_density", "duplicated_blocks", "sqale_index", "sqale_debt_ratio",
            "reliability_rating", "security_rating", "sqale_rating", "ncloc", "complexity", "tests"]
NOMES = {
    "bugs": "Bugs", "vulnerabilities": "Vulnerabilidades", "security_hotspots": "Pontos sensíveis de segurança",
    "code_smells": "Code smells", "coverage": "Cobertura (%)", "line_coverage": "Cobertura de linhas (%)",
    "branch_coverage": "Cobertura de ramos (%)", "duplicated_lines_density": "Linhas duplicadas (%)",
    "duplicated_blocks": "Blocos duplicados", "sqale_index": "Dívida técnica (min)",
    "sqale_debt_ratio": "Razão de dívida técnica (%)", "reliability_rating": "Nota de confiabilidade",
    "security_rating": "Nota de segurança", "sqale_rating": "Nota de manutenibilidade",
    "ncloc": "Linhas de código", "complexity": "Complexidade ciclomática", "tests": "Testes de unidade",
}
NOTAS = {"1.0": "A", "2.0": "B", "3.0": "C", "4.0": "D", "5.0": "E"}


def obter(url, caminho, parametros, token):
    req = urllib.request.Request(f"{url}{caminho}?{urllib.parse.urlencode(parametros)}")
    req.add_header("Authorization", "Basic " + base64.b64encode(f"{token}:".encode()).decode())
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser()
    p.add_argument("destino")
    p.add_argument("--url", default="http://localhost:9000")
    args = p.parse_args()
    token = os.environ.get("SONAR_TOKEN") or sys.exit("Defina a variável SONAR_TOKEN.")
    destino = Path(args.destino)
    destino.mkdir(parents=True, exist_ok=True)

    for _ in range(60):  # aguarda o processamento da análise no servidor
        fila = obter(args.url, "/api/ce/component", {"component": PROJETO}, token)
        if not fila.get("queue"):
            break
        time.sleep(2)
    analise = fila.get("current", {})

    medidas = obter(args.url, "/api/measures/component", {"component": PROJETO, "metricKeys": ",".join(METRICAS)}, token)
    problemas = obter(args.url, "/api/issues/search", {"componentKeys": PROJETO, "resolved": "false", "ps": 500}, token)
    (destino / "medidas.json").write_text(json.dumps(medidas, ensure_ascii=False, indent=2), encoding="utf-8")
    (destino / "problemas.json").write_text(json.dumps(problemas, ensure_ascii=False, indent=2), encoding="utf-8")

    portao = obter(args.url, "/api/qualitygates/project_status", {"projectKey": PROJETO}, token)["projectStatus"]
    (destino / "quality_gate.json").write_text(json.dumps(portao, ensure_ascii=False, indent=2), encoding="utf-8")
    valores = {m["metric"]: m.get("value", "—") for m in medidas["component"]["measures"]}
    linhas = [f"# SonarQube — {destino.name}", "",
              f"Exportado em {dt.datetime.now():%Y-%m-%d %H:%M} por `scripts/sonar_relatorio.py`.", "",
              f"- Servidor: SonarQube local {args.url} (Community Build)",
              f"- Análise: {analise.get('submittedAt', '—')} — tarefa {analise.get('id', '—')} — situação {analise.get('status', '—')}",
              f"- Quality gate (Sonar way): **{portao.get('status', '—')}**",
              "", "## Medidas", "", "| Medida | Valor |", "|---|---|"]
    for chave in METRICAS:
        valor = valores.get(chave, "—")
        if chave.endswith("_rating"):
            valor = NOTAS.get(valor, valor)
        linhas.append(f"| {NOMES[chave]} | {valor} |")

    lista = problemas.get("issues", [])
    linhas += ["", f"## Problemas em aberto ({problemas.get('total', len(lista))})", "",
               "| Severidade | Quantidade |", "|---|---|"]
    linhas += [f"| {k} | {v} |" for k, v in Counter(i.get("severity", "—") for i in lista).most_common()]
    linhas += ["", "| Tipo | Quantidade |", "|---|---|"]
    linhas += [f"| {k} | {v} |" for k, v in Counter(i.get("type", "—") for i in lista).most_common()]
    linhas += ["", "| Regra | Quantidade | Exemplo |", "|---|---|---|"]
    por_regra = Counter(i["rule"] for i in lista)
    for regra, qtd in por_regra.most_common():
        ex = next(i for i in lista if i["rule"] == regra)
        arquivo = ex["component"].split(":", 1)[-1]
        linhas.append(f"| `{regra}` | {qtd} | {arquivo}:{ex.get('line', '—')} — {ex['message']} |")
    (destino / "resumo.md").write_text("\n".join(linhas) + "\n", encoding="utf-8")
    print(f"Exportado para {destino}: {len(lista)} problemas em aberto")


if __name__ == "__main__":
    main()
