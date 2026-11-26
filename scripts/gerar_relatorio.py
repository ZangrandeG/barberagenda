"""
Gera o relatório final (P12) em Markdown, DOCX e PDF a partir de:
  - scripts/relatorio/P12_modelo.md  (texto do relatório, escrito pelo grupo, com marcadores {{...}});
  - dados/ (requisitos, riscos, casos, execuções, defeitos) e evidências reais em entrega/;
  - P02, P03, P09 e P11 (tabelas reaproveitadas, sem cópia manual).

Numera tabelas e figuras, acrescenta "Fonte", monta sumário, lista de figuras e lista de tabelas com o número
da página (duas passagens: a primeira gera o PDF e localiza as páginas; a segunda escreve os números).

Uso:  python scripts/gerar_relatorio.py
Requer: pandoc e LibreOffice (caminhos em PANDOC/SOFFICE ou variáveis de ambiente), pdftotext, matplotlib.
"""
import csv
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
from collections import Counter, OrderedDict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "relatorio"))
import modelo_docx  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
ENTREGA = RAIZ / "entrega"
PASTA = ENTREGA / "13_RELATORIO_FINAL"
FIGURAS = PASTA / "figuras"
MODELO = RAIZ / "scripts" / "relatorio" / "P12_modelo.md"
NOME = "P12_Relatorio_Final"
PANDOC = os.environ.get("PANDOC", r"C:\Users\Admin\AppData\Local\Pandoc\pandoc.exe")
SOFFICE = os.environ.get("SOFFICE", r"C:\Program Files\LibreOffice\program\soffice.exe")
PDFTOTEXT = os.environ.get("PDFTOTEXT", shutil.which("pdftotext") or "pdftotext")
FONTE_PADRAO = "Fonte: Elaborado pelos autores (2026)."


# --------------------------------------------------------------------------- leitura dos dados
def ler_json(caminho):
    return json.loads(Path(caminho).read_text(encoding="utf-8"))


