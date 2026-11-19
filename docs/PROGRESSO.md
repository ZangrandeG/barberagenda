# Progresso do Projeto P2 — BarberAgenda

Arquivo de acompanhamento para retomar o trabalho entre sessões. Atualizado a cada etapa.

**Última atualização:** 2026-11-18

## Situação atual

- Fase 1 concluída: ficha P01 (v1.2) e sistema base, versão atual 1.1.0 (tag `v1.1.0-sistema-base`). O grupo decidiu construir o sistema antes da decisão do professor sobre a ficha.
- Fase 2 concluída: Marco 1 (níveis, tipos e estratégia) — tag `marco-1`.
- Fase 3 concluída: Marco 2 (P02 e P03) — tag `marco-2`. Feita antes da aprovação do professor, por decisão do grupo (o manual pede o sistema aprovado no Marco 2).
- Fase 4 concluída: Marco 3 (P04 com 35 casos e P05 em XLSX) — tag `marco-3`. Fonte única em `dados/`; gerador `scripts/gerar_artefatos.py`.
- Fase 5 em andamento: **o grupo executa os 35 casos** (decisão de 2026-11-18). Preparação pronta: roteiro, checklist, registro, convenção de evidências, `scripts/datas_teste.py`, modelo de issue "Defeito", etiquetas no GitHub e `scripts/exportar_defeitos.py`. Nenhum caso executado ainda.
- Ao trazer resultados: lançar em `dados/execucoes.csv`, abrir issues para reprovações, rodar `exportar_defeitos.py` e `gerar_artefatos.py`; depois, tag `marco-4`.
- Fase 6 concluída (adiantada enquanto o grupo executa a Fase 5): 35 métodos de teste de unidade (52 execuções, 0 falhas), JaCoCo (36,4% linhas; serviços 76,8%) e linha de base do SonarQube (3 bugs, 2 vulnerabilidades, 0 code smells, 0% duplicação, cobertura 38,9%) — tag `marco-5`.
- Fase 7 concluída: Postman/Newman (26 requisições, 63 asserções, 0 falhas) e Selenium (5 testes E2E, Chrome headless, 0 falhas) — tag `marco-6`. Taxa de automação 31/31.
- SonarQube: Community Build 26.11 em zip (sem Docker) em `C:\Users\Admin\Ferramentas`, dados em `D:\SonarQubeDados` (o C: tem menos de 10% livre). Senha do admin e tokens só em `C:\Users\Admin\Ferramentas\SONARQUBE_LOCAL.txt` (fora do Git). Capturas de tela do painel não foram feitas: exigem login (a liberação de acesso anônimo foi negada); evidência = exportação pela API.

## Fases

| Fase | Marco | Situação |
|---|---|---|
| 1a — Ficha de proposta (P01) | Marco 1 (parcial) | Concluída v1.2 — aguardando decisão do professor |
| 1b — Sistema base + README + ambiente | — | Concluída em 2026-11-18 — versão atual 1.1.0 (tag `v1.1.0-sistema-base`); verificação 46/46 |
| 2 — Fundamentos | Marco 1 | Concluída em 2026-11-18 — `entrega/03_PLANO_DE_TESTES/M1_Niveis_Tipos_e_Estrategia.md`; tag `marco-1` |
| 3 — Planejamento (P02, P03) | Marco 2 | Concluída em 2026-11-18 — tag `marco-2` |
| 4 — Especificação (P04, P05) | Marco 3 | Concluída em 2026-11-18 — tag `marco-3` |
| 5 — Execução manual e defeitos (P06, P07) | Marco 4 | Em andamento — preparação concluída; execução pelo grupo pendente |
| 6 — Automação unitária + Sonar linha de base (P08) | Marco 5 | Concluída em 2026-11-18 — tag `marco-5` |
| 7 — Integração/API e sistema/interface (P08) | Marco 6 | Concluída em 2026-11-18 — tag `marco-6` |
| 8 — Aceitação e não funcionais (P09) | Marco 7 | Não iniciada |
| 9 — TDD, CI/CD e melhoria (P11) | Marco 9 | Não iniciada |
| 10 — Métricas (P10) | Marco 8 | Não iniciada |
| 11 — Entrega final (P12, P13, P14, Drive) | Entrega final | Não iniciada |

## Produtos

