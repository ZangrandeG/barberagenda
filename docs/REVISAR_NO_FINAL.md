# O que o grupo precisa revisar, completar ou decidir

Lista final (2026-11-18), a pedido do grupo: "preencha o que falta e no final indique o que mudar". Ordem sugerida: primeiro a seção A (sem isso a entrega não fica completa), depois B e C.

## A. Obrigatório antes da entrega — só vocês podem fazer

| # | O que fazer | Onde | Por quê |
|---|---|---|---|
| A1 | Informar o **número do grupo** e substituir `[PREENCHER]`/`GRUPO[XX]` | P01, README (raiz e pasta 00), P03, P12 (capa e identificação), comprovante, nome da pasta do Drive | Não foi informado |
| A2 | Levar a **ficha P01 ao professor** e registrar decisão, ajustes e data | P01 | Manual 5.5: o sistema precisa estar aprovado |
| A3 | Confirmar a **regra do professor sobre uso de IA** e manter/ajustar a declaração | P01 e P12 (folha de identificação) | Manual, seção 15 |
| A4 | **Aceitação** (CA-01 a CA-04) com pessoa externa ao grupo e registro da decisão | P09, parte A; depois `dados/execucoes.csv` | Não pode ser simulado |
| A5 | **Usabilidade** (TNF-08) com participante externo, usando o roteiro e o questionário | `P09_Roteiro_Usabilidade.md` | Não pode ser simulado |
| A6 | **Gravar o vídeo de contingência** (até 5 min, MP4) | `14_APRESENTACAO_E_VIDEO_CONTINGENCIA/` (roteiro na seção 6) | Manual 13.2 |
| A7 | **Diário de Participação**: revisar as linhas sugeridas e preencher responsável, colaboradores e tempo reais | P14 | Deve refletir a participação real |
| A8 | Assinar a declaração do relatório e o **COMPROVANTE_DE_ENTREGA** (data, hora, checklist) | P12 e `00_IDENTIFICACAO_E_README/COMPROVANTE_DE_ENTREGA.pdf` | Manual 11.6 |
| A9 | Decidir o **acesso ao repositório**: hoje está **privado**. Tornar público (`gh repo edit --visibility public`) ou adicionar o professor como colaborador; testar os links em janela anônima | GitHub | Manual 11.6, item 3 |
| A10 | Copiar `entrega/` para a pasta do Drive do professor com o nome `P2_TQS_2026_A_GRUPOXX_BARBERAGENDA` e dar permissão de visualização/download | Drive | Entrega oficial é pelo Drive |
| A11 | Informar a **data da P2** e preencher as datas-limite | P03, seção 15 | Não informada |

Depois de A4, A5 e do CT-036: lançar as execuções em `dados/execucoes.csv`, rodar `python scripts/gerar_artefatos.py` e `python scripts/metricas.py`, atualizar os números do P10/P12 e regerar o DOCX/PDF (comandos no README).

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
| Relatório final (P12) | Formatação padrão do pandoc | Se o professor exigir ABNT/fonte específica, ajustar estilos no DOCX e exportar o PDF de novo pelo próprio Word/LibreOffice |

## D. Decisões técnicas que vocês devem conhecer (para responder ao professor)

- Construímos o sistema antes da aprovação da ficha (decisão de vocês em 2026-11-18).
- Revisão de segurança antes dos testes gerou as versões 1.0.1 (reset protegido) e 1.1.0 (código de acesso aleatório); não foram registradas como defeitos porque não vieram da execução de casos.
- SonarQube roda localmente em zip (sem Docker), com dados em `D:\SonarQubeDados` (o disco C: tem menos de 10% livre). Senha e tokens em `C:\Users\Admin\Ferramentas\SONARQUBE_LOCAL.txt` (fora do Git). Não há capturas de tela do painel: exigem login.
- A branch `demo/falha-pipeline` contém a falha **proposital** do pipeline (demonstração exigida) e não deve ser integrada à `main`.
- Nenhum defeito foi encontrado na execução dos casos: isso é um resultado real e está explicado no P10 e no P12.
