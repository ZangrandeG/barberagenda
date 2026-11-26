"""
Gera a apresentação final (P13) em PPTX: poucas palavras e imagens grandes; o texto detalhado fica nas notas
do apresentador, divididas entre os integrantes. Imagens: scripts/gerar_imagens_apresentacao.py.
Uso: python scripts/gerar_apresentacao.py   (depois: soffice --headless --convert-to pdf <pptx>)
"""
import sys
from pathlib import Path

from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

RAIZ = Path(__file__).resolve().parent.parent
PASTA = RAIZ / "entrega" / "14_APRESENTACAO_E_VIDEO_CONTINGENCIA"
IMG = PASTA / "imagens"
METR = RAIZ / "entrega" / "11_METRICAS_E_QUALIDADE" / "metricas"
COMPAT = RAIZ / "entrega/10_ACEITACAO_NAO_FUNCIONAIS/evidencias/TNF-07_compatibilidade/capturas"
MARROM, ESCURO, CLARO = RGBColor(0x5B, 0x3A, 0x29), RGBColor(0x2B, 0x26, 0x22), RGBColor(0xF6, 0xF3, 0xEF)
G, J = "Guilherme", "José Paulo"


def fundo(s, cor):
    f = s.background.fill
    f.solid()
    f.fore_color.rgb = cor


def texto(s, x, y, w, h, linhas, tamanho=24, cor=ESCURO, negrito=False, alinhar=PP_ALIGN.LEFT):
    tf = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)).text_frame
    tf.word_wrap = True
    for k, linha in enumerate(linhas):
        p = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
        p.text, p.alignment = linha, alinhar
        p.space_after = Pt(12)
        p.runs[0].font.size, p.runs[0].font.bold, p.runs[0].font.color.rgb = Pt(tamanho), negrito, cor


def titulo(s, t):
    barra = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(1.0))
    barra.fill.solid()
    barra.fill.fore_color.rgb = MARROM
    barra.line.fill.background()
    texto(s, 0.5, 0.15, 12.3, 0.8, [t], 30, RGBColor(0xFF, 0xFF, 0xFF), True)


def imagem(s, arquivo, x, y, w, h):
    """Insere a imagem centralizada dentro da caixa (x, y, w, h), mantendo a proporção."""
    largura, altura = Image.open(arquivo).size
    escala = min(w / largura, h / altura)
    lw, lh = largura * escala, altura * escala
    s.shapes.add_picture(str(arquivo), Inches(x + (w - lw) / 2), Inches(y + (h - lh) / 2), Inches(lw), Inches(lh))


def numero(s, x, y, valor, legenda, cor=MARROM):
    caixa = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(3.6), Inches(1.6))
    caixa.fill.solid()
    caixa.fill.fore_color.rgb = cor
    caixa.line.fill.background()
    texto(s, x, y + 0.1, 3.6, 0.9, [valor], 40, RGBColor(0xFF, 0xFF, 0xFF), True, PP_ALIGN.CENTER)
    texto(s, x, y + 0.95, 3.6, 0.6, [legenda], 16, RGBColor(0xFF, 0xFF, 0xFF), False, PP_ALIGN.CENTER)


def novo(prs, t, notas):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    fundo(s, CLARO)
    if t:
        titulo(s, t)
    s.notes_slide.notes_text_frame.text = notas
    return s


