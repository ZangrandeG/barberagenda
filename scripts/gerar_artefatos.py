"""
Gera o Catálogo de casos de teste (P04, Markdown) e a Matriz de rastreabilidade (P05, XLSX)
a partir dos dados do projeto em dados/:

  requisitos.json, riscos.json, casos.json  -> especificação
  execucoes.csv, defeitos.csv               -> resultados reais (preenchidos nas execuções)

Uso (na raiz do projeto):  python scripts/gerar_artefatos.py

A planilha usa fórmulas (contagens e métricas recalculam quando os dados mudam).
Nenhum resultado é inventado: sem linhas em execucoes.csv, todos os casos aparecem como "Não executado".
"""
import csv
import json
import shutil
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

RAIZ = Path(__file__).resolve().parent.parent
DADOS = RAIZ / "dados"
SAIDA = RAIZ / "entrega" / "04_CASOS_E_RASTREABILIDADE"
P04 = SAIDA / "P04_Catalogo_Casos_de_Teste.md"
P05 = SAIDA / "P05_Matriz_Rastreabilidade.xlsx"

LIMITE_LINHAS = 500  # linhas preparadas com fórmulas nas abas de execuções e defeitos

FONTE = "Arial"
COR_CABECALHO = "5B3A29"
COR_FAIXA = "F3EDE7"
BORDA = Border(*(Side(style="thin", color="D9D0C7"),) * 4)


# ---------------------------------------------------------------- leitura
def ler_json(nome):
    with open(DADOS / nome, encoding="utf-8") as f:
        return json.load(f)


def ler_csv(nome):
    with open(DADOS / nome, encoding="utf-8", newline="") as f:
        return [linha for linha in csv.DictReader(f) if any((v or "").strip() for v in linha.values())]


def validar(requisitos, riscos, casos, execucoes, defeitos):
    ids_req = {r["id"] for r in requisitos}
    ids_risco = {r["id"] for r in riscos}
    ids_caso = [c["id"] for c in casos]
    assert len(ids_caso) == len(set(ids_caso)), "IDs de casos repetidos"
    for c in casos:
        for r in c["requisitos"]:
            assert r in ids_req, f"{c['id']}: requisito desconhecido {r}"
        for r in c["riscos"]:
            assert r in ids_risco, f"{c['id']}: risco desconhecido {r}"
        assert c["automacao"]["candidato"] in ("Sim", "Não"), c["id"]
    for e in execucoes:
        assert e["caso"] in ids_caso, f"{e['execucao']}: caso desconhecido {e['caso']}"
        assert e["resultado"] in ("Aprovado", "Reprovado", "Bloqueado", "Não executado"), e["execucao"]
    for d in defeitos:
        assert d["severidade"] in ("Baixa", "Média", "Alta", "Crítica"), d["id"]


