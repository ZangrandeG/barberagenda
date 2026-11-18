# P03 — Plano de testes

**Projeto Integrado P2 — Testes e Qualidade de Software — UNISAGRADO 2026**
**Grupo:** Turma A — Guilherme Ribeiro Zangrande (RA 23110757) e José Paulo Dassie Felippi (RA 24111563)

| Versão | Data | Descrição |
|---|---|---|
| v1.0 | 2026-11-18 | Primeira versão do plano (Marco 2), com todos os itens da seção 9.4 e do Apêndice D do manual |

> Elaborado antes da decisão do professor sobre a ficha P01, por decisão do grupo. Este plano é um documento vivo: cada mudança gera nova versão nesta tabela e um commit no repositório.

## 1. Identificação e versão do sistema

| Item | Valor |
|---|---|
| Sistema | BarberAgenda — sistema web de agendamento de barbearia (fictícia) |
| Versão sob teste | 1.1.0 — tag Git `v1.1.0-sistema-base` |
| Repositório | https://github.com/ZangrandeG/barberagenda |
| Base de teste | `docs/ESPECIFICACAO_SISTEMA.md` (v1.2) e P02 (`entrega/02_REQUISITOS_ESCOPO_RISCOS/P02_Requisitos_Escopo_Riscos.md`) |
| Arquitetura | Interface HTML/JS → API REST (Spring Boot 3.5.16) → regras (service) → Spring Data JPA → H2 |

Toda execução registra a versão (tag ou hash do commit) em que foi feita. Se o sistema mudar durante os testes (correções ou TDD), a versão nova é registrada e os casos afetados são reexecutados.

## 2. Objetivo

Verificar, com evidências reproduzíveis, se o BarberAgenda 1.1.0 atende aos requisitos RF-01 a RF-08 e RNF-01 a RNF-05, priorizando os riscos de maior prioridade (R-01, R-02 e R-03), e informar quais defeitos, riscos residuais e oportunidades de melhoria permanecem antes da disponibilização aos usuários.

## 3. Escopo e fora do escopo

**Dentro do escopo:** RF-01 a RF-08 e RNF-01 a RNF-05 (detalhes e critérios de aceitação no P02, seção 1), na interface web, na API REST e no banco H2 (perfis `dev` e `test`), nos navegadores Chrome e Firefox. A evolução por TDD (Marco 9) acrescentará um requisito ao escopo.

**Fora do escopo:** conforme P02, seção 2.2 — regra de antecedência para cancelamento (até o TDD), login de clientes, pagamentos e notificações, perfil PostgreSQL, testes de carga/estresse/invasão, concorrência real, Safari/Edge/iOS, acessibilidade formal e outros idiomas/fusos.

## 4. Riscos

### 4.1 Riscos do produto

Matriz completa no P02, seção 3. Ordem de execução por prioridade:

| Prioridade | Riscos | Consequência no plano |
|---|---|---|
| Alta | R-01 (sobreposição), R-02 (funcionamento/intervalo), R-03 (acesso indevido) | Casos especificados e executados primeiro; incluídos em todas as regressões; automatizados em mais de um nível |
| Média | R-04 a R-10 | Executados no ciclo principal |
| Baixa | R-11 | Executado após os fluxos principais |

### 4.2 Riscos do processo de teste

| ID | Risco | Probabilidade | Impacto | Resposta |
|---|---|---|---|---|
| RP-01 | Prazo curto até a P2 (projeto iniciado em novembro; data da P2 a confirmar) | Alta | Alto | Executar por prioridade de risco; automatizar cedo os casos repetitivos; acompanhar `docs/PROGRESSO.md` a cada fase |
| RP-02 | Falta de pessoa externa para aceitação e usabilidade | Média | Alto | Combinar com antecedência um colega de outro grupo; roteiro pronto para execução em até 20 minutos |
| RP-03 | Ferramenta indisponível no ambiente (Docker para SonarQube, Firefox, Newman) | Média | Médio | Instalar no início da fase que a usa; SonarCloud como alternativa se o repositório for público (exige autorização do professor para troca de ferramenta) |
| RP-04 | Opção 1 não aprovada ou aprovada com ajustes | Baixa | Alto | Documentos versionados; ajuste de escopo registrado como nova versão do P02 e deste plano |
| RP-05 | Viés: o grupo construiu o sistema que testa | Alta | Médio | Casos derivados da especificação (caixa-preta); aceitação por pessoa externa; revisão cruzada dos casos entre os integrantes |
| RP-06 | Testes de interface instáveis (dependência de tempo e de carregamento) | Média | Médio | Esperas explícitas (`WebDriverWait`), dados restaurados antes de cada teste, `Clock`/datas relativas |
| RP-07 | Falha de rede ou equipamento no dia da apresentação | Baixa | Alto | Execução local, capturas, logs e vídeo de contingência (seção 13.2 do manual) |