def ler_csv(caminho):
    with open(caminho, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def ler_texto(caminho):
    dados = Path(caminho).read_bytes()
    for cod in ("utf-8", "cp1252"):
        try:
            return dados.decode(cod)
        except UnicodeDecodeError:
            continue
    return dados.decode("utf-8", errors="replace")


REQ = ler_json(RAIZ / "dados/requisitos.json")
RIS = ler_json(RAIZ / "dados/riscos.json")
CASOS = ler_json(RAIZ / "dados/casos.json")
COMPL = ler_json(RAIZ / "dados/testes_complementares.json")
EXEC = ler_csv(RAIZ / "dados/execucoes.csv")
DEF = ler_csv(RAIZ / "dados/defeitos.csv")
MET = ler_json(ENTREGA / "11_METRICAS_E_QUALIDADE/metricas/metricas.json")
TODOS = CASOS + COMPL
POR_ID = {c["id"]: c for c in TODOS}
ATUAL = {}
for _e in EXEC:
    ATUAL[_e["caso"]] = _e
RESULTADO = {c["id"]: (ATUAL[c["id"]]["resultado"] if c["id"] in ATUAL else "Não executado") for c in TODOS}


def br(numero, casas=1):
    return f"{numero:.{casas}f}".replace(".", ",")


def data_br(iso):
    a, m, d = iso[:10].split("-")
    return f"{d}/{m}/{a}"


def celula(texto):
    return str(texto).replace("|", "\\|").replace("\n", " ").strip()


def tabela(cabecalho, linhas):
    """Tabela pipe do pandoc. As larguras das colunas são recalculadas no pós-processamento."""
    saida = ["| " + " | ".join(cabecalho) + " |", "|" + "---|" * len(cabecalho)]
    saida += ["| " + " | ".join(celula(c) for c in linha) + " |" for linha in linhas]
    return "\n".join(saida)


def secao_markdown(arquivo, titulo):
    """Linhas da seção de um documento Markdown (do título indicado até o próximo título de mesmo nível ou superior)."""
    linhas = ler_texto(arquivo).splitlines()
    for i, l in enumerate(linhas):
        m = re.match(r"^(#+)\s+(.*)$", l)
        if m and m.group(2).strip().startswith(titulo):
            nivel, corpo = len(m.group(1)), []
            for l2 in linhas[i + 1:]:
                m2 = re.match(r"^(#+)\s", l2)
                if m2 and len(m2.group(1)) <= nivel:
                    break
                corpo.append(l2)
            return corpo
    raise KeyError(f"seção '{titulo}' não encontrada em {arquivo}")


def tabelas_da_secao(arquivo, titulo):
    """Tabelas pipe de uma seção; blocos de linhas '|' sem linha separadora são unidos à tabela anterior."""
    tabelas, atual = [], []
    for l in secao_markdown(arquivo, titulo) + [""]:
        if l.startswith("|"):
            atual.append(l)
        elif atual:
            if tabelas and not any(re.match(r"^\|\s*:?-{3,}", x) for x in atual):
                tabelas[-1] += atual
            else:
                tabelas.append(atual)
            atual = []
    return ["\n".join(t) for t in tabelas]


def linhas_tabela(md):
    linhas = [l for l in md.splitlines() if l.startswith("|")]
    def partes(l):
        return [c.strip() for c in re.split(r"(?<!\\)\|", l.strip())[1:-1]]
    return partes(linhas[0]), [partes(l) for l in linhas[2:]]


def sem_negrito(texto):
    return re.sub(r"\*\*(.*?)\*\*", r"\1", texto)


# --------------------------------------------------------------------------- figuras geradas com dados reais
def figuras_geradas():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "axes.spines.top": False, "axes.spines.right": False})
    FIGURAS.mkdir(parents=True, exist_ok=True)

    # 1) tempos de resposta do TNF-01 (as 60 medições)
    amostras = ler_csv(ENTREGA / "10_ACEITACAO_NAO_FUNCIONAIS/evidencias/TNF-01_desempenho_amostras.csv")
    ops = list(OrderedDict.fromkeys(a["operacao"] for a in amostras))
    fig, ax = plt.subplots(figsize=(9, 3.6))
    for i, op in enumerate(ops):
        valores = [float(a["tempo_ms"]) for a in amostras if a["operacao"] == op]
        ax.plot(range(1, len(valores) + 1), valores, marker="o", ms=4, lw=1.4, label=op, color=["#3a6ea5", "#5b3a29"][i])
    ax.axhline(500, color="#b23b3b", lw=1.2, ls="--")
    ax.text(30.4, 500, "critério p95 < 500 ms", va="center", ha="left", fontsize=9, color="#b23b3b")
    ax.set_yscale("log")
    ax.set_ylim(2, 1000)
    ax.set_xlabel("Medição")
    ax.set_ylabel("Tempo (ms, escala log)")
    ax.legend(frameon=False, fontsize=9, loc="upper left")
    fig.savefig(FIGURAS / "tnf01_tempos.png", dpi=170, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    # 2) resultado atual dos casos por requisito
    cores = {"Aprovado": "#2e7d4f", "Reprovado": "#b23b3b", "Bloqueado": "#c98a1b", "Não executado": "#9e9e9e"}
    ids = [r["id"] for r in REQ]
    cont = {k: [sum(1 for c in TODOS if r in c["requisitos"] and RESULTADO[c["id"]] == k) for r in ids] for k in cores}
    fig, ax = plt.subplots(figsize=(9, 3.8))
    base = [0] * len(ids)
    for k, cor in cores.items():
        ax.bar(ids, cont[k], bottom=base, color=cor, label=k, width=0.65)
        base = [a + b for a, b in zip(base, cont[k])]
    ax.set_ylabel("Casos e testes")
    ax.legend(frameon=False, fontsize=9, ncol=4, loc="upper right")
    ax.set_ylim(0, max(base) + 2)
    plt.xticks(rotation=45, ha="right")
    fig.savefig(FIGURAS / "resultado_por_requisito.png", dpi=170, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    # 3) capturas reais do Selenium na largura de celular: Chrome e Firefox lado a lado
    from PIL import Image
    cap = ENTREGA / "10_ACEITACAO_NAO_FUNCIONAIS/evidencias/TNF-07_compatibilidade/capturas"
    imgs = [Image.open(cap / f"AgendamentoE2ETest_deveAgendarHorarioPelaTela_{n}_375x667_OK.png").convert("RGB") for n in ("chrome", "firefox")]
    altura = max(i.height for i in imgs)
    folga = 40
    tela = Image.new("RGB", (sum(i.width for i in imgs) + folga, altura), "white")
    x = 0
    for img in imgs:
        tela.paste(img, (x, 0))
        x += img.width + folga
    tela.save(FIGURAS / "compat_celular.png")


# --------------------------------------------------------------------------- blocos gerados ({{NOME}})
def b_requisitos_rf():
    cab, linhas = linhas_tabela(tabelas_da_secao(ENTREGA / "02_REQUISITOS_ESCOPO_RISCOS/P02_Requisitos_Escopo_Riscos.md", "1.1 Requisitos")[0])
    return tabela(["ID", "Descrição verificável", "Prior.", "Critério de aceitação"], [[l[0], l[1], l[3], l[4]] for l in linhas])


def b_requisitos_rnf():
    cab, linhas = linhas_tabela(tabelas_da_secao(ENTREGA / "02_REQUISITOS_ESCOPO_RISCOS/P02_Requisitos_Escopo_Riscos.md", "1.2 Requisitos")[0])
    return tabela(["ID", "Descrição", "Prior.", "Critério de aceitação"], [[l[0], l[1], l[3], l[4]] for l in linhas])


def b_fora_escopo():
    cab, linhas = linhas_tabela(tabelas_da_secao(ENTREGA / "02_REQUISITOS_ESCOPO_RISCOS/P02_Requisitos_Escopo_Riscos.md", "2.2 Fora")[0])
    return tabela(["Item fora do escopo", "Motivo"], [[l[0].replace("~~", ""), l[1]] for l in linhas if not l[0].startswith("~~")])


def b_riscos():
    cab, linhas = linhas_tabela(tabelas_da_secao(ENTREGA / "02_REQUISITOS_ESCOPO_RISCOS/P02_Requisitos_Escopo_Riscos.md", "3. Matriz")[0])
    linhas.sort(key=lambda l: l[0])
    return tabela(["ID", "Risco", "Req.", "Prob.", "Impacto", "Prior.", "Resposta / teste"], [[sem_negrito(x) for x in l] for l in linhas])


def b_tabela_doc(arquivo, titulo, indice=0, colunas=None):
    md = tabelas_da_secao(ENTREGA / arquivo, titulo)[indice]
    cab, linhas = linhas_tabela(md)
    linhas = [l for l in linhas if not any("[PREENCHER" in c for c in l)]  # pendências humanas ficam no Apêndice H
    if colunas:
        cab = [cab[i] for i in colunas]
        linhas = [[l[i] for i in colunas] for l in linhas]
    return tabela(cab, linhas)


def tecnica_principal(t):
    t = t.lower()
    for chave, nome in (("tabela de decisão", "Tabela de decisão"), ("transição de estados", "Transição de estados"),
                        ("valor limite", "Análise de valor limite"), ("particionamento", "Particionamento de equivalência"),
                        ("caso de uso", "Caso de uso (fluxo principal)")):
        if chave in t:
            return nome
    return t


def b_casos_por_tecnica():
    grupos = OrderedDict()
    for c in CASOS:
        grupos.setdefault(tecnica_principal(c["tecnica"]), []).append(c["id"])
    linhas = sorted(grupos.items(), key=lambda kv: -len(kv[1]))
    return tabela(["Técnica (principal)", "Casos", "Qtd."], [[k, ", ".join(v), len(v)] for k, v in linhas])


def b_casos_por_classificacao():
    grupos = OrderedDict()
    for c in CASOS:
        grupos.setdefault(c["classificacao"], []).append(c["id"])
    return tabela(["Classificação", "Casos", "Qtd."], [[k, ", ".join(v), len(v)] for k, v in sorted(grupos.items(), key=lambda kv: -len(kv[1]))])


def b_casos_por_requisito():
    linhas = []
    for r in REQ:
        cs = [c for c in CASOS if r["id"] in c["requisitos"]]
        cp = [c for c in COMPL if r["id"] in c["requisitos"]]
        linhas.append([r["id"], ", ".join(c["id"] for c in cs) or "—", ", ".join(c["id"] for c in cp) or "—", len(cs) + len(cp)])
    return tabela(["Requisito", "Casos manuais (P04)", "Aceitação e não funcionais (P09)", "Total"], linhas)


def b_execucoes_ciclo():
    linhas = []
    for e in EXEC:
        c = POR_ID[e["caso"]]
        if not e["caso"].startswith("CT-"):
            continue
        linhas.append([e["execucao"], e["caso"], c["titulo"], e["versao"].split(" ")[0], e["resultado"], e["defeito"] or "—"])
    return tabela(["Exec.", "Caso", "Título", "Versão", "Resultado", "Defeito"], linhas)


def obtidos(execucao, caso):
    """Linhas de verificação ([OK]/[FALHOU]/[BLOQUEADO]) da transcrição da execução, sem as respostas completas."""
    arq = ENTREGA / "05_EXECUCAO_MANUAL/evidencias" / f"{execucao}_{caso}_{data_iso(execucao)}.txt"
    if not arq.exists():
        return []
    saida = []
    for l in ler_texto(arq).splitlines():
        m = re.match(r"^\[(OK|FALHOU|BLOQUEADO|INFO)\]\s*(.*)$", l.strip())
        if m:
            saida.append(f"[{m.group(1)}] {m.group(2)}")
    return saida


def data_iso(execucao):
    return next(e["data"] for e in EXEC if e["execucao"] == execucao)


def b_apendice_execucoes():
    linhas = []
    for e in EXEC:
        c = POR_ID[e["caso"]]
        evid = ", ".join(Path(x).name for x in e["evidencia"].split())
        verif = obtidos(e["execucao"], e["caso"])
        obtido = "; ".join(v.replace("[OK] ", "✓ ") for v in verif) if verif else (e["observacoes"] or "—")
        if verif and e["observacoes"]:
            obtido += f". Obs.: {e['observacoes']}"
        linhas.append([f"**{e['execucao']}**", e["caso"], e["versao"].split(" ")[0], f"**{e['resultado']}**", obtido])
    return tabela(["Exec.", "Caso", "Versão", "Resultado", "Resultado obtido (verificações registradas na transcrição)"], linhas)


def b_catalogo():
    partes = []
    for c in CASOS:
        a = c["automacao"]
        linhas = [["Rastreabilidade", f"Requisito {', '.join(c['requisitos'])} · risco {', '.join(c['riscos'])} · regra {', '.join(c['regras']) or '—'}"],
                  ["Classificação", f"{c['nivel_tipo']} · {c['classificacao']} · prioridade {c['prioridade']} · interface: {c['interface']}"],
                  ["Técnica", c["tecnica"]],
                  ["Pré-condições", c["precondicoes"]], ["Dados de teste", c["dados"]],
                  ["Passos", " ".join(f"{i}. {p}" for i, p in enumerate(c["passos"], 1))], ["Resultado esperado", c["esperado"]],
                  ["Automação", f"{a['candidato']}" + (f" – {a.get('referencia', '')}" if a["candidato"] == "Sim" else f" – {a.get('justificativa', '')}")],
                  ["Responsável · resultado", f"{c['responsavel']} · último resultado: **{RESULTADO[c['id']]}**"
                   + (f" ({ATUAL[c['id']]['execucao']})" if c["id"] in ATUAL else "")]]
        partes.append(f"### {c['id']} – {c['titulo']}\n\n" + tabela(["Campo", "Conteúdo"], linhas) + "\n")
    return "\n".join(partes)


def b_matriz():
    linhas = []
    for r in REQ:
        for c in [c for c in TODOS if r["id"] in c["requisitos"]]:
            e = ATUAL.get(c["id"])
            linhas.append([r["id"], ", ".join(c["riscos"]) or "—", c["id"], e["execucao"] if e else "—", RESULTADO[c["id"]],
                           (e["defeito"] if e and e["defeito"] else "—")])
    return tabela(["Requisito", "Riscos", "Caso", "Última execução", "Resultado", "Defeito"], linhas)


def situacao_requisito(rid):
    res = [RESULTADO[c["id"]] for c in TODOS if rid in c["requisitos"]]
    if any(r == "Reprovado" for r in res):
        return "Com falhas"
    if res and all(r == "Aprovado" for r in res):
        return "Atendido"
    if any(r == "Aprovado" for r in res):
        return "Atendido no que foi executado"
    return "Sem teste executado"


def b_rastreabilidade_resumo():
    linhas = []
    for r in REQ:
        cs = [c for c in TODOS if r["id"] in c["requisitos"]]
        cont = Counter(RESULTADO[c["id"]] for c in cs)
        linhas.append([r["id"], ", ".join(r["riscos"]), len(cs), cont.get("Aprovado", 0) + cont.get("Reprovado", 0), cont.get("Aprovado", 0),
                       cont.get("Reprovado", 0), cont.get("Bloqueado", 0) + cont.get("Não executado", 0),
                       sum(1 for d in DEF if d["requisito"] == r["id"]), situacao_requisito(r["id"])])
    return tabela(["Req.", "Riscos", "Casos", "Exec.", "Aprov.", "Reprov.", "Pend.", "Defeitos", "Situação"], linhas)


def b_metricas():
    m = MET
    sev = m["defeitos_por_severidade"]
    sta = m["defeitos_por_status"]
    linhas = [
        ["1. Percentual de execução", f"executados / planejados = {m['casos_executados']} / {m['casos_planejados']}", f"{br(m['percentual_execucao'])}%"],
        ["2. Taxa de aprovação", f"aprovados / executados = {m['aprovados']} / {m['casos_executados']}", f"{br(m['taxa_aprovacao'])}%"],
        ["3. Taxa de reprovação", f"reprovados / executados = {m['reprovados']} / {m['casos_executados']}", f"{br(m['taxa_reprovacao'])}%"],
        ["4. Cobertura de requisitos", f"requisitos com teste executado / requisitos = {m['requisitos_com_teste_executado']} / {m['requisitos_no_escopo']}", f"{br(m['cobertura_requisitos'])}%"],
        ["5. Taxa de automação", f"automatizados / planejados para automação = {m['casos_automatizados']} / {m['casos_planejados_automacao']}", f"{br(m['taxa_automacao'])}%"],
        ["6. Defeitos por severidade", "contagem por categoria", " · ".join(f"{k} {v}" for k, v in sev.items())],
        ["7. Defeitos por status", "contagem por estado", " · ".join(f"{k} {v}" for k, v in sta.items())],
        ["8. Taxa de reabertura", f"reabertos / retestados = {m['defeitos_reabertos']} / {m['defeitos_retestados']}",
         "não se aplica" if m["defeitos_retestados"] == 0 else f"{br(m['taxa_reabertura'])}%"],
    ]
    return tabela(["Indicador", "Cálculo", "Valor"], linhas)


def contar_testes_log(arquivo):
    """Lê as linhas 'Tests run: N ... -- in <nome>' de um log do Maven (Surefire)."""
    linhas = []
    total = None
    for l in ler_texto(arquivo).splitlines():
        l = re.sub(r"\x1b\[[0-9;]*m", "", l)
        m = re.search(r"Tests run: (\d+), Failures: (\d+), Errors: (\d+), Skipped: (\d+)(?:, Time elapsed: ([\d.,]+) s)?(?: -+ in (.+))?", l)
        if not m:
            continue
        if m.group(6):
            linhas.append((m.group(6).strip(), int(m.group(1)), int(m.group(2)) + int(m.group(3)), m.group(5)))
        else:
            total = (int(m.group(1)), int(m.group(2)) + int(m.group(3)))
    return linhas, total


def b_unidade_classes():
    linhas, total = contar_testes_log(ENTREGA / "12_TDD_CICD_MELHORIA/regressao_v1.2.0/unidade_integracao_mvnw_verify.log")
    saida = [[n, q, f] for n, q, f, _ in linhas]
    saida.append(["**Total**", f"**{total[0]}**", f"**{total[1]}**"])
    return tabela(["Classe de teste (descrição no @DisplayName)", "Execuções", "Falhas"], saida)


def b_e2e_classes():
    linhas, total = contar_testes_log(ENTREGA / "12_TDD_CICD_MELHORIA/regressao_v1.2.0/e2e_chrome_1366x768.log")
    saida = [[n, q, f] for n, q, f, _ in linhas]
    saida.append(["**Total (Chrome, 1366×768)**", f"**{total[0]}**", f"**{total[1]}**"])
    return tabela(["Classe de teste", "Execuções", "Falhas"], saida)


def metodos_java(pasta):
    """(classe, método, @DisplayName, parametrizado) de cada teste em src/test/java/br/com/barberagenda/<pasta>.
    As anotações do método são o trecho entre o fim da instrução anterior e a palavra 'void'."""
    corrigido = []
    for arq in sorted((RAIZ / "src/test/java/br/com/barberagenda" / pasta).glob("*Test.java")):
        txt = ler_texto(arq)
        anterior = 0
        for m in re.finditer(r"\bvoid\s+(\w+)\s*\(", txt):
            # trecho desde o método anterior: corpos de método não têm anotações, então as anotações
            # encontradas aqui são as deste método (anotações como @CsvSource({...}) podem ter chaves)
            bloco, anterior = txt[anterior:m.start()], m.end()
            if not re.search(r"@(Test|ParameterizedTest)\b", bloco):
                continue
            dn = re.findall(r'@DisplayName\("((?:[^"\\]|\\.)*)"\)', bloco)
            corrigido.append((arq.stem, m.group(1), dn[-1].replace('\\"', '"') if dn else m.group(1),
                              "sim" if "@ParameterizedTest" in bloco else "não"))
    return corrigido


def b_lista_junit():
    linhas = [[f"{c}.{m}", d, p] for c, m, d, p in metodos_java("unit") + metodos_java("integration")]
    return tabela(["Classe.método", "Descrição (@DisplayName: caso e requisito)", "Param."], linhas)


def b_lista_selenium():
    linhas = [[f"{c}.{m}", d] for c, m, d, p in metodos_java("e2e")]
    return tabela(["Classe.método", "Descrição (@DisplayName)"], linhas)


def postman_itens():
    col = ler_json(ENTREGA / "08_INTEGRACAO_API/BarberAgenda.postman_collection.json")
    saida = []

    def percorrer(itens, pasta=""):
        for i in itens:
            if "item" in i:
                percorrer(i["item"], i["name"])
            else:
                testes = [re.search(r"pm\.test\(\s*['\"](.+?)['\"]", l) for e in i.get("event", []) if e["listen"] == "test"
                          for l in e["script"]["exec"]]
                testes = [t.group(1) for t in testes if t]
                req = i["request"]
                url = req["url"]["raw"] if isinstance(req["url"], dict) else req["url"]
                url = re.sub(r"^\{\{[^}]+\}\}", "", url)
                saida.append((pasta, i["name"], req["method"], url, testes))
    percorrer(col["item"])
    return saida


def b_postman_resumo():
    grupos = OrderedDict()
    for pasta, nome, met, url, testes in postman_itens():
        g = grupos.setdefault(pasta, [0, 0])
        g[0] += 1
        g[1] += len(testes)
    linhas = [[p, q, a] for p, (q, a) in grupos.items()]
    linhas.append(["**Total**", f"**{sum(q for q, _ in grupos.values())}**", f"**{sum(a for _, a in grupos.values())}**"])
    return tabela(["Pasta da coleção", "Requisições", "Asserções"], linhas)


def b_postman_lista():
    linhas = [[p.split(" ")[0], n, f"`{m} {u}`", "; ".join(t)] for p, n, m, u, t in postman_itens()]
    return tabela(["Pasta", "Requisição (caso / requisito)", "Método e rota", "Asserções (pm.test)"], linhas)


def newman_resultado():
    xml = ler_texto(ENTREGA / "12_TDD_CICD_MELHORIA/regressao_v1.2.0/newman.xml")
    req = len(re.findall(r"<testsuite ", xml))
    casos = len(re.findall(r"<testcase ", xml))
    falhas = len(re.findall(r"<failure", xml))
    return req, casos, falhas


def b_nf_resumo():
    cab, linhas = linhas_tabela(tabelas_da_secao(ENTREGA / "10_ACEITACAO_NAO_FUNCIONAIS/P09_Aceitacao_e_Nao_Funcionais.md", "Parte B")[0])
    return tabela(cab, [[sem_negrito(x) for x in l] for l in linhas])


def b_nf_registros():
    arq = ENTREGA / "10_ACEITACAO_NAO_FUNCIONAIS/P09_Aceitacao_e_Nao_Funcionais.md"
    partes = []
    for l in secao_markdown(arq, "Parte B"):
        m = re.match(r"^### (TNF-\d+) — (.*)$", l)
        if m:
            cab, linhas = linhas_tabela(tabelas_da_secao(arq, f"{m.group(1)} —")[0])
            linhas = [[pendente(c) for c in l] for l in linhas]
            partes.append(f"### {m.group(1)} — {m.group(2)}\n\nQuadro: Registro do {m.group(1)} (modelo do Apêndice I do manual)\n\n"
                          + tabela(["Campo", "Conteúdo"], linhas) + "\n")
    return "\n".join(partes)


def pendente(texto):
    """Campos que só a pessoa externa pode preencher aparecem como pendentes (e não como marcador)."""
    t = re.sub(r"\[PREENCHER[^\]]*\]\s*(Aceito / Aceito com ressalvas / Não aceito|Atende / Atende parcialmente / Não atende)",
               r"Pendente (opções: \1)", texto)
    return re.sub(r"\[PREENCHER[^\]]*\]", "Pendente: depende da execução pela pessoa externa", t)


def b_aceitacao_registros():
    arq = ENTREGA / "10_ACEITACAO_NAO_FUNCIONAIS/P09_Aceitacao_e_Nao_Funcionais.md"
    partes = []
    for l in secao_markdown(arq, "Parte A"):
        m = re.match(r"^### (CA-\d+) — (.*)$", l)
        if m:
            cab, linhas = linhas_tabela(tabelas_da_secao(arq, f"{m.group(1)} —")[0])
            linhas = [[pendente(c) for c in l] for l in linhas]
            partes.append(f"### {m.group(1)} — {m.group(2)}\n\nQuadro: Cenário {m.group(1)} (Dado / Quando / Então)\n\n"
                          + tabela(["Campo", "Conteúdo"], linhas) + "\n")
    return "\n".join(partes)


def b_tnf01():
    d = ler_json(ENTREGA / "10_ACEITACAO_NAO_FUNCIONAIS/evidencias/TNF-01_desempenho_resultado.json")
    linhas = [[r["operacao"], r["amostras"], br(r["media_ms"]), br(r["mediana_ms"]), br(r["p95_ms"]), br(r["min_ms"]), br(r["max_ms"]),
               "Atende" if r["atende"] else "Não atende"] for r in d["resultados"]]
    return tabela(["Operação", "n", "Média (ms)", "Mediana (ms)", "p95 (ms)", "Mín. (ms)", "Máx. (ms)", "Conclusão"], linhas)


def b_tnf02():
    d = ler_json(ENTREGA / "10_ACEITACAO_NAO_FUNCIONAIS/evidencias/TNF-02_seguranca_acesso.json")
    itens = d.get("resultados") or d.get("verificacoes") or d
    cont = Counter()
    for i in itens if isinstance(itens, list) else []:
        cont[(i.get("cenario", ""), str(i.get("status", "")))] += 1
    linhas = [[c or "—", s, q] for (c, s), q in sorted(cont.items())]
    return tabela(["Cenário", "Status HTTP obtido", "Requisições"], linhas) if linhas else ""


def b_inventario():
    linhas = []
    for pasta in sorted(p for p in ENTREGA.iterdir() if p.is_dir()):
        arqs = [f for f in pasta.rglob("*") if f.is_file()]
        if pasta.name.startswith("13_"):
            arqs = [f for f in arqs if f.suffix.lower() in (".md", ".docx", ".pdf")]
        tipos = Counter(f.suffix.lower().lstrip(".") or "sem extensão" for f in arqs)
        linhas.append([f"`{pasta.name}`", len(arqs), ", ".join(f"{q} {t}" for t, q in tipos.most_common(6))])
    return tabela(["Pasta da entrega", "Arquivos", "Tipos (principais)"], linhas)


def git(*args):
    return subprocess.run(["git", *args], cwd=RAIZ, capture_output=True, text=True, encoding="utf-8").stdout.strip()


def b_tdd_commits():
    linhas = []
    for etapa, h, log in (("RED", "35ce2a2", "01_RED_mvnw_test.log"), ("GREEN", "c9c6e4c", "02_GREEN_mvnw_test.log"),
                          ("REFACTOR", "78b44e3", "03_REFACTOR_mvnw_test.log")):
        quando, assunto = git("show", "-s", "--format=%ad|%s", "--date=format:%d/%m/%Y %H:%M", h).split("|", 1)
        _, total = contar_testes_log(ENTREGA / "12_TDD_CICD_MELHORIA/tdd" / log)
        linhas.append([etapa, f"`{h}` · {quando}", assunto, f"{total[0]} testes, {total[1]} falhas" if total else "—"])
    return tabela(["Etapa", "Commit e horário", "Mensagem do commit", "`./mvnw test`"], linhas)


def trecho_java(texto, inicio):
    """Do primeiro trecho que contém `inicio` até a chave que fecha o bloco (linha só com '}' no mesmo recuo)."""
    linhas = texto.splitlines()
    i = next(k for k, l in enumerate(linhas) if l.strip() == inicio)
    recuo = len(linhas[i]) - len(linhas[i].lstrip())
    j = next(k for k in range(i + 1, len(linhas)) if linhas[k].strip() == "}" and len(linhas[k]) - len(linhas[k].lstrip()) == recuo)
    return "```java\n" + "\n".join(l[recuo:] for l in linhas[i:j + 1]) + "\n```"


def b_codigo_red():
    # o teste exatamente como estava no commit RED (antes de existir a implementação)
    texto = git("show", "35ce2a2:src/test/java/br/com/barberagenda/integration/CancelamentoAntecedenciaIntegracaoTest.java")
    return trecho_java(texto, "@Test")


def b_codigo_politica():
    return trecho_java(ler_texto(RAIZ / "src/main/java/br/com/barberagenda/service/PoliticaCancelamento.java"), "@Component")


BLOCOS = {
    "REQUISITOS_RF": b_requisitos_rf, "REQUISITOS_RNF": b_requisitos_rnf, "FORA_ESCOPO": b_fora_escopo, "RISCOS": b_riscos,
    "RISCOS_PROCESSO": lambda: b_tabela_doc("03_PLANO_DE_TESTES/P03_Plano_de_Testes.md", "4.2 Riscos do processo"),
    "RESPONSABILIDADES": lambda: b_tabela_doc("03_PLANO_DE_TESTES/P03_Plano_de_Testes.md", "10. Responsabilidades", colunas=[0, 1, 2, 3]),
    "SUSPENSAO": lambda: b_tabela_doc("03_PLANO_DE_TESTES/P03_Plano_de_Testes.md", "14. Critérios de suspensão"),
    "GESTAO_DEFEITOS": lambda: b_tabela_doc("03_PLANO_DE_TESTES/P03_Plano_de_Testes.md", "17. Gestão de defeitos"),
    "TECNICAS": lambda: b_tabela_doc("03_PLANO_DE_TESTES/P03_Plano_de_Testes.md", "7. Técnicas"),
    "TRANSICAO": lambda: b_tabela_doc("04_CASOS_E_RASTREABILIDADE/P04_Catalogo_Casos_de_Teste.md", "2.2 Transição"),
    "DECISAO": lambda: b_tabela_doc("04_CASOS_E_RASTREABILIDADE/P04_Catalogo_Casos_de_Teste.md", "2.3 Tabela de decisão"),
    "PARTICOES": lambda: b_tabela_doc("04_CASOS_E_RASTREABILIDADE/P04_Catalogo_Casos_de_Teste.md", "2.1 Particionamento"),
    "SONAR": lambda: b_tabela_doc("12_TDD_CICD_MELHORIA/P11_TDD_CICD_Melhoria.md", "2. Análise de qualidade"),
    "MELHORIAS": lambda: b_tabela_doc("12_TDD_CICD_MELHORIA/P11_TDD_CICD_Melhoria.md", "3. Plano de melhoria", colunas=[0, 1, 3, 4, 5]),
    "REGISTRO_TDD": lambda: b_tabela_doc("12_TDD_CICD_MELHORIA/P11_TDD_CICD_Melhoria.md", "1. Registro de TDD"),
    "CASOS_TECNICA": b_casos_por_tecnica, "CASOS_CLASSIFICACAO": b_casos_por_classificacao, "CASOS_REQUISITO": b_casos_por_requisito,
    "EXECUCOES_CICLO": b_execucoes_ciclo, "APENDICE_EXECUCOES": b_apendice_execucoes, "CATALOGO": b_catalogo, "MATRIZ": b_matriz,
    "RASTREABILIDADE": b_rastreabilidade_resumo, "METRICAS": b_metricas, "UNIDADE_CLASSES": b_unidade_classes,
    "E2E_CLASSES": b_e2e_classes, "TESTES_JUNIT": b_lista_junit, "TESTES_SELENIUM": b_lista_selenium,
    "POSTMAN_RESUMO": b_postman_resumo, "POSTMAN_LISTA": b_postman_lista, "NF_RESUMO": b_nf_resumo, "NF_REGISTROS": b_nf_registros,
    "ACEITACAO_REGISTROS": b_aceitacao_registros, "TNF01": b_tnf01, "INVENTARIO": b_inventario, "TDD_COMMITS": b_tdd_commits,
    "CODIGO_RED": b_codigo_red, "CODIGO_POLITICA": b_codigo_politica,
}


def valores():
    nreq, ncasos, nfalhas = newman_resultado()
    _, tot_u = contar_testes_log(ENTREGA / "12_TDD_CICD_MELHORIA/regressao_v1.2.0/unidade_integracao_mvnw_verify.log")
    _, tot_e = contar_testes_log(ENTREGA / "12_TDD_CICD_MELHORIA/regressao_v1.2.0/e2e_chrome_1366x768.log")
    m = MET
    cnt = Counter(RESULTADO[c["id"]] for c in CASOS)
    return {
        "EXECUCAO": br(m["percentual_execucao"]), "APROVACAO": br(m["taxa_aprovacao"]), "REPROVACAO": br(m["taxa_reprovacao"]),
        "COBERTURA": br(m["cobertura_requisitos"]), "AUTOMACAO": br(m["taxa_automacao"]),
        "PLANEJADOS": m["casos_planejados"], "EXECUTADOS": m["casos_executados"], "APROVADOS": m["aprovados"],
        "REPROVADOS": m["reprovados"], "REQ_EXEC": m["requisitos_com_teste_executado"], "REQ_TOTAL": m["requisitos_no_escopo"],
        "REQ_SEM": ", ".join(m["requisitos_sem_teste_executado"]), "AUTO_FEITOS": m["casos_automatizados"],
        "AUTO_PLAN": m["casos_planejados_automacao"], "DEFEITOS": m["defeitos_total"], "EXEC_REG": len(EXEC),
        "NCASOS": len(CASOS), "CT_APROV": cnt.get("Aprovado", 0), "CT_BLOQ": cnt.get("Bloqueado", 0),
        "CT_REPROV": cnt.get("Reprovado", 0), "NREQ_API": nreq, "NASSERT_API": ncasos, "NFALHA_API": nfalhas,
        "NUNIT": tot_u[0], "NE2E": tot_e[0], "NE2E_TOTAL": tot_e[0] * 4, "NRF": sum(r["tipo"] == "Funcional" for r in REQ),
        "NRNF": sum(r["tipo"] != "Funcional" for r in REQ), "NRISCOS": len(RIS),
        "NEVID05": len(list((ENTREGA / "05_EXECUCAO_MANUAL/evidencias").glob("*"))),
    }


# --------------------------------------------------------------------------- pós-processamento
def normalizar(texto):
    t = unicodedata.normalize("NFKD", texto)
    t = "".join(ch for ch in t if not unicodedata.combining(ch))
    return re.sub(r"[^a-z0-9]", "", t.lower())


def larguras(linhas):
    """Recalcula a linha separadora de uma tabela pipe: dashes proporcionais ao conteúdo de cada coluna."""
    partes = [[re.sub(r"[`*\\]", "", c.strip()) for c in re.split(r"(?<!\\)\|", l.strip())[1:-1]] for l in linhas]
    ncol = len(partes[0])
    corpo = [p for k, p in enumerate(partes) if k != 1]
    linha_util = 86  # caracteres médios de 9,5 pt que cabem na largura útil (16 cm), descontadas as margens das células

    def largura_texto(w):  # maiúsculas, dígitos e negrito ocupam mais que a letra média; pontuação, menos
        return sum(1.3 if ch.isupper() or ch.isdigit() or ch in "—–@%#" else 0.55 if ch in "il.,;:!|'()- " else 1.0 for ch in w)

    minimo, conteudo = [], []
    for j in range(ncol):
        celulas = [p[j] for p in corpo if j < len(p)]
        palavra = max((largura_texto(w) for c in celulas for w in re.split(r"[\s/]+", c) if w), default=3)
        if j < len(partes[0]) and partes[0][j]:
            palavra = max(palavra, 1.1 * max(largura_texto(w) for w in partes[0][j].split()))  # cabeçalho em negrito
        minimo.append(min(palavra + 2.5, 20))          # a maior palavra cabe sem quebrar (até 20 caracteres)
        conteudo.append(max(len(c) for c in celulas) if celulas else 3)
    # distribui o espaço restante proporcionalmente ao texto de cada coluna, sem passar do necessário (água-cheia)
    largura = list(map(float, minimo))
    teto = [max(m, c + 2) for m, c in zip(minimo, conteudo)]
    for _ in range(6):
        sobra = linha_util - sum(largura)
        abertas = [j for j in range(ncol) if largura[j] < teto[j] - 0.01]
        if sobra <= 0.01 or not abertas:
            break
        soma = sum(teto[j] - largura[j] for j in abertas)
        for j in abertas:
            largura[j] = min(teto[j], largura[j] + sobra * (teto[j] - largura[j]) / soma)
    total = sum(largura)
    dashes = [max(3, round(100 * l / total)) for l in largura]
    linhas[1] = "|" + "|".join("-" * d for d in dashes) + "|"
    return linhas


def div(estilo, texto):
    return f'::: {{custom-style="{estilo}"}}\n{texto}\n:::\n'


def pos_processar(md):
    """Numera tabelas e figuras, ajusta larguras e devolve (markdown, figuras, tabelas, títulos)."""
    saida, figs, tabs, titulos = [], [], [], []
    linhas = md.splitlines()
    i, em_codigo = 0, False
    while i < len(linhas):
        l = linhas[i]
        if l.startswith("```"):
            em_codigo = not em_codigo
            saida.append(l)
            i += 1
            continue
        if em_codigo:
            saida.append(l)
            i += 1
            continue
        m_h = re.match(r"^(#{1,2})\s+(.+?)\s*(\{[^}]*\})?$", l)
        if m_h and "{.unnumbered" not in l:
            titulos.append((len(m_h.group(1)), m_h.group(2)))
        m_t = re.match(r"^(Tabela|Quadro):\s*(.+)$", l)
        if m_t:
            tipo, resto = m_t.groups()
            titulo, _, fonte = resto.partition(" | Fonte: ")
            j = i + 1
            while j < len(linhas) and not linhas[j].startswith("|"):
                if linhas[j].strip():
                    raise ValueError(f"'{l}' não é seguido de uma tabela (bloco vazio?): {linhas[j][:60]}")
                j += 1
            k = j
            while k < len(linhas) and linhas[k].startswith("|"):
                k += 1
            bloco = larguras(linhas[j:k])
            if tipo == "Tabela":
                tabs.append(titulo.strip())
                saida.append(div("Legenda", f"Tabela {len(tabs)} – {titulo.strip()}"))
                saida += bloco + [""]
                saida.append(div("Fonte", f"Fonte: {fonte.strip()}" if fonte else FONTE_PADRAO))
            else:
                saida.append(div("TituloQuadro", titulo.strip()))
                saida += bloco + [""]
            i = k
            continue
        if l.startswith("|") and i + 1 < len(linhas) and re.match(r"^\|\s*:?-{3,}", linhas[i + 1]):
            k = i
            while k < len(linhas) and linhas[k].startswith("|"):
                k += 1
            saida += larguras(linhas[i:k])
            i = k
            continue
        m_f = re.match(r"^!\[(.+?)\]\((.+?)\)(\{[^}]*\})?\s*$", l)
        if m_f:
            titulo, caminho, attr = m_f.groups()
            titulo, _, fonte = titulo.partition(" | Fonte: ")
            figs.append(titulo.strip())
            saida.append(div("Legenda", f"Figura {len(figs)} – {titulo.strip()}"))
            saida.append(div("Figura", f"![]({caminho}){attr or ''}"))
            saida.append(div("Fonte", f"Fonte: {fonte.strip()}" if fonte else FONTE_PADRAO))
            i += 1
            continue
        saida.append(l)
        i += 1
    return "\n".join(saida), figs, tabs, titulos


def xml_esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def paragrafo_lista(estilo, texto, pagina):
    texto = re.sub(r"[`*]", "", texto)
    return (f'<w:p><w:pPr><w:pStyle w:val="{estilo}"/></w:pPr><w:r><w:t xml:space="preserve">{xml_esc(texto)}</w:t></w:r>'
            f'<w:r><w:tab/></w:r><w:r><w:t>{pagina}</w:t></w:r></w:p>')


def lista_xml(entradas, paginas, estilo_por_nivel):
    corpo = [paragrafo_lista(estilo_por_nivel(n), t, paginas.get((n, t), "")) for n, t in entradas]
    return "```{=openxml}\n" + "\n".join(corpo) + "\n```"


def localizar_paginas(pdf, titulos, figs, tabs):
    texto = subprocess.run([PDFTOTEXT, "-enc", "UTF-8", str(pdf), "-"], capture_output=True).stdout.decode("utf-8", "replace")
    paginas = texto.split("\f")
    norm = [normalizar(p) for p in paginas]
    primeira = [normalizar(next((x for x in p.splitlines() if x.strip()), "")) for p in paginas]
    achados, pos = {}, 0
    # o corpo começa na última página cuja primeira linha é o primeiro título de nível 1
    alvo = normalizar(titulos[0][1])
    inicio = max((k for k, f in enumerate(primeira) if f.startswith(alvo[:25])), default=0)
    pos = inicio
    for nivel, t in titulos:
        chave = normalizar(t)[:40]
        for k in range(pos, len(paginas)):
            if (nivel == 1 and primeira[k].startswith(chave[:30])) or (nivel > 1 and chave in norm[k]):
                achados[(nivel, t)] = k + 1
                pos = k
                break
    # legendas: procurar fora das páginas de listas e sumário (que repetem os títulos), inclusive na folha de identificação
    listas = next((k for k, f in enumerate(primeira) if f.startswith("listadefiguras")), inicio)
    validas = list(range(0, listas)) + list(range(inicio, len(paginas)))
    for tipo, lista in (("Figura", figs), ("Tabela", tabs)):
        pos = 0
        for n, t in enumerate(lista, 1):
            chave = normalizar(f"{tipo} {n} – {t}")[:45]
            for idx in range(pos, len(validas)):
                k = validas[idx]
                if chave in norm[k]:
                    achados[(tipo, f"{tipo} {n} – {t}")] = k + 1
                    pos = idx
                    break
    return achados, len(paginas) - 1


def montar(md_base, paginas):
    md, figs, tabs, titulos = pos_processar(md_base)
    sumario = lista_xml(titulos, paginas, lambda n: "Sumario1" if n == 1 else "Sumario2")
    lfig = lista_xml([("Figura", f"Figura {n} – {t}") for n, t in enumerate(figs, 1)], paginas, lambda n: "Lista")
    ltab = lista_xml([("Tabela", f"Tabela {n} – {t}") for n, t in enumerate(tabs, 1)], paginas, lambda n: "Lista")
    md = md.replace("{{SUMARIO}}", sumario).replace("{{LISTA_FIGURAS}}", lfig).replace("{{LISTA_TABELAS}}", ltab)
    return md, figs, tabs, titulos


def converter(md, destino_docx, referencia):
    destino_docx = Path(destino_docx)
    fonte = destino_docx.with_suffix(".md")
    fonte.write_text(md, encoding="utf-8")
    subprocess.run([PANDOC, str(fonte), "-f", "markdown-implicit_figures-tex_math_dollars", "-o", str(destino_docx), "--reference-doc", str(referencia),
                    "--columns=20", "--resource-path", str(PASTA), "--metadata", "lang=pt-BR"], check=True, cwd=PASTA)
    subprocess.run([SOFFICE, "--headless", "--convert-to", "pdf", "--outdir", str(destino_docx.parent), str(destino_docx)],
                   check=True, capture_output=True)
    return destino_docx.with_suffix(".pdf")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    figuras_geradas()
    texto = re.sub(r"<!--.*?-->\n?", "", MODELO.read_text(encoding="utf-8"), flags=re.S)  # comentários do modelo
    vals = valores()
    texto = re.sub(r"\{\{V:(\w+)\}\}", lambda m: str(vals[m.group(1)]), texto)
    texto = re.sub(r"\{\{(?!SUMARIO}|LISTA_FIGURAS|LISTA_TABELAS)(\w+)\}\}", lambda m: BLOCOS[m.group(1)](), texto)

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        referencia = modelo_docx.criar(PANDOC, tmp / "referencia.docx")
        md, figs, tabs, titulos = montar(texto, {})
        pdf1 = converter(md, tmp / f"{NOME}.docx", referencia)          # 1ª passagem: localizar páginas
        paginas, total = localizar_paginas(pdf1, titulos, figs, tabs)
        faltando = [t for t in titulos if t not in paginas]
        md, figs, tabs, titulos = montar(texto, paginas)                 # 2ª passagem: com os números
        pdf2 = converter(md, tmp / f"{NOME}.docx", referencia)
        paginas2, total2 = localizar_paginas(pdf2, titulos, figs, tabs)
        if paginas2 != paginas:
            md, figs, tabs, titulos = montar(texto, paginas2)
            pdf2 = converter(md, tmp / f"{NOME}.docx", referencia)
            total2 = localizar_paginas(pdf2, titulos, figs, tabs)[1]
        for ext in (".md", ".docx", ".pdf"):
            shutil.copy(tmp / f"{NOME}{ext}", PASTA / f"{NOME}{ext}")
    print(f"{NOME}: {total2} páginas, {len(titulos)} títulos no sumário, {len(figs)} figuras, {len(tabs)} tabelas")
    if faltando:
        print("ATENÇÃO — títulos sem página localizada:", faltando)


if __name__ == "__main__":
    main()
