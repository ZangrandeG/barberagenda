"""
Gera as imagens da apresentação (P13): diagramas (matplotlib) e capturas limpas das telas do sistema.
Requer a aplicação no ar em http://localhost:8080 (perfil dev ou test) para as capturas.
Uso: python scripts/gerar_imagens_apresentacao.py
"""
import datetime as dt
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402

sys.path.insert(0, str(Path(__file__).parent / "nf"))
import comum  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / "entrega" / "14_APRESENTACAO_E_VIDEO_CONTINGENCIA" / "imagens"
MARROM, VERDE, VERMELHO, AZUL, CINZA = "#5b3a29", "#2e7d4f", "#b23b3b", "#3a6ea5", "#7a7a7a"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 13, "axes.spines.top": False, "axes.spines.right": False})


def salvar(fig, nome):
    fig.savefig(SAIDA / nome, dpi=160, bbox_inches="tight", transparent=False, facecolor="white")
    plt.close(fig)


def caixa(ax, x, y, w, h, texto, cor, fonte=13):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08", fc=cor, ec="none"))
    ax.text(x + w / 2, y + h / 2, texto, ha="center", va="center", color="white", fontsize=fonte, fontweight="bold")


def seta(ax, a, b, cor=CINZA):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=22, color=cor, lw=2.2))


def arquitetura():
    fig, ax = plt.subplots(figsize=(12, 3.2))
    ax.set_xlim(0, 12); ax.set_ylim(0, 3); ax.axis("off")
    itens = [("Navegador\nHTML/CSS/JS", AZUL), ("API REST\ncontrollers", MARROM), ("Regras\nservices", VERDE), ("Banco H2\nJPA", CINZA)]
    for i, (t, c) in enumerate(itens):
        caixa(ax, 0.2 + i * 3, 1.0, 2.4, 1.3, t, c)
        if i:
            seta(ax, (i * 3 - 0.4, 1.65), (i * 3 + 0.2, 1.65))
    ax.text(6, 0.35, "Java 21 · Spring Boot 3.5 · Spring Security · JSON padronizado", ha="center", fontsize=13, color="#333")
    salvar(fig, "arquitetura.png")


def piramide():
    fig, ax = plt.subplots(figsize=(7, 5.2))
    ax.set_xlim(0, 10); ax.set_ylim(0, 9); ax.axis("off")
    niveis = [("Selenium\n11 testes", 3.4, AZUL), ("API — Postman/Newman\n26 requisições · 63 asserções", 5.6, MARROM),
              ("Unidade + integração — JUnit\n58 testes", 8.4, VERDE)]
    for i, (t, w, c) in enumerate(reversed(niveis)):
        y = i * 2.8
        ax.add_patch(FancyBboxPatch((5 - w / 2, y + 0.2), w, 2.4, boxstyle="round,pad=0.02,rounding_size=0.1", fc=c, ec="none"))
        ax.text(5, y + 1.4, t, ha="center", va="center", color="white", fontsize=12, fontweight="bold")
    salvar(fig, "piramide.png")


def tdd():
    fig, ax = plt.subplots(figsize=(11, 3.4))
    ax.set_xlim(0, 11); ax.set_ylim(0, 3.4); ax.axis("off")
    etapas = [("RED\nteste falha\n35ce2a2", VERMELHO), ("GREEN\ncódigo mínimo\nc9c6e4c", VERDE), ("REFACTOR\norganiza o código\n78b44e3", AZUL)]
    for i, (t, c) in enumerate(etapas):
        caixa(ax, 0.3 + i * 3.7, 0.9, 3.0, 1.9, t, c, 14)
        if i:
            seta(ax, (i * 3.7 - 0.4, 1.85), (i * 3.7 + 0.3, 1.85))
    ax.text(5.5, 0.3, "Regra RF-09: cancelar com menos de 2 h → HTTP 422", ha="center", fontsize=13, color="#333")
    salvar(fig, "tdd.png")


def pipeline():
    fig, ax = plt.subplots(figsize=(12, 4.2))
    ax.set_xlim(0, 12); ax.set_ylim(0, 4.2); ax.axis("off")
    caixa(ax, 0.2, 1.5, 2.2, 1.2, "push /\npull request", CINZA)
    caixa(ax, 3.2, 1.5, 2.8, 1.2, "Unidade +\nintegração + JaCoCo", VERDE, 12)
    caixa(ax, 7.0, 2.6, 2.6, 1.0, "API — Newman", MARROM, 12)
    caixa(ax, 7.0, 0.6, 2.6, 1.0, "Interface — Selenium", AZUL, 12)
    caixa(ax, 10.2, 1.5, 1.6, 1.2, "Relatórios", CINZA, 12)
    seta(ax, (2.45, 2.1), (3.15, 2.1)); seta(ax, (6.05, 2.3), (6.95, 3.05)); seta(ax, (6.05, 1.9), (6.95, 1.15))
    seta(ax, (9.65, 3.05), (10.15, 2.4)); seta(ax, (9.65, 1.15), (10.15, 1.8))
    salvar(fig, "pipeline.png")