## 5. Níveis de teste

Detalhados no documento do Marco 1 (`entrega/03_PLANO_DE_TESTES/M1_Niveis_Tipos_e_Estrategia.md`).

| Nível | Objeto | Ferramenta | Quantidade planejada (mínimo do manual) |
|---|---|---|---|
| Unidade | Regras na camada de serviço (`RegrasAgendamento`, `AgendamentoService`, `ClienteService`) e validações | JUnit 5, AssertJ, Mockito | ≥ 10 (mínimo 6) |
| Integração/API | API REST + banco | Postman/Newman; MockMvc | ≥ 8 requisições com testes (mínimo 5), com fluxo positivo e negativo por operação crítica |
| Sistema | Aplicação completa | Execução manual (P04) e Selenium | ≥ 24 casos manuais (mínimo 24); ≥ 4 testes Selenium (mínimo 4) |
| Aceitação | Cenários do cliente e do dono da barbearia | Roteiro Dado/Quando/Então | 4 cenários (mínimo 4), por pessoa externa |

## 6. Tipos de teste

| Tipo | Aplicação |
|---|---|
| Funcional | RF-01 a RF-08 em todos os níveis |
| Não funcional | RNF-01 (desempenho), RNF-02 (segurança), RNF-03 (compatibilidade), RNF-04 (confiabilidade), RNF-05 (usabilidade): ≥ 6 testes em 5 categorias (mínimo 6 em 3) |
| Confirmação (reteste) | Reexecução do caso que revelou cada defeito, após a correção, registrada como nova execução |
| Regressão | Suítes automatizadas completas após cada correção e após o TDD; pipeline a cada `push`/pull request; casos manuais de prioridade Alta após correções no mesmo requisito |
| Estático (complemento) | SonarQube: linha de base (Marco 5) e análise final (Marco 9) |

## 7. Técnicas de especificação

| Técnica | Requisitos | Exemplos |
|---|---|---|
| Particionamento de equivalência | RF-01, RF-03, RF-07 | Telefone: válido (10–11 dígitos), inválido (letras, 9 ou 12 dígitos); serviço ativo × inativo |
| Análise de valor limite | RF-01, RF-02, RF-03, RF-04, RF-07 | Nome 2/3/60/61; início 08:30/09:00; término 19:00/19:30; antecedência hoje + 30 / + 31; 3º/4º agendamento; duração 14/15/180/195; preço 0,99/1,00/1.000,00/1.000,01 |
| Transição de estados | RF-05, RF-08 | `AGENDADO` → `CANCELADO`; `AGENDADO` → `CONCLUIDO`; operações inválidas a partir de `CANCELADO`/`CONCLUIDO` |
| Tabela de decisão | RF-05 | Combinações código correto/incorreto × e-mail correto/incorreto |
| Baseada em experiência | RNF-02, RNF-03 | Entradas com HTML/script, espaços e acentos; uso em tela de celular |

As partições e os limites de cada regra serão documentados explicitamente no catálogo de casos (P04).

## 8. Ambiente