# ---------------------------------------------------------------- P04 (Markdown)
def gerar_p04(requisitos, casos):
    partes = [(DADOS / "P04_introducao.md").read_text(encoding="utf-8").rstrip(), "", "## 3. Casos de teste (Apêndice E)", ""]
    for c in casos:
        a = c["automacao"]
        candidato = a["candidato"] + (f" — {a['nivel']}" if a["candidato"] == "Sim" else "") + f". {a['justificativa']}"
        passos = "<br>".join(f"{i}. {p}" for i, p in enumerate(c["passos"], 1))
        regras = ", ".join(c["regras"]) if c["regras"] else "—"
        partes += [
            f"### {c['id']} — {c['titulo']}",
            "",
            "| Campo | Conteúdo |",
            "|---|---|",
            f"| ID do caso | {c['id']} |",
            f"| Título | {c['titulo']} |",
            f"| Requisito relacionado | {', '.join(c['requisitos'])} (regras: {regras}; riscos: {', '.join(c['riscos'])}) |",
            f"| Nível/tipo | {c['nivel_tipo']} — classificação: {c['classificacao']}; interface: {c['interface']} |",
            f"| Técnica aplicada | {c['tecnica']} |",
            f"| Prioridade | {c['prioridade']} |",
            f"| Pré-condições | {c['precondicoes']} |",
            f"| Dados de entrada | {c['dados']} |",
            f"| Passos numerados | {passos} |",
            f"| Resultado esperado | {c['esperado']} |",
            f"| Candidato à automação | {candidato} |",
            f"| Responsável | {c.get('responsavel', '[PREENCHER PELO GRUPO]')} |",
            "",
        ]

    # Resumos
    por_req = defaultdict(list)
    for c in casos:
        for r in c["requisitos"]:
            por_req[r].append(c["id"])
    partes += ["## 4. Resumo", "", "### 4.1 Casos por requisito", "", "| Requisito | Casos | Quantidade |", "|---|---|---|"]
    for r in requisitos:
        ids = por_req.get(r["id"], [])
        texto = ", ".join(ids) if ids else "— (testes não funcionais no P09, Marco 7)"
        partes.append(f"| {r['id']} | {texto} | {len(ids)} |")

    classes = Counter(c["classificacao"] for c in casos)
    partes += ["", "### 4.2 Casos por classificação", "", "| Classificação | Quantidade |", "|---|---|"]
    partes += [f"| {k} | {v} |" for k, v in sorted(classes.items())]
    prioridades = Counter(c["prioridade"] for c in casos)
    partes += ["", "### 4.3 Casos por prioridade", "", "| Prioridade | Quantidade |", "|---|---|"]
    partes += [f"| {k} | {prioridades.get(k, 0)} |" for k in ("Alta", "Média", "Baixa")]

    candidatos = [c for c in casos if c["automacao"]["candidato"] == "Sim"]
    partes += ["", "### 4.4 Candidatos à automação", "",
               f"{len(candidatos)} de {len(casos)} casos são candidatos à automação (base da taxa de automação, P10).", "",
               "| Nível da automação | Casos |", "|---|---|"]
    por_nivel = defaultdict(list)
    for c in candidatos:
        nivel = c["automacao"]["nivel"]
        for termo, rotulo in (("Unidade", "Unidade (JUnit)"), ("API", "API (Postman)"), ("Interface", "Interface (Selenium)")):
            if termo in nivel:
                por_nivel[rotulo].append(c["id"])
    for nivel in ("Unidade (JUnit)", "API (Postman)", "Interface (Selenium)"):
        partes.append(f"| {nivel} | {', '.join(por_nivel[nivel])} |")
    partes += ["", f"**Total de casos manuais: {len(casos)}** (mínimo do manual: 24).", ""]

    P04.write_text("\n".join(partes), encoding="utf-8")


# ---------------------------------------------------------------- P05 (XLSX)
def estilizar_cabecalho(ws, colunas, larguras):
    for i, (titulo, largura) in enumerate(zip(colunas, larguras), 1):
        cel = ws.cell(row=1, column=i, value=titulo)
        cel.font = Font(name=FONTE, bold=True, color="FFFFFF")
        cel.fill = PatternFill("solid", fgColor=COR_CABECALHO)
        cel.alignment = Alignment(wrap_text=True, vertical="center")
        cel.border = BORDA
        ws.column_dimensions[get_column_letter(i)].width = largura
    ws.freeze_panes = "B2"
    ws.row_dimensions[1].height = 32


def estilizar_corpo(ws, ultima_linha, ultima_coluna):
    for linha in ws.iter_rows(min_row=2, max_row=ultima_linha, max_col=ultima_coluna):
        for cel in linha:
            cel.font = Font(name=FONTE, size=10)
            cel.alignment = Alignment(wrap_text=True, vertical="top")
            cel.border = BORDA
            if cel.row % 2 == 0:
                cel.fill = PatternFill("solid", fgColor=COR_FAIXA)


