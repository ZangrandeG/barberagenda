# O que o grupo precisa revisar, completar ou decidir

Lista final (2026-11-18), a pedido do grupo: "preencha o que falta e no final indique o que mudar". Ordem sugerida: primeiro a seção A (sem isso a entrega não fica completa), depois B e C.

## A. Obrigatório antes da entrega — só vocês podem fazer

| # | O que fazer | Onde | Por quê |
|---|---|---|---|
| A1 | ~~Número do grupo~~ — **feito (2026-11-25)**: o grupo é identificado pelos integrantes ("Grupo Guilherme e José Paulo"); pasta do Drive `P2_TQS_2026_A_GRUPO_GUILHERME_JOSEPAULO_BARBERAGENDA`. Se o professor atribuir um número, trocar | P01, README, P12, comprovante | Feito |
| A2 | ~~Aprovação da ficha P01~~ — **feito**: aprovada pelo professor em 2026-11-19, sem ajustes (registrado em 2026-11-25) | P01 | Feito |
| A3 | ~~Regra do professor sobre uso de IA~~ — **feito**: uso de IA autorizado pelo professor; declaração mantida em P01 e P12 (registrado em 2026-11-25) | P01, P12 | Feito |
| A4 | **Aceitação** (CA-01 a CA-04) com pessoa externa ao grupo e registro da decisão | P09, parte A; depois `dados/execucoes.csv` | Não pode ser simulado |
| A5 | **Usabilidade** (TNF-08) com participante externo, usando o roteiro e o questionário | `P09_Roteiro_Usabilidade.md` | Não pode ser simulado |
| A6 | **Gravar o vídeo de contingência** (até 5 min, MP4) | `14_APRESENTACAO_E_VIDEO_CONTINGENCIA/` (roteiro na seção 6) | Manual 13.2 |
| A7 | **Diário de Participação**: revisar as linhas sugeridas e preencher responsável, colaboradores e tempo reais | P14 | Deve refletir a participação real |
| A8 | Assinar a declaração do relatório e o **COMPROVANTE_DE_ENTREGA** (data, hora, checklist) | P12 e `00_IDENTIFICACAO_E_README/COMPROVANTE_DE_ENTREGA.pdf` | Manual 11.6 |
| A9 | Decidir o **acesso ao repositório**: hoje está **privado**. Tornar público (`gh repo edit --visibility public`) ou adicionar o professor como colaborador; testar os links em janela anônima | GitHub | Manual 11.6, item 3 |
| A10 | Copiar `entrega/` para a pasta do Drive do professor com o nome `P2_TQS_2026_A_GRUPO_GUILHERME_JOSEPAULO_BARBERAGENDA` e dar permissão de visualização/download | Drive | Entrega oficial é pelo Drive |
| A11 | Informar a **data da P2** e preencher as datas-limite | P03, seção 15 | Não informada |

Depois de A4, A5 e do CT-036: lançar as execuções em `dados/execucoes.csv`, rodar `python scripts/gerar_artefatos.py` e `python scripts/metricas.py`, atualizar os números do P10 e rodar `python scripts/gerar_relatorio.py`, que regenera o P12 (MD, DOCX e PDF) com os dados novos.

## B. Preenchido por mim por suposição — confirmar ou corrigir

| Onde | O que foi preenchido |
|---|---|
| P03, seção 10 | Papéis: Guilherme (coordenação, automação) e José Paulo (análise e execução manual) |
| P03, seções 9 e 20 | IDE (VS Code) e canal de comunicação (grupo de mensagens + issues) |
| P04 | Responsável: CT-001 a CT-018 José Paulo; CT-019 a CT-036 Guilherme |
| P11, seção 3 | Responsáveis das ações de melhoria M-01 a M-07 |
| P13 | Divisão da fala entre os integrantes e tempos por slide |
| P02/RNF-05 | Critério de usabilidade (5 minutos, nota ≥ 4) |

## C. Feito pela IA a pedido do grupo — vocês podem refazer ou complementar

| Item | Situação | Sugestão |
|---|---|---|
| Execução dos 36 casos manuais (P06) | Executados por Claude (IA) com `scripts/execucao_assistida.py`, registrados como tal; 35 aprovados, CT-036 bloqueado (exige horário comercial; foi executado às 23h) | Executar o CT-036 entre 09:00 e 16:30 e, se quiserem, reexecutar alguns casos à mão (novas linhas EX com o nome de vocês) |
| Sistema, testes, scripts e documentos | Construídos com apoio de IA | Ler e conseguir explicar cada parte (manual 13.2); as "3 perguntas do professor" de cada fase ajudam |
| Relatório final (P12) | Ampliado em 2026-11-26 (99 páginas, padrão ABNT: Arial 12, espaçamento 1,5, margens 3/2 cm, sumário, listas de figuras e tabelas, 10 apêndices), gerado por `scripts/gerar_relatorio.py` a partir de `scripts/relatorio/P12_modelo.md` e dos dados reais | Ler o relatório inteiro; para mudar o texto, editar o modelo (não o arquivo gerado) e rodar o script de novo |

## D. Decisões técnicas que vocês devem conhecer (para responder ao professor)

- Construímos o sistema antes da aprovação da ficha (decisão de vocês em 2026-11-18); o professor aprovou a ficha em 2026-11-19.
- Revisão de segurança antes dos testes gerou as versões 1.0.1 (reset protegido) e 1.1.0 (código de acesso aleatório); não foram registradas como defeitos porque não vieram da execução de casos.
- SonarQube roda localmente em zip (sem Docker), com dados em `D:\SonarQubeDados` (o disco C: tem menos de 10% livre). Senha e tokens em `C:\Users\Admin\Ferramentas\SONARQUBE_LOCAL.txt` (fora do Git). Não há capturas de tela do painel: exigem login.
- A branch `demo/falha-pipeline` contém a falha **proposital** do pipeline (demonstração exigida) e não deve ser integrada à `main`.
- Nenhum defeito foi encontrado na execução dos casos: isso é um resultado real e está explicado no P10 e no P12.
