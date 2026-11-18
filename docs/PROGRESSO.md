# Progresso do Projeto P2 — BarberAgenda

Arquivo de acompanhamento para retomar o trabalho entre sessões. Atualizado a cada etapa.

**Última atualização:** 2026-11-18

## Situação atual

- Fase 1 concluída: ficha P01 (v1.2) e sistema base, versão atual 1.1.0 (tag `v1.1.0-sistema-base`). O grupo decidiu construir o sistema antes da decisão do professor sobre a ficha.
- Fase 2 concluída: Marco 1 (níveis, tipos e estratégia) — tag `marco-1`.
- Próxima: Fase 3 (Marco 2 — P02 requisitos/escopo/riscos e P03 plano de testes). O manual pede o sistema **aprovado** no Marco 2. Aguardando: decisão do professor sobre a ficha e respostas do grupo (ver Pendências).

## Fases

| Fase | Marco | Situação |
|---|---|---|
| 1a — Ficha de proposta (P01) | Marco 1 (parcial) | Concluída v1.2 — aguardando decisão do professor |
| 1b — Sistema base + README + ambiente | — | Concluída em 2026-11-18 — versão atual 1.1.0 (tag `v1.1.0-sistema-base`); verificação 46/46 |
| 2 — Fundamentos | Marco 1 | Concluída em 2026-11-18 — `entrega/03_PLANO_DE_TESTES/M1_Niveis_Tipos_e_Estrategia.md`; tag `marco-1` |
| 3 — Planejamento (P02, P03) | Marco 2 | Não iniciada |
| 4 — Especificação (P04, P05) | Marco 3 | Não iniciada |
| 5 — Execução manual e defeitos (P06, P07) | Marco 4 | Não iniciada |
| 6 — Automação unitária + Sonar linha de base (P08) | Marco 5 | Não iniciada |
| 7 — Integração/API e sistema/interface (P08) | Marco 6 | Não iniciada |
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
| P02 | Requisitos, escopo e riscos | — | Não iniciado |
| P03 | Plano de testes | — | Não iniciado |
| P04 | Catálogo de casos de teste | — | Não iniciado |
| P05 | Matriz de rastreabilidade | — | Não iniciado |
| P06 | Evidências de execução manual | — | Não iniciado |
| P07 | Registro de defeitos | — | Não iniciado |
| P08 | Scripts de automação | — | Não iniciado |
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