def gerar_p05(requisitos, riscos, casos, execucoes, defeitos):
    wb = Workbook()

    # --- Requisitos
    ws = wb.active
    ws.title = "Requisitos"
    cols = ["ID", "Tipo", "Prioridade", "Descrição", "Riscos", "Casos", "Casos planejados", "Casos executados",
            "Casos aprovados", "Casos reprovados", "Defeitos abertos", "Situação"]
    estilizar_cabecalho(ws, cols, [9, 13, 10, 55, 14, 30, 11, 11, 11, 11, 11, 24])
    por_req = defaultdict(list)
    for c in casos:
        for r in c["requisitos"]:
            por_req[r].append(c["id"])
    for i, r in enumerate(requisitos, 2):
        ws.append([r["id"], r["tipo"], r["prioridade"], r["descricao"], ", ".join(r["riscos"]),
                   ", ".join(por_req.get(r["id"], [])) or "—"])
        criterio = f'"*"&$A{i}&"*"'
        ws[f"G{i}"] = f"=COUNTIF(Casos!$C:$C,{criterio})"
        ws[f"H{i}"] = f'=COUNTIFS(Casos!$C:$C,{criterio},Casos!$W:$W,"Aprovado")+COUNTIFS(Casos!$C:$C,{criterio},Casos!$W:$W,"Reprovado")'
        ws[f"I{i}"] = f'=COUNTIFS(Casos!$C:$C,{criterio},Casos!$W:$W,"Aprovado")'
        ws[f"J{i}"] = f'=COUNTIFS(Casos!$C:$C,{criterio},Casos!$W:$W,"Reprovado")'
        ws[f"K{i}"] = (f'=COUNTIFS(Defeitos!$D:$D,{criterio},Defeitos!$I:$I,"<>Encerrado")'
                       f'-COUNTIFS(Defeitos!$D:$D,{criterio},Defeitos!$I:$I,"")')
        ws[f"L{i}"] = (f'=IF(G{i}=0,"Sem casos (testes no P09)",IF(H{i}=0,"Não executado",'
                       f'IF(OR(J{i}>0,K{i}>0),"Com falha ou defeito aberto",'
                       f'IF(H{i}<G{i},"Parcialmente executado","Aprovado"))))')
    ultima_req = len(requisitos) + 1
    estilizar_corpo(ws, ultima_req, len(cols))
    ws.auto_filter.ref = f"A1:{get_column_letter(len(cols))}{ultima_req}"

    # --- Riscos
    ws = wb.create_sheet("Riscos")
    cols = ["ID", "Risco", "Probabilidade", "Impacto", "Prioridade", "Resposta / teste", "Requisitos", "Casos"]
    estilizar_cabecalho(ws, cols, [8, 50, 13, 10, 11, 50, 18, 34])
    req_por_risco = defaultdict(list)
    for r in requisitos:
        for k in r["riscos"]:
            req_por_risco[k].append(r["id"])
    casos_por_risco = defaultdict(list)
    for c in casos:
        for k in c["riscos"]:
            casos_por_risco[k].append(c["id"])
    for r in riscos:
        ws.append([r["id"], r["risco"], r["probabilidade"], r["impacto"], r["prioridade"], r["resposta"],
                   ", ".join(req_por_risco[r["id"]]), ", ".join(casos_por_risco[r["id"]]) or "—"])
    estilizar_corpo(ws, len(riscos) + 1, len(cols))

    # --- Casos
    ws = wb.create_sheet("Casos")
    cols = ["ID", "Título", "Requisito(s)", "Risco(s)", "Regra(s)", "Nível/tipo", "Técnica", "Classificação",
            "Prioridade", "Interface", "Pré-condições", "Dados de entrada", "Passos", "Resultado esperado",
            "Candidato à automação", "Nível da automação", "Justificativa", "Automatizado", "Teste automatizado",
            "Responsável", "Execuções", "Última execução", "Resultado atual"]
    estilizar_cabecalho(ws, cols, [8, 40, 14, 12, 14, 20, 30, 12, 10, 11, 35, 45, 60, 55, 11, 30, 40, 12, 30, 16, 10, 12, 16])
    for i, c in enumerate(casos, 2):
        a = c["automacao"]
        ws.append([c["id"], c["titulo"], ", ".join(c["requisitos"]), ", ".join(c["riscos"]),
                   ", ".join(c["regras"]) or "—", c["nivel_tipo"], c["tecnica"], c["classificacao"], c["prioridade"],
                   c["interface"], c["precondicoes"], c["dados"],
                   "\n".join(f"{n}. {p}" for n, p in enumerate(c["passos"], 1)), c["esperado"],
                   a["candidato"], a["nivel"], a["justificativa"], a.get("automatizado", "Não"),
                   a.get("referencia", ""), c.get("responsavel", "[PREENCHER]")])
        ws[f"U{i}"] = f"=COUNTIF('Execuções'!$B:$B,$A{i})"
        ws[f"V{i}"] = f"=IFERROR(INDEX('Execuções'!$A:$A,MATCH($A{i}&\"|ÚLTIMA\",'Execuções'!$J:$J,0)),\"—\")"
        ws[f"W{i}"] = f"=IFERROR(INDEX('Execuções'!$F:$F,MATCH($A{i}&\"|ÚLTIMA\",'Execuções'!$J:$J,0)),\"Não executado\")"
    ultima_caso = len(casos) + 1
    estilizar_corpo(ws, ultima_caso, len(cols))
    ws.auto_filter.ref = f"A1:{get_column_letter(len(cols))}{ultima_caso}"
    for linha in range(2, ultima_caso + 1):
        ws.row_dimensions[linha].height = 90

    # --- Execuções (Apêndice F)
    ws = wb.create_sheet("Execuções")
    cols = ["Execução", "Caso", "Data", "Versão", "Executor", "Resultado", "Evidência", "Defeito", "Observações",
            "Chave (fórmula)"]
    estilizar_cabecalho(ws, cols, [10, 9, 12, 20, 22, 14, 45, 10, 45, 16])
    for e in execucoes:
        ws.append([e["execucao"], e["caso"], e["data"], e["versao"], e["executor"], e["resultado"],
                   e["evidencia"], e["defeito"], e["observacoes"]])
    for linha in range(2, LIMITE_LINHAS + 1):
        ws[f"J{linha}"] = f'=IF(B{linha}="","",B{linha}&IF(COUNTIF(B{linha + 1}:B${LIMITE_LINHAS + 1},B{linha})=0,"|ÚLTIMA",""))'
    estilizar_corpo(ws, max(len(execucoes) + 1, 2), len(cols))
    resultado = DataValidation(type="list", formula1='"Aprovado,Reprovado,Bloqueado,Não executado"', allow_blank=True)
    ws.add_data_validation(resultado)
    resultado.add(f"F2:F{LIMITE_LINHAS}")

    # --- Defeitos (Apêndice G, resumo)
    ws = wb.create_sheet("Defeitos")
    cols = ["ID", "Issue (GitHub)", "Título", "Requisito", "Caso", "Execução", "Severidade", "Prioridade", "Status",
            "Data de abertura", "Data de encerramento", "Retestado", "Reaberto", "Responsável"]
    estilizar_cabecalho(ws, cols, [8, 36, 45, 10, 9, 10, 11, 10, 18, 12, 12, 10, 10, 18])
    for d in defeitos:
        ws.append([d["id"], d["issue"], d["titulo"], d["requisito"], d["caso"], d["execucao"], d["severidade"],
                   d["prioridade"], d["status"], d["data_abertura"], d["data_encerramento"], d["retestado"],
                   d["reaberto"], d["responsavel"]])
    estilizar_corpo(ws, max(len(defeitos) + 1, 2), len(cols))

    # --- Rastreabilidade (Apêndice H)
    ws = wb.create_sheet("Rastreabilidade")
    cols = ["Requisito", "Risco", "Caso(s)", "Execução(ões)", "Defeito(s)", "Situação"]
    estilizar_cabecalho(ws, cols, [10, 16, 40, 40, 20, 28])
    exec_por_caso = defaultdict(list)
    for e in execucoes:
        exec_por_caso[e["caso"]].append(e["execucao"])
    def_por_req = defaultdict(list)
    for d in defeitos:
        for r in d["requisito"].replace(";", ",").split(","):
            if r.strip():
                def_por_req[r.strip()].append(d["id"])
    for i, r in enumerate(requisitos, 2):
        ids = por_req.get(r["id"], [])
        execs = [x for cid in ids for x in exec_por_caso[cid]]
        ws.append([r["id"], ", ".join(r["riscos"]), ", ".join(ids) or "— (P09)", ", ".join(execs) or "—",
                   ", ".join(def_por_req[r["id"]]) or "—"])
        ws[f"F{i}"] = f"=Requisitos!L{i}"
    estilizar_corpo(ws, len(requisitos) + 1, len(cols))

    # --- Métricas (seção 9.13 do manual)
    ws = wb.create_sheet("Métricas")
    estilizar_cabecalho(ws, ["Indicador", "Valor", "Cálculo (seção 9.13)", "Fonte dos dados"], [34, 14, 48, 46])
    caso_rng = f"Casos!$W$2:$W${ultima_caso}"
    linhas = [
        ("Casos planejados", f"=COUNTA(Casos!$A$2:$A${ultima_caso})", "Quantidade de casos no catálogo", "Aba Casos"),
        ("Casos executados", f'=COUNTIF({caso_rng},"Aprovado")+COUNTIF({caso_rng},"Reprovado")',
         "Casos cujo resultado atual é Aprovado ou Reprovado", "Aba Casos (resultado da execução mais recente)"),
        ("Casos aprovados", f'=COUNTIF({caso_rng},"Aprovado")', "Resultado atual = Aprovado", "Aba Casos"),
        ("Casos reprovados", f'=COUNTIF({caso_rng},"Reprovado")', "Resultado atual = Reprovado", "Aba Casos"),
        ("Percentual de execução", '=IF(B2=0,"—",B3/B2)', "casos executados / casos planejados × 100", "Linhas 2 e 3"),
        ("Taxa de aprovação", '=IF(B3=0,"—",B4/B3)', "casos aprovados / casos executados × 100", "Linhas 3 e 4"),
        ("Taxa de reprovação", '=IF(B3=0,"—",B5/B3)', "casos reprovados / casos executados × 100", "Linhas 3 e 5"),
        ("Requisitos no escopo", f"=COUNTA(Requisitos!$A$2:$A${ultima_req})", "Quantidade de requisitos", "Aba Requisitos"),
        ("Requisitos com teste executado", f'=COUNTIF(Requisitos!$H$2:$H${ultima_req},">0")',
         "Requisitos com ao menos um caso executado", "Aba Requisitos"),
        ("Cobertura de requisitos", '=IF(B9=0,"—",B10/B9)', "requisitos com teste executado / requisitos no escopo × 100", "Linhas 9 e 10"),
        ("Casos planejados para automação", f'=COUNTIF(Casos!$O$2:$O${ultima_caso},"Sim")', "Candidato à automação = Sim", "Aba Casos"),
        ("Casos automatizados", f'=COUNTIFS(Casos!$O$2:$O${ultima_caso},"Sim",Casos!$R$2:$R${ultima_caso},"Sim")',
         "Candidatos com Automatizado = Sim", "Aba Casos"),
        ("Taxa de automação", '=IF(B12=0,"—",B13/B12)', "casos automatizados / casos planejados para automação × 100", "Linhas 12 e 13"),
        ("Defeitos — severidade Crítica", '=COUNTIF(Defeitos!$G:$G,"Crítica")', "contagem por categoria", "Aba Defeitos"),
        ("Defeitos — severidade Alta", '=COUNTIF(Defeitos!$G:$G,"Alta")', "contagem por categoria", "Aba Defeitos"),
        ("Defeitos — severidade Média", '=COUNTIF(Defeitos!$G:$G,"Média")', "contagem por categoria", "Aba Defeitos"),
        ("Defeitos — severidade Baixa", '=COUNTIF(Defeitos!$G:$G,"Baixa")', "contagem por categoria", "Aba Defeitos"),
    ]
    for status in ("Novo", "Em análise", "Em correção", "Pronto para reteste", "Encerrado", "Reaberto"):
        linhas.append((f"Defeitos — status {status}", f'=COUNTIF(Defeitos!$I:$I,"{status}")', "contagem por estado", "Aba Defeitos"))
    n = len(linhas) + 2
    linhas += [
        ("Defeitos retestados", '=COUNTIF(Defeitos!$L:$L,"Sim")', "Retestado = Sim", "Aba Defeitos"),
        ("Defeitos reabertos", '=COUNTIF(Defeitos!$M:$M,"Sim")', "Reaberto = Sim", "Aba Defeitos"),
        ("Taxa de reabertura", f'=IF(B{n}=0,"—",B{n + 1}/B{n})', "defeitos reabertos / defeitos retestados × 100", f"Linhas {n} e {n + 1}"),
    ]
    for indicador, formula, calculo, fonte in linhas:
        ws.append([indicador, formula, calculo, fonte])
    ultima_metrica = len(linhas) + 1
    estilizar_corpo(ws, ultima_metrica, 4)
    for linha in range(2, ultima_metrica + 1):
        if ws[f"A{linha}"].value.startswith(("Percentual", "Taxa", "Cobertura")):
            ws[f"B{linha}"].number_format = "0.0%"
            ws[f"A{linha}"].font = Font(name=FONTE, size=10, bold=True)
    nota = ultima_metrica + 2
    ws[f"A{nota}"] = "Como esta planilha é mantida"
    ws[f"A{nota}"].font = Font(name=FONTE, bold=True)
    textos = [
        "Gerada por scripts/gerar_artefatos.py a partir de dados/*.json (especificação) e dados/*.csv (execuções e defeitos reais).",
        "Para registrar resultados: acrescente linhas em dados/execucoes.csv e dados/defeitos.csv e rode o script novamente.",
        "Resultado atual de um caso = resultado da execução mais recente (última linha do caso na aba Execuções).",
        "Casos executados = resultado atual Aprovado ou Reprovado (Bloqueado e Não executado não contam como executados).",
        "Requisitos não funcionais (RNF) recebem testes no P09 (Marco 7); até lá aparecem como 'Sem casos'.",
    ]
    for k, texto in enumerate(textos, nota + 1):
        ws[f"A{k}"] = texto
        ws[f"A{k}"].font = Font(name=FONTE, size=10)

    wb.calculation.fullCalcOnLoad = True
    wb.save(P05)
    recalcular_com_libreoffice(P05)