def main():
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)

    s = novo(prs, None, f"{G}: apresenta o grupo, o sistema e o roteiro (12 a 15 minutos).")
    fundo(s, ESCURO)
    texto(s, 0.7, 1.6, 5.6, 1.5, ["BarberAgenda"], 54, RGBColor(0xFF, 0xFF, 0xFF), True)
    texto(s, 0.7, 2.8, 5.6, 2.5, ["Qualidade e testes de um sistema de agendamento", "Guilherme R. Zangrande · José Paulo D. Felippi",
                                  "Testes e Qualidade de Software — UNISAGRADO 2026"], 20, RGBColor(0xE8, 0xDE, 0xD3))
    imagem(s, IMG / "tela_inicio.png", 6.6, 1.2, 6.3, 5.2)

    s = novo(prs, "O sistema", f"{G}: o cliente se cadastra, escolhe barbeiro, serviço, data e horário livre e recebe um código de "
             "acesso para consultar ou cancelar. O dono administra barbeiros, serviços e a agenda do dia.")
    imagem(s, IMG / "tela_horarios.png", 0.4, 1.3, 8.4, 5.8)
    texto(s, 9.1, 2.2, 3.9, 4, ["Cliente agenda sozinho", "Dono gerencia a agenda", "Só horários livres aparecem"], 24)

    s = novo(prs, "Como foi construído", f"{G}: Java 21 com Spring Boot. A tela chama a API REST (JSON); os controllers recebem, "
             "os services aplicam as regras e os repositories gravam no H2. Erros sempre no mesmo formato, sem detalhes internos.")
    imagem(s, IMG / "arquitetura.png", 0.5, 1.6, 12.3, 5.2)

    s = novo(prs, "Riscos: o que testar primeiro", f"{J}: 12 riscos classificados por probabilidade × impacto. Os de prioridade Alta "
             "(R-01 horários sobrepostos, R-02 fora do expediente, R-03 acesso indevido) foram testados primeiro e entram em toda regressão.")
    imagem(s, IMG / "riscos.png", 0.5, 1.3, 7.6, 5.9)
    texto(s, 8.5, 2.3, 4.5, 4, ["12 riscos", "Prioridade Alta: conflito de horário, expediente, acesso indevido"], 24)

    s = novo(prs, "Estratégia: pirâmide de testes", f"{J}: muitos testes rápidos onde ficam as regras (unidade), menos na API e poucos "
             "na interface, que são lentos. Nas regras de data usamos um relógio fixo, para o teste dar o mesmo resultado em qualquer dia.")
    imagem(s, IMG / "piramide.png", 0.5, 1.3, 7.2, 5.9)
    texto(s, 8.2, 2.3, 4.8, 4, ["Mais testes onde está a regra", "Relógio fixo nos testes de data", "Dados fictícios restauráveis"], 24)

    s = novo(prs, "Casos de teste e execução", f"{J}: 36 casos com partições e valores limite (ex.: 08:30 recusado, 09:00 aceito). "
             "Mostrar o CT-012 no P04 e a evidência. Nenhum defeito na execução — os problemas foram achados antes, por revisão e SonarQube.")
    numero(s, 0.6, 1.5, "36", "casos manuais")
    numero(s, 0.6, 3.4, "35 ✓", "aprovados", RGBColor(0x2E, 0x7D, 0x4F))
    numero(s, 0.6, 5.3, "0", "defeitos", RGBColor(0x5A, 0x5A, 0x5A))
    imagem(s, IMG / "tela_consulta.png", 4.6, 1.3, 8.3, 5.9)

    s = novo(prs, "Automação — demonstração", f"{G}: DEMONSTRAÇÃO — '.\\mvnw.cmd test' (58 testes) e o Newman (26 requisições, 63 asserções). "
             "O Selenium abre o navegador e agenda sozinho; cada tela tem uma classe (Page Object).")
    imagem(s, IMG / "tela_confirmacao.png", 0.4, 1.3, 8.4, 5.9)
    texto(s, 9.1, 2.2, 3.9, 4, ["58 unidade + integração", "26 requisições de API", "11 testes de interface"], 24, MARROM, True)

    s = novo(prs, "Testes não funcionais", f"{J}: desempenho medido em 30 repetições; segurança sem login barrada em 28 de 28 rotas; "
             "o sistema funciona no Chrome e no Firefox, no computador e no celular. Aceitação e usabilidade aguardam pessoa externa.")
    numero(s, 0.6, 1.5, "34 ms", "tempo de resposta (p95)", RGBColor(0x3A, 0x6E, 0xA5))
    numero(s, 0.6, 3.4, "28/28", "acessos sem login barrados")
    numero(s, 0.6, 5.3, "44/44", "Chrome e Firefox, PC e celular", RGBColor(0x2E, 0x7D, 0x4F))
    imagem(s, COMPAT / "AgendamentoE2ETest_deveAgendarHorarioPelaTela_chrome_375x667_OK.png", 4.8, 1.3, 3.6, 5.9)
    imagem(s, COMPAT / "AgendamentoE2ETest_deveAgendarHorarioPelaTela_firefox_375x667_OK.png", 8.9, 1.3, 3.6, 5.9)

    s = novo(prs, "Métricas", f"{J}: 87,5% executado (faltam aceitação/usabilidade com pessoa externa e um caso de horário comercial), "
             "100% aprovado, 85,7% dos requisitos cobertos e 100% da automação planejada.")
    imagem(s, METR / "02_indicadores_percentuais.png", 1.2, 1.3, 10.9, 5.9)

    s = novo(prs, "TDD: teste antes do código", f"{G}: regra nova 'cancelar só com 2 horas de antecedência'. Primeiro o teste falhou "
             "(RED), depois o código mínimo (GREEN) e por fim a organização em PoliticaCancelamento (REFACTOR). Três commits no GitHub.")
    imagem(s, IMG / "tdd.png", 0.5, 1.6, 12.3, 5.2)

    s = novo(prs, "Pipeline CI/CD", f"{G}: DEMONSTRAÇÃO — GitHub Actions roda tudo a cada envio de código. Mostrar as 3 execuções: "
             "verde, falha proposital (teste alterado de propósito numa branch) e correção.")
    imagem(s, IMG / "pipeline.png", 0.5, 1.5, 12.3, 4.3)
    texto(s, 0.5, 6.0, 12.3, 1, ["Verde  →  falha proposital  →  correção"], 26, MARROM, True, PP_ALIGN.CENTER)

    s = novo(prs, "Qualidade do código (SonarQube)", f"{J}: linha de base × final — bugs 3 → 0, cobertura 38,9% → 72,3%, "
             "confiabilidade D → A. As 2 vulnerabilidades restantes são decisões de projeto justificadas.")
    imagem(s, IMG / "sonar.png", 0.8, 1.4, 11.7, 5.7)

    s = novo(prs, "Conclusão", f"{J}: pronto para demonstração; para uso real faltam a aceitação com usuários e as melhorias do plano "
             "(limite de tentativas, segurança do CSRF). Lição: análise estática e testes se complementam. Abrir para perguntas.")
    imagem(s, IMG / "tela_admin_agenda.png", 0.4, 1.3, 8.0, 5.9)
    texto(s, 8.8, 2.2, 4.2, 4.5, ["Pronto para demonstração", "Falta: aceitação com usuários", "Plano com 7 melhorias", "Perguntas?"], 24)

    PASTA.mkdir(parents=True, exist_ok=True)
    destino = PASTA / (sys.argv[1] if len(sys.argv) > 1 else "P13_Apresentacao.pptx")
    prs.save(destino)
    print(f"{destino.relative_to(RAIZ)}: {len(prs.slides)} slides")


if __name__ == "__main__":
    main()