| Código | Produto | Arquivo | Situação |
|---|---|---|---|
| P01 | Ficha de identificação e aprovação | `entrega/00_IDENTIFICACAO_E_README/P01_Ficha_Sistema.md` | v1.2 — aguardando professor |
| — | Sistema base, README, ambiente | `README.md`, `docs/ESPECIFICACAO_SISTEMA.md`, `entrega/01_SISTEMA_ALVO/` | Versão 1.1.0 — concluído |
| — | Marco 1: níveis, tipos e estratégia (insumo do P03) | `entrega/03_PLANO_DE_TESTES/M1_Niveis_Tipos_e_Estrategia.md` | v1.0 — concluído |
| P02 | Requisitos, escopo e riscos | `entrega/02_REQUISITOS_ESCOPO_RISCOS/P02_Requisitos_Escopo_Riscos.md` | v1.0 — 8 RF, 5 RNF, 11 riscos |
| P03 | Plano de testes | `entrega/03_PLANO_DE_TESTES/P03_Plano_de_Testes.md` | v1.0 — completo; responsabilidades, IDE, canal e datas a preencher |
| P04 | Catálogo de casos de teste | `entrega/04_CASOS_E_RASTREABILIDADE/P04_Catalogo_Casos_de_Teste.md` | v1.0 — 35 casos (7 positivos, 9 negativos, 8 fronteira, 6 alternativos, 5 exceção); 31 candidatos à automação; responsáveis a preencher |
| P05 | Matriz de rastreabilidade | `entrega/04_CASOS_E_RASTREABILIDADE/P05_Matriz_Rastreabilidade.xlsx` | v1.0 — 7 abas com fórmulas; execuções e defeitos vazios até o Marco 4 |
| P06 | Evidências de execução manual | `entrega/05_EXECUCAO_MANUAL/` (roteiro, checklist, registro, evidencias/) | Preparado — 0 de 35 casos executados |
| P07 | Registro de defeitos | GitHub Issues (etiqueta `defeito`) + `entrega/06_DEFEITOS/` | Preparado — modelo, etiquetas e exportação prontos; 0 defeitos |
| P08 | Scripts de automação | `src/test/java/.../unit/` e `.../e2e/`; `postman/`; `entrega/07`, `08` e `09` | Concluído: unidade (52 execuções), API (26 requisições/63 asserções), interface (5 testes); 31/31 candidatos automatizados |
| P09 | Aceitação e não funcionais | — | Não iniciado |
| P10 | Métricas e indicadores | — | Não iniciado |
| P11 | TDD, CI/CD e melhoria contínua | — | Não iniciado |
| P12 | Relatório final | — | Não iniciado |
| P13 | Apresentação e roteiro de demonstração | — | Não iniciado |
| P14 | Diário de participação | `entrega/15_DIARIO_DE_PARTICIPACAO/P14_Diario_Participacao.md` | Modelo criado — preenchimento contínuo pelo grupo |

## Decisões registradas

| Data | Decisão |
|---|---|
| 2026-11-18 | Ficha de proposta antes da construção do sistema (manual, seção 5.5). |
| 2026-11-18 | Estrutura `entrega/` criada com as 17 pastas da seção 11.3. |
| 2026-11-18 | `MANUAL_P2.pdf` mantido apenas localmente (fora do Git), por ser material do professor. |
| 2026-11-18 | Proposta de ramificação: `main` com o sistema base; branch `testes-p2` para o trabalho de testes, integrada por pull request (seção 9.1, item 2). [CONFIRMAR PELO GRUPO] |
| 2026-11-18 | Spring Boot 3.5.16 (última linha 3.x; o Spring Initializr só oferece 4.x, então o projeto foi montado manualmente com o Maven Wrapper oficial). |
| 2026-11-18 | Desvios em relação ao prompt inicial, por segurança e usabilidade: `GET /api/clientes` exige administrador; o agendamento identifica o cliente pelo e-mail (`emailCliente`); consulta/cancelamento exigem código + e-mail. Ver `docs/ESPECIFICACAO_SISTEMA.md`, seção 5. |
| 2026-11-18 | Regra de cancelamento com antecedência mínima **não** implementada: reservada para o TDD (Fase 9). |
| 2026-11-18 | Versão 1.0.1 (tag `v1.0.1-sistema-base`): revisão automática de segurança do código, feita antes do início dos testes, apontou que `POST /api/dev/reset` não exigia autenticação; passou a exigir administrador e CSRF. Por ter sido encontrado em revisão de código durante o desenvolvimento (e não na execução de um caso de teste), não foi registrado como defeito do processo de testes. Verificação: 42/42. |
| 2026-11-18 | Versão 1.1.0 (tag `v1.1.0-sistema-base`), por decisão do grupo: a mesma revisão apontou que consulta/cancelamento por id sequencial + e-mail permitia, a quem conhecesse o e-mail de alguém, descobrir e cancelar os agendamentos dessa pessoa variando o id. Agora cada agendamento recebe um código de acesso aleatório de 8 caracteres, exigido junto com o e-mail; o código não aparece nas respostas administrativas. Massa fictícia com códigos fixos `SEMENTE2`…`SEMENTE6`. Verificação: 46/46 (`verificacao_v1.1.0_2026-11-18.txt`). |

## Repositório

- GitHub: https://github.com/ZangrandeG/barberagenda (privado em 2026-11-18; visibilidade a decidir — a seção 11.6 pede links testados em janela anônima)
- Branch `main`; identidade Git deste computador: Guilherme Ribeiro Zangrande (e-mail `noreply` do GitHub)

## Ambiente (verificado em 2026-11-18)

| Ferramenta | Situação |
|---|---|
| Java | JDK 21.0.13 (Eclipse Temurin) instalado em 2026-11-18; Java 1.8 continua presente (usar `JAVA_HOME`) |
| Maven | 3.10.1 via Maven Wrapper |
| Git | 2.56.0 |
| GitHub CLI (`gh`) | 2.105.0, autenticado como `ZangrandeG` |
| Node / npm | 24.21.0 / 11.19.0 |
| Newman | Não instalado |
| Python | 3.11.9 — falta `openpyxl` e `matplotlib` |
| Chrome | Instalado |
| Firefox | Não instalado |
| Docker | Não instalado |
| pandoc / LibreOffice | Não instalados |

## Pendências do grupo

- [x] Identidade do Git configurada neste computador (Guilherme). José Paulo configura a própria no computador dele.
- [x] Turma (A) e integrantes preenchidos na ficha P01.
- [x] JDK 21 e GitHub CLI instalados; repositório criado no GitHub.
- [x] RAs preenchidos na ficha P01.
- [x] Convite de colaborador (escrita) enviado para `zepadf` em 2026-11-18 — José Paulo precisa aceitar em https://github.com/ZangrandeG/barberagenda/invitations
- [ ] Preencher número do grupo na ficha P01.
- [ ] Confirmar a licença (MIT) e a opção preferencial.
- [ ] Apresentar a ficha ao professor e registrar a decisão, os ajustes e a data.
- [ ] Informar: orientação do professor sobre uso de IA, data da P2, marcos já entregues, repositório público ou privado.