def sonar():
    base = json.load(open(RAIZ / "entrega/11_METRICAS_E_QUALIDADE/sonar_baseline/medidas.json", encoding="utf-8"))
    final = json.load(open(RAIZ / "entrega/11_METRICAS_E_QUALIDADE/sonar_final/medidas.json", encoding="utf-8"))
    v = lambda d, k: float(next(m["value"] for m in d["component"]["measures"] if m["metric"] == k))  # noqa: E731
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.2))
    for ax, rot, chave, cor in ((a1, "Bugs", "bugs", VERMELHO), (a2, "Cobertura (%)", "coverage", VERDE)):
        vals = [v(base, chave), v(final, chave)]
        b = ax.bar(["Linha de base", "Final"], vals, color=[CINZA, cor], width=0.55)
        ax.set_title(rot, fontsize=16, loc="left")
        ax.set_yticks([])
        for barra, x in zip(b, vals):
            ax.annotate(f"{x:g}", (barra.get_x() + barra.get_width() / 2, barra.get_height()), ha="center", va="bottom", fontsize=18, fontweight="bold")
        ax.set_ylim(0, max(vals) * 1.25 + 0.5)
    salvar(fig, "sonar.png")


def riscos():
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.set_xlim(-0.5, 2.5); ax.set_ylim(-0.5, 2.5)
    cores = [["#e8f1e8", "#fff3d6", "#fde2d2"], ["#fff3d6", "#fde2d2", "#f8c9c9"], ["#fde2d2", "#f8c9c9", "#f0a8a8"]]
    for i in range(3):
        for j in range(3):
            ax.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, fc=cores[i][j], ec="white", lw=3))
    nivel = {"Baixa": 0, "Média": 1, "Alta": 2, "Baixo": 0, "Médio": 1, "Alto": 2}
    pos = {}
    for r in json.load(open(RAIZ / "dados/riscos.json", encoding="utf-8")):
        pos.setdefault((nivel[r["impacto"]], nivel[r["probabilidade"]]), []).append(r["id"])
    for (x, y), ids in pos.items():
        ax.text(x, y, "\n".join(", ".join(ids[k:k + 3]) for k in range(0, len(ids), 3)), ha="center", va="center", fontsize=12, fontweight="bold")
    ax.set_xticks(range(3), ["Baixo", "Médio", "Alto"]); ax.set_yticks(range(3), ["Baixa", "Média", "Alta"])
    ax.set_xlabel("Impacto"); ax.set_ylabel("Probabilidade")
    salvar(fig, "riscos.png")


def capturas():
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import Select, WebDriverWait

    base = "http://localhost:8080"
    comum.restaurar(base)
    op = webdriver.ChromeOptions()
    op.add_argument("--headless=new"); op.add_argument("--window-size=1280,800"); op.add_argument("--hide-scrollbars")
    d = webdriver.Chrome(options=op)
    w = WebDriverWait(d, 10)
    foto = lambda nome: d.save_screenshot(str(SAIDA / nome))  # noqa: E731
    try:
        d.get(base + "/index.html"); foto("tela_inicio.png")
        d.get(base + "/agendar.html")
        d.find_element(By.ID, "campo-email-agendamento").send_keys("camila.prado@exemplo.com")
        for campo, texto in (("campo-barbeiro", "Carlos Navalha"), ("campo-servico", "Barba")):
            w.until(lambda x: len(x.find_elements(By.CSS_SELECTOR, f"#{campo} option")) > 1)
            sel = Select(d.find_element(By.ID, campo))
            sel.select_by_visible_text(next(o.text for o in sel.options if o.text.startswith(texto)))
        data = comum.dias_de_funcionamento(7, 1)[0]
        d.execute_script("arguments[0].value=arguments[1];", d.find_element(By.ID, "campo-data"), data.isoformat())
        d.find_element(By.ID, "botao-buscar-horarios").click()
        w.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='horario-11:00']"))).click()
        d.execute_script("document.getElementById('titulo-horarios').scrollIntoView({block:'start'})"); foto("tela_horarios.png")
        d.find_element(By.ID, "botao-confirmar-agendamento").click()
        w.until(EC.visibility_of_element_located((By.ID, "resumo-agendamento")))
        d.execute_script("document.getElementById('mensagem-agendamento').scrollIntoView({block:'start'})"); foto("tela_confirmacao.png")
        d.get(base + "/consulta.html")
        d.find_element(By.ID, "campo-codigo-acesso").send_keys("SEMENTE2")
        d.find_element(By.ID, "campo-email-consulta").send_keys("ana.rocha@exemplo.com")
        d.find_element(By.ID, "botao-consultar").click()
        w.until(EC.visibility_of_element_located((By.ID, "detalhes-agendamento")))
        d.execute_script("document.getElementById('detalhes-agendamento').scrollIntoView({block:'center'})"); foto("tela_consulta.png")
        d.get(base + "/admin/login.html")
        d.find_element(By.ID, "campo-usuario").send_keys(comum.ADMIN[0])
        d.find_element(By.ID, "campo-senha").send_keys(comum.ADMIN[1])
        d.find_element(By.ID, "botao-entrar").click()
        w.until(EC.url_contains("/admin/index.html"))
        d.get(base + "/admin/agenda.html")
        w.until(lambda x: len(x.find_elements(By.CSS_SELECTOR, "#campo-barbeiro-agenda option")) > 0)
        Select(d.find_element(By.ID, "campo-barbeiro-agenda")).select_by_visible_text("Rafael Tesoura")
        d.execute_script("arguments[0].value=arguments[1];", d.find_element(By.ID, "campo-data-agenda"), comum.dias_de_funcionamento(1, 1)[0].isoformat())
        d.find_element(By.ID, "botao-carregar-agenda").click()
        w.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#tabela-agenda tbody tr")))
        foto("tela_admin_agenda.png")
    finally:
        d.quit()
        comum.restaurar(base)


def main():
    SAIDA.mkdir(parents=True, exist_ok=True)
    for f in (arquitetura, piramide, tdd, pipeline, sonar, riscos, capturas):
        f()
    print(sorted(p.name for p in SAIDA.glob("*.png")))


if __name__ == "__main__":
    main()