| Item | Especificação |
|---|---|
| Equipamento | Computador pessoal do grupo (Windows 11 Pro 10.0.26200, 64 bits); recomendável 8 GB de RAM |
| Execução da aplicação | Local, `http://localhost:8080`, perfil `test` (H2 em memória) para testes automatizados e `dev` (H2 em arquivo) para testes manuais e de confiabilidade |
| Versões | Registradas em `entrega/01_SISTEMA_ALVO/ambiente.md` (gerado por `scripts/registrar-ambiente.ps1`): Java 21.0.13, Maven 3.10.1 (wrapper), Spring Boot 3.5.16, H2 2.3.232, Chrome 157 |
| Pipeline | GitHub Actions (runner Ubuntu), Java 21, aplicação no perfil `test` |
| Restrições | Nenhum dado real; nenhum ambiente de produção; nenhum teste contra sistemas de terceiros |

## 9. Ferramentas

| Ferramenta | Uso no projeto | Situação |
|---|---|---|
| IntelliJ IDEA ou VS Code | Edição de código e testes | [PREENCHER IDE usada por cada integrante] |
| Git e GitHub | Versionamento, tags por marco, histórico | Em uso |
| JUnit 5 + AssertJ + Mockito | Testes de unidade | Incluídos no `spring-boot-starter-test` |
| Postman + Newman | Testes de integração/API, executados por linha de comando e no pipeline | A instalar no Marco 6 |
| Selenium WebDriver (Java) | Testes de sistema/interface, Chrome e Firefox headless | A configurar no Marco 6 (Firefox a instalar) |
| JaCoCo | Cobertura de código | A configurar no Marco 5 |
| SonarQube | Análise estática (linha de base e final) | A configurar no Marco 5 (requer Docker ou SonarCloud) |
| GitHub Issues | Registro e acompanhamento de defeitos | Disponível |
| GitHub Actions | CI/CD | A configurar no Marco 9 |
| Planilha XLSX (Python + openpyxl) | Requisitos, casos, execuções, defeitos, rastreabilidade e métricas | A gerar no Marco 3 |
| Editor de texto e apresentação | Relatório final (DOCX/PDF) e apresentação (PPTX/PDF) | Marco final |

## 10. Responsabilidades

Papéis da seção 4.2 do manual. Em grupos de dois integrantes os papéis são acumulados; todos participam de todas as etapas e devem conseguir explicar o projeto inteiro.

| Papel | Responsabilidades principais | Responsável principal | Apoio |
|---|---|---|---|
| Coordenação e planejamento | Prazos, plano de testes, riscos, versões, integração dos documentos, comunicação com o professor | [PREENCHER PELO GRUPO] | [PREENCHER] |
| Análise e execução manual | Requisitos, casos de teste, dados, execução manual, registro de defeitos, retestes | [PREENCHER PELO GRUPO] | [PREENCHER] |
| Automação e qualidade | Ferramentas, scripts automatizados, métricas, SonarQube, TDD e CI/CD | [PREENCHER PELO GRUPO] | [PREENCHER] |
| Representante do usuário (aceitação e usabilidade) | Executar os cenários de aceitação e o roteiro de usabilidade | [PREENCHER — pessoa externa ao grupo] | — |

## 11. Dados de teste

- **Somente dados fictícios:** nomes inventados, telefones fictícios, e-mails `@exemplo.com`, credencial fictícia de administrador (`admin`/`admin123`).
- **Massa inicial** (perfis `dev` e `test`): 3 barbeiros (1 inativo), 5 serviços (1 inativo), 10 clientes e 5 agendamentos com datas relativas ao dia atual e códigos de acesso fixos `SEMENTE2` a `SEMENTE6` (`docs/ESPECIFICACAO_SISTEMA.md`, seção 6).
- **Restauração:** antes de cada sessão de execução manual e de cada suíte automatizada, `bash scripts/reset-dados.sh` (ou `scripts\reset-dados.ps1`), que chama `POST /api/dev/reset` como administrador.
- **Dados criados pelos testes:** e-mails com sufixo único por execução (ex.: `ct012.20261120@exemplo.com`) para não depender de dados permanentes; datas calculadas a partir do dia da execução (ex.: "próxima segunda-feira") e registradas na evidência.
- **Datas em testes de unidade:** relógio fixo (`Clock.fixed`) em data conhecida.

## 12. Critérios de entrada

Uma rodada de execução só começa quando:

