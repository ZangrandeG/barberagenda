# P08 — Testes de unidade automatizados (Marco 5)

**Projeto Integrado P2 — BarberAgenda 1.1.0** — Turma A — Guilherme Ribeiro Zangrande e José Paulo Dassie Felippi

| Versão | Data | Descrição |
|---|---|---|
| v1.0 | 2026-11-18 | 35 métodos de teste (52 execuções com os parametrizados), JaCoCo e linha de base do SonarQube |

## 1. Objetivo e princípios

Verificar as regras de negócio isoladamente, sem banco, rede ou interface (manual, seção 9.8):

- **Isolamento:** os repositórios são substituídos por *mocks* (Mockito); as validações usam o Bean Validation sem subir o Spring.
- **Tempo controlado:** o "agora" vem de um `Clock` fixo em **quarta-feira, 18/11/2026, 10:00 (America/Sao_Paulo)** — os testes de data dão o mesmo resultado em qualquer dia.
- **Uma intenção por teste**, com nome descritivo (`deveRejeitar...`, `deveAceitar...`) e `@DisplayName` indicando o **caso de teste (CT) e o requisito (RF)** que representa.
- **Valores limite** com testes parametrizados (`@ParameterizedTest`), por exemplo 08:30/09:00, D+30/D+31, 14/15/180/195 minutos.
- **Dados fictícios** em `DadosTeste.java`.

## 2. Ferramentas e versões

| Ferramenta | Versão |
|---|---|
| JUnit Jupiter | 5.12.2 |
| Mockito | 5.17.0 |
| AssertJ | 3.27.7 |
| Hibernate Validator | 8.0.3.Final |
| JaCoCo | 0.8.16 |
| Java / Maven | 21.0.13 / 3.10.1 (wrapper) |

## 3. Como executar

```bash
./mvnw test                     # executa os testes e gera a cobertura em target/site/jacoco/index.html
```

Código: `src/test/java/br/com/barberagenda/unit/`.

## 4. Resultado da execução (2026-11-18)

Comando `./mvnw -B test`, versão 1.1.0 (commit posterior à tag `marco-3`):

| Classe de teste | Execuções | Falhas | Erros |
|---|---|---|---|
| AgendamentoServiceTest | 13 | 0 | 0 |
| CadastroServiceTest | 4 | 0 | 0 |
| RegrasAgendamentoTest | 19 | 0 | 0 |
| ValidacaoEntradaTest | 16 | 0 | 0 |
| **Total** | **52** | **0** | **0** |

Evidências: `execucao_mvnw_test_2026-11-18.log` (saída completa), `surefire/` (relatórios XML e texto por classe) e `jacoco/index.html` (cobertura).

## 5. Cobertura (JaCoCo)

| Escopo | Linhas | Ramos |
|---|---|---|
| Projeto inteiro | 196/539 = **36,4%** | 59/116 = 50,9% |
| Pacote `service` (regras de negócio) | 126/164 = **76,8%** | — |
| `RegrasAgendamento` | 42/42 = **100%** | 26/28 |
| `AgendamentoService` | 64/69 = 92,8% | 18/22 |
| `ClienteService` | 8/11 = 72,7% | 2/2 |
| `BarbeiroService` | 11/17 = 64,7% | 2/2 |

A cobertura geral é baixa porque os controllers, a segurança e a carga de dados (0%) só são exercitados por testes de integração e de interface, previstos para o Marco 6. Os testes de unidade concentram-se na camada de regras, onde está o maior risco (R-01, R-02, R-04).

## 6. Rastreabilidade: teste → caso → requisito