def recalcular_com_libreoffice(arquivo):
    """Grava os valores calculados das fórmulas (para pré-visualizações que não calculam, como a do Drive).
    As fórmulas são mantidas. Sem LibreOffice instalado, o Excel calcula ao abrir o arquivo."""
    candidatos = [Path(r"C:\Program Files\LibreOffice\program\soffice.exe"), Path("/usr/bin/soffice"),
                  Path("/usr/bin/libreoffice")]
    soffice = next((c for c in candidatos if c.exists()), None)
    if soffice is None:
        print("LibreOffice não encontrado: valores serão calculados ao abrir no Excel.")
        return
    with tempfile.TemporaryDirectory() as pasta:
        subprocess.run([str(soffice), "--headless", "--calc", "--convert-to", "xlsx", "--outdir", pasta, str(arquivo)],
                       check=True, capture_output=True, timeout=180)
        shutil.copyfile(Path(pasta) / arquivo.name, arquivo)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    requisitos = ler_json("requisitos.json")
    riscos = ler_json("riscos.json")
    casos = ler_json("casos.json")
    execucoes = ler_csv("execucoes.csv")
    defeitos = ler_csv("defeitos.csv")
    validar(requisitos, riscos, casos, execucoes, defeitos)
    SAIDA.mkdir(parents=True, exist_ok=True)
    gerar_p04(requisitos, casos)
    gerar_p05(requisitos, riscos, casos, execucoes, defeitos)
    print(f"P04: {P04.relative_to(RAIZ)} ({len(casos)} casos)")
    print(f"P05: {P05.relative_to(RAIZ)} ({len(requisitos)} requisitos, {len(riscos)} riscos, "
          f"{len(execucoes)} execuções, {len(defeitos)} defeitos)")


if __name__ == "__main__":
    main()