1. A versão sob teste está identificada (tag ou commit) e compila com `./mvnw -DskipTests package`.
2. A aplicação sobe no perfil previsto e `bash scripts/verificar-sistema.sh` termina sem falhas.
3. Os dados foram restaurados (`reset-dados`).
4. Os casos a executar estão especificados no P04 (revisados pelo outro integrante) e o registro de execução está preparado.
5. As ferramentas da rodada estão instaladas, com versão registrada.

## 13. Critérios de saída

A etapa de testes é considerada concluída quando:

1. 100% dos casos manuais planejados foram executados (percentual de execução = 100%) ou têm justificativa registrada para "Bloqueado"/"Não executado".
2. Todos os requisitos do escopo têm ao menos um teste executado (cobertura de requisitos = 100%).
3. Não há defeito de severidade **Crítica** ou **Alta** aberto; defeitos de severidade Média ou Baixa abertos estão justificados como risco residual no relatório final.
4. Todo defeito corrigido tem reteste aprovado e regressão executada.
5. As suítes automatizadas (unidade, API, interface) passam no pipeline na versão final.
6. As quantidades mínimas da seção 10 do manual foram atingidas e as 8 métricas foram calculadas com dados reais.

## 14. Critérios de suspensão e retomada

| Suspender a execução quando | Retomar quando |
|---|---|
| A aplicação não compila ou não sobe no perfil previsto | Build e `verificar-sistema.sh` voltam a passar |
| Um defeito Crítico bloqueia 30% ou mais dos casos da rodada | O defeito está "Pronto para reteste" e o reteste foi aprovado |
| Os dados de teste ficam inconsistentes (ex.: restauração falhou) | `reset-dados` executado com sucesso e verificação passando |
| Ferramenta essencial indisponível (navegador, Newman, Java) | Ferramenta reinstalada e versão registrada |
| A versão sob teste mudou sem registro | Nova versão identificada e casos afetados replanejados |

Toda suspensão é registrada (data, motivo, casos afetados) no registro de execução.

## 15. Cronograma

Alinhado aos marcos da seção 7 do manual. As datas-limite dependem do calendário da disciplina.

| Marco | Atividades principais | Produtos | Data-limite | Situação |
|---|---|---|---|---|
| 0 e 1 — Fundamentos | Grupo, duas opções de sistema, níveis e justificativa; sistema base | P01, documento do Marco 1 | [PREENCHER] | Concluído em 2026-11-18 (tag `marco-1`) |
| 2 — Planejamento | Requisitos, escopo, riscos e plano de testes | P02, P03 | [PREENCHER] | Concluído em 2026-11-18 (tag `marco-2`), aguardando aprovação do sistema |
| 3 — Especificação | ≥ 24 casos com partições e limites; matriz de rastreabilidade em XLSX | P04, P05 | [PREENCHER] | Planejado |
| 4 — Execução e defeitos | Execução manual com evidências; defeitos no GitHub Issues; retestes | P06, P07 | [PREENCHER] | Planejado |
| 5 — Automação e suporte | ≥ 6 testes de unidade; JaCoCo; SonarQube linha de base | P08 (unidade) | [PREENCHER] | Planejado |
| 6 — Integração e sistema | Postman/Newman (≥ 5) e Selenium (≥ 4) | P08 (API e interface) | [PREENCHER] | Planejado |
| 7 — Aceitação e não funcionais | 4 cenários de aceitação; 6 testes não funcionais | P09 | [PREENCHER] | Planejado |
| 9 — TDD, CI/CD e melhoria | Ciclo Red-Green-Refactor; pipeline (execução verde e com falha); SonarQube final; plano de melhoria | P11 | [PREENCHER] | Planejado |
| 8 — Métricas | 8 indicadores, gráficos e interpretação | P10 | [PREENCHER] | Planejado (após o Marco 9, para usar os dados finais; versão preliminar se o professor cobrar antes) |
| Entrega final | Relatório, apresentação, vídeo de contingência, diário, Drive | P12, P13, P14 | Data da P2: [PREENCHER] | Planejado |

## 16. Produtos