| Classe | Método | Caso / requisito | O que verifica |
|---|---|---|---|
| AgendamentoServiceTest | `deveRejeitarAgendamentoQuandoHorarioConflitaComOutroDoMesmoBarbeiro` | CT-019 / RF-04 | recusa agendamento sobreposto a outro do mesmo barbeiro |
| AgendamentoServiceTest | `deveRejeitarQuartoAgendamentoAtivoDoCliente` | CT-021 / RF-04 | recusa o 4º agendamento quando o cliente já tem 3 ativos |
| AgendamentoServiceTest | `deveAceitarTerceiroAgendamentoAtivoDoCliente` | CT-021 / RF-04 | aceita o 3º agendamento ativo e grava status, término e código de acesso |
| AgendamentoServiceTest | `deveRejeitarAgendamentoComBarbeiroInativo` | CT-017 / RF-03 | recusa agendamento com barbeiro inativo |
| AgendamentoServiceTest | `deveRejeitarAgendamentoComServicoInativo` | CT-017 / RF-03 | recusa agendamento com serviço inativo |
| AgendamentoServiceTest | `deveRejeitarAgendamentoDeClienteNaoCadastrado` | CT-018 / RF-03 | recusa agendamento de e-mail não cadastrado |
| AgendamentoServiceTest | `naoDeveOferecerHorariosOcupadosPeloBarbeiro` | CT-008 / RF-02 | não oferece horários que se sobrepõem a agendamento do barbeiro (14:00–15:00) |
| AgendamentoServiceTest | `deveOferecerHorarioDeAgendamentoCancelado` | CT-025 / RF-05 | agendamento cancelado não ocupa o horário |
| AgendamentoServiceTest | `deveCancelarAgendamentoAtivoDoCliente` | CT-025 / RF-05 | cliente cancela agendamento ativo informando código e e-mail |
| AgendamentoServiceTest | `deveRecusarConsultaComEmailDeOutroCliente` | CT-024 / RF-05 | consulta com e-mail de outra pessoa é recusada como não encontrada |
| AgendamentoServiceTest | `deveRejeitarCancelamentoDeAgendamentoJaCancelado` | CT-026 / RF-05 | recusa cancelar agendamento que já está cancelado |
| AgendamentoServiceTest | `deveRejeitarConclusaoDeAgendamentoCancelado` | CT-035 / RF-08 | recusa concluir agendamento cancelado |
| AgendamentoServiceTest | `deveConcluirAgendamentoAtivo` | CT-034 / RF-08 | conclui agendamento ativo |
| CadastroServiceTest | `deveRejeitarCadastroComEmailJaCadastrado` | CT-006 / RF-01 | recusa cadastro com e-mail já cadastrado, mesmo em maiúsculas |
| CadastroServiceTest | `deveCadastrarClienteComDadosValidos` | CT-001 / RF-01 | cadastra cliente com dados válidos e data de cadastro do relógio |
| CadastroServiceTest | `deveRejeitarExclusaoDeBarbeiroComAgendamentos` | CT-033 / RF-07 | recusa excluir barbeiro que possui agendamentos |
| CadastroServiceTest | `deveExcluirBarbeiroSemAgendamentos` | CT-033 / RF-07 | exclui barbeiro sem agendamentos |
| RegrasAgendamentoTest | `deveGerarHorariosDe09hA18hParaServicoDe60Minutos` | CT-007 / RF-02 | serviço de 60 min tem 19 inícios possíveis, de 09:00 a 18:00, de 30 em 30 min |
| RegrasAgendamentoTest | `naoDeveOferecerHorariosJaPassadosNoDiaDeHoje` | RF-02 | no dia de hoje não são oferecidos horários que já passaram (agora = 10:00) |
| RegrasAgendamentoTest | `deveRetornarListaVaziaParaDataSemAtendimento` | CT-009 / RF-02 | data sem atendimento não tem horários disponíveis |
| RegrasAgendamentoTest | `deveAceitarAgendamentoNosLimitesDoFuncionamento` | CT-011 / RF-03 | aceita agendamento nos limites do horário de funcionamento |
| RegrasAgendamentoTest | `deveRejeitarAgendamentoForaDoHorarioDeFuncionamento` | CT-012 / RF-03 | recusa agendamento que começa antes de 09:00 ou termina depois de 19:00 |
| RegrasAgendamentoTest | `deveRejeitarInicioForaDoIntervaloDe30Minutos` | CT-013 / RF-03 | recusa início fora dos intervalos de 30 minutos |
| RegrasAgendamentoTest | `deveRejeitarAgendamentoNoDomingo` | CT-014 / RF-03 | recusa agendamento no domingo |
| RegrasAgendamentoTest | `deveAceitarAgendamentoComTrintaDiasDeAntecedencia` | CT-015 / RF-03 | aceita agendamento com exatamente 30 dias de antecedência (D+30) |
| RegrasAgendamentoTest | `deveRejeitarAgendamentoComTrintaEUmDiasDeAntecedencia` | CT-015 / RF-03 | recusa agendamento com 31 dias de antecedência (D+31) |
| RegrasAgendamentoTest | `deveRejeitarAgendamentoNoPassado` | CT-016 / RF-03 | recusa agendamento em data ou horário que já passou |
| RegrasAgendamentoTest | `deveAceitarProximoHorarioDoDiaDeHoje` | CT-016 / RF-03 | aceita o próximo horário do dia de hoje (10:30, com agora = 10:00) |
| ValidacaoEntradaTest | `deveAceitarNomeETelefoneNosLimitesValidos` | CT-002 / RF-01 | aceita nome e telefone nos limites válidos |
| ValidacaoEntradaTest | `deveRejeitarNomeForaDoLimite` | CT-003 / RF-01 | recusa nome com 2 e com 61 caracteres |
| ValidacaoEntradaTest | `deveRejeitarTelefoneForaDoPadrao` | CT-004 / RF-01 | recusa telefone com 9 ou 12 dígitos ou com caracteres não numéricos |
| ValidacaoEntradaTest | `deveRejeitarEmailEmFormatoInvalido` | CT-005 / RF-01 | recusa e-mail sem @ ou sem domínio de topo |
| ValidacaoEntradaTest | `deveAceitarServicoNosLimitesValidos` | CT-030 / RF-07 | aceita duração e preço nos limites válidos |
| ValidacaoEntradaTest | `deveRejeitarDuracaoForaDosLimites` | CT-031 / RF-07 | recusa duração menor que 15, não múltipla de 15 ou maior que 180 |
| ValidacaoEntradaTest | `deveRejeitarPrecoForaDosLimites` | CT-031 / RF-07 | recusa preço abaixo de R$ 1,00 ou acima de R$ 1.000,00 |

