"""
Gera a apresentação final (P13) em PPTX, com notas do apresentador divididas entre os integrantes.
Uso: python scripts/gerar_apresentacao.py   (depois: soffice --headless --convert-to pdf <pptx>)
"""
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Inches, Pt

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / "entrega" / "14_APRESENTACAO_E_VIDEO_CONTINGENCIA" / "P13_Apresentacao.pptx"
G, J = "Guilherme", "José Paulo"
MARROM, CINZA = RGBColor(0x5B, 0x3A, 0x29), RGBColor(0x55, 0x55, 0x55)
IMG = {"metricas": RAIZ / "entrega/11_METRICAS_E_QUALIDADE/metricas/02_indicadores_percentuais.png",
       "casos": RAIZ / "entrega/11_METRICAS_E_QUALIDADE/metricas/01_resultado_dos_casos.png",
       "tela": RAIZ / "entrega/09_SISTEMA_INTERFACE/capturas/AgendamentoE2ETest_deveAgendarHorarioPelaTela_chrome_1366x768_OK.png"}

SLIDES = [
    ("BarberAgenda — qualidade e testes", ["Projeto Integrado P2 — Testes e Qualidade de Software", "Guilherme Ribeiro Zangrande e José Paulo Dassie Felippi — Turma A",
      "Prof. Dr. Elvio Gilberto da Silva — UNISAGRADO 2026"], None, f"{G}: apresenta o grupo e o roteiro (12 a 15 min, 7 partes)."),
    ("1. Sistema, objetivo e escopo", ["Agendamento web de barbearia fictícia: cliente agenda e cancela; dono administra",
      "Java 21, Spring Boot 3.5, API REST, H2, interface HTML/JS — versão 1.2.0",
      "Escopo: 9 requisitos funcionais + 5 não funcionais com critério mensurável",
      "Fora do escopo: pagamentos, login de clientes, carga/invasão, concorrência real"], None,
     f"{G}: o que o sistema faz e por que foi escolhido (regras com limites, API, interface). Mostrar o README."),
    ("2. Riscos e estratégia de teste", ["12 riscos; prioridade Alta: horários sobrepostos, fora do expediente, acesso indevido",
      "Pirâmide: muitos testes de unidade nas regras, menos de API, poucos de interface",
      "Clock injetável → testes de data reproduzíveis; dados fictícios restauráveis",
      "Níveis: unidade, integração, sistema, aceitação; tipos: funcional, não funcional, confirmação, regressão"], None,
     f"{J}: matriz de riscos (P02) e plano (P03). Explicar diferença entre nível e tipo de teste."),
    ("3. Casos, técnicas e execução", ["36 casos manuais: partições e valores limite por regra (ex.: 08:30/09:00, D+30/D+31, 3º/4º)",
      "Transição de estados (status) e tabela de decisão (código × e-mail)",
      "Execução: 35 aprovados, 1 bloqueado (CT-036 exige horário comercial)",
      "Defeitos: nenhum observado — problemas foram achados antes, por revisão e SonarQube"], None,
     f"{J}: mostrar um caso (CT-012) no P04, a evidência EX-xxx e a planilha P05. Explicar por que 0 defeitos não foi inventado nem escondido."),
    ("4. Automação em vários níveis", ["Unidade/integração: 58 testes (JUnit, Mockito, MockMvc), cobertura 74%",
      "API: Postman/Newman — 26 requisições, 63 asserções, encadeamento cadastro → agendar → cancelar",
      "Interface: Selenium com Page Objects e esperas explícitas — 11 testes",
      "Taxa de automação: 39/39 candidatos"], "tela",
     f"{G}: DEMONSTRAÇÃO 1 — rodar './mvnw test' e o Newman (roteiro de demonstração)."),
    ("5. Aceitação, não funcionais e métricas", ["Desempenho p95 26–34 ms (critério < 500 ms); segurança 28/28; HTML não executado",
      "Confiabilidade: dados após reinício, 16/16 entradas inválidas sem HTTP 500",
      "Compatibilidade: Chrome e Firefox, desktop e celular (44/44)",
      "Execução 87,5% · aprovação 100% · cobertura de requisitos 85,7% · automação 100%"], "metricas",
     f"{J}: P09 e P10. Aceitação e usabilidade aguardam pessoa externa — explicar como serão aplicadas."),
    ("6. TDD e pipeline CI/CD", ["RF-09 por TDD: RED (4 falhas pelo motivo certo) → GREEN → REFACTOR (PoliticaCancelamento)",
      "Cancelar com menos de 2 h → HTTP 422",
      "GitHub Actions: unidade+cobertura, Newman e Selenium a cada push/PR",
      "Demonstração: run verde, falha proposital e correção"], None,
     f"{G}: DEMONSTRAÇÃO 2 — commits 35ce2a2, c9c6e4c, 78b44e3 e as 3 runs no GitHub Actions."),
    ("7. Conclusão e melhorias", ["SonarQube: bugs 3 → 0, cobertura 38,9% → 72,3%, confiabilidade D → A",
      "Apto para demonstração; para uso real: aceitação externa, CT-036, ações de segurança",
      "Melhorias M-01 a M-07 com responsável e critério de verificação",
      "Lição: análise estática + testes dinâmicos se complementam"], "casos",
     f"{J}: fecha com a situação do sistema e o plano de melhoria. Abrir para perguntas (até 5 min)."),
]


def main():
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    for i, (titulo, itens, imagem, notas) in enumerate(SLIDES):
        s = prs.slides.add_slide(prs.slide_layouts[6])
        caixa = s.shapes.add_textbox(Inches(0.6), Inches(0.4), Inches(12), Inches(1.0)).text_frame
        caixa.text = titulo
        caixa.paragraphs[0].runs[0].font.size = Pt(40 if i == 0 else 32)
        caixa.paragraphs[0].runs[0].font.bold = True
        caixa.paragraphs[0].runs[0].font.color.rgb = MARROM
        largura = Inches(6.6) if imagem else Inches(12)
        corpo = s.shapes.add_textbox(Inches(0.7), Inches(1.7), largura, Inches(5.2)).text_frame
        corpo.word_wrap = True
        for k, item in enumerate(itens):
            p = corpo.paragraphs[0] if k == 0 else corpo.add_paragraph()
            p.text = ("" if i == 0 else "• ") + item
            p.space_after = Pt(14)
            p.runs[0].font.size = Pt(22 if i == 0 else 20)
            p.runs[0].font.color.rgb = CINZA if i == 0 else RGBColor(0x22, 0x22, 0x22)
        if imagem:
            s.shapes.add_picture(str(IMG[imagem]), Inches(7.5), Inches(1.9), width=Inches(5.4))
        s.notes_slide.notes_text_frame.text = notas
    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    prs.save(SAIDA)
    print(f"{SAIDA.relative_to(RAIZ)}: {len(SLIDES)} slides")


if __name__ == "__main__":
    main()