| Código | Produto | Pasta de entrega |
|---|---|---|
| P01 | Ficha de identificação e aprovação | `00_IDENTIFICACAO_E_README` |
| P02 | Requisitos, escopo e riscos | `02_REQUISITOS_ESCOPO_RISCOS` |
| P03 | Plano de testes (este documento) | `03_PLANO_DE_TESTES` |
| P04 | Catálogo de casos de teste | `04_CASOS_E_RASTREABILIDADE` |
| P05 | Matriz de rastreabilidade (XLSX) | `04_CASOS_E_RASTREABILIDADE` |
| P06 | Evidências de execução manual | `05_EXECUCAO_MANUAL` |
| P07 | Registro de defeitos (GitHub Issues + exportação) | `06_DEFEITOS` |
| P08 | Scripts de automação (unidade, API, interface) | `07_AUTOMACAO_UNITARIA`, `08_INTEGRACAO_API`, `09_SISTEMA_INTERFACE` |
| P09 | Aceitação e não funcionais | `10_ACEITACAO_NAO_FUNCIONAIS` |
| P10 | Métricas e indicadores | `11_METRICAS_E_QUALIDADE` |
| P11 | TDD, CI/CD e melhoria contínua | `12_TDD_CICD_MELHORIA` |
| P12 | Relatório final (DOCX e PDF) | `13_RELATORIO_FINAL` |
| P13 | Apresentação e roteiro de demonstração | `14_APRESENTACAO_E_VIDEO_CONTINGENCIA` |
| P14 | Diário de participação | `15_DIARIO_DE_PARTICIPACAO` |

## 17. Gestão de defeitos

| Item | Definição |
|---|---|
| Ferramenta | GitHub Issues do repositório, no modelo do Apêndice G |
| Severidade (impacto técnico) | **Crítica:** impede o uso principal ou corrompe/expõe dados. **Alta:** regra de negócio importante violada, sem alternativa. **Média:** função prejudicada com alternativa. **Baixa:** problema visual ou de texto sem prejuízo funcional |
| Prioridade (urgência da correção) | **Alta:** corrigir antes da próxima rodada. **Média:** corrigir no ciclo atual. **Baixa:** pode ficar para melhoria futura |
| Status | Novo → Em análise → Em correção → Pronto para reteste → Encerrado (ou Reaberto, se o reteste falhar) |
| Regra | Registrar somente defeitos reais observados na execução; cada defeito aponta requisito, caso, execução e evidência |

## 18. Métricas planejadas

As 8 métricas da seção 9.13 do manual, calculadas a partir da planilha de execuções e da exportação das issues: percentual de execução, taxa de aprovação, taxa de reprovação, cobertura de requisitos, taxa de automação, defeitos por severidade, defeitos por status e taxa de reabertura — cada uma com gráfico e interpretação (P10).

## 19. Controle de versão

- **Código, scripts e documentos** no repositório Git (`main`). Proposta: trabalho de testes em uma branch própria do grupo (`testes-p2`), integrada à `main` por pull request, o que também aciona o pipeline (seção 9.1, item 2 do manual) — [CONFIRMAR PELO GRUPO].
- **Tags:** `vX.Y.Z-sistema-base` para versões do sistema; `marco-N` ao fim de cada marco.
- **Documentos:** cabeçalho com tabela de versões (versão, data, descrição); versões anteriores preservadas no histórico do Git. Nenhum histórico é reescrito (sem `push --force`).
- **Commits:** pequenos, em português, no padrão `tipo: descrição` (ex.: `test: adiciona testes de unidade da regra de sobreposição (CT-012)`).
- **Drive:** a pasta `entrega/` espelha as 17 pastas obrigatórias e será copiada para o Drive do professor a cada marco e na entrega final.

## 20. Comunicação

| Com quem | Canal | Conteúdo |
|---|---|---|
| Professor | Aulas, Connect+ e canal definido na disciplina | Aprovação do sistema, mudanças de escopo e exceções (sempre por escrito) |
| Entre os integrantes | [PREENCHER canal do grupo] | Divisão de tarefas e andamento |
| Registro de andamento | `docs/PROGRESSO.md` no repositório | Situação de cada fase e produto, decisões e pendências |
| Defeitos | GitHub Issues | Registro, discussão e acompanhamento até o encerramento |
| Participação | Diário de Participação (P14), atualizado a cada atividade | Quem fez o quê, quando e com qual evidência |