**Casos do P04 com teste de unidade:** 27 — 17 candidatos automatizados por completo (a unidade era o único nível planejado), 9 candidatos parcialmente (falta o nível de API ou de interface, previsto para o Marco 6) e 1 caso não candidato (CT-034). Taxa de automação atual na planilha P05: 17/31 = 54,8%.

## 7. Linha de base de qualidade (SonarQube)

Primeira análise feita em 2026-11-18 com o SonarQube Community Build 26.11 local, logo após os testes de unidade (antes de qualquer correção). Detalhes em `entrega/11_METRICAS_E_QUALIDADE/sonar_baseline/resumo.md`.

| Medida | Linha de base |
|---|---|
| Bugs | 3 (regra `java:S8696`) |
| Vulnerabilidades | 2 (`java:S3330` cookie sem HttpOnly; `java:S4502` proteção CSRF) |
| Code smells | 0 |
| Duplicação | 0,0% |
| Cobertura | 38,9% |
| Dívida técnica | 0 min |
| Notas (confiabilidade / segurança / manutenibilidade) | D / D / A |
| Quality gate (Sonar way) | OK — avalia apenas "código novo"; na primeira análise não há código novo |

Os 5 problemas serão analisados no Marco 9 (melhoria contínua): corrigidos quando procedentes, ou justificados quando forem decisões de projeto (o cookie `XSRF-TOKEN` precisa ser legível pelo JavaScript para o padrão de CSRF adotado). A segunda análise será comparada com esta.
