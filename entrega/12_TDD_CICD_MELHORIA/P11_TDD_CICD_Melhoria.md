# P11 — TDD, CI/CD e melhoria contínua (Marco 9)

**Projeto Integrado P2 — BarberAgenda** — Turma A — Guilherme Ribeiro Zangrande e José Paulo Dassie Felippi

| Versão | Data | Descrição |
|---|---|---|
| v1.0 | 2026-11-18 | Ciclo TDD da RF-09, pipeline GitHub Actions (verde e falha controlada), 2ª análise SonarQube e plano de melhoria |

## 1. Registro de TDD e CI/CD (Apêndice J)

| Etapa | Evidência e descrição |
|---|---|
| Comportamento escolhido | **RF-09:** o cliente só pode cancelar um agendamento com no mínimo 2 horas de antecedência; caso contrário, a API responde **HTTP 422** com mensagem explicativa. A regra não existia na versão 1.1.0 (reservada para esta etapa). |
| RED — teste falhando | Commit `35ce2a2` (`test(tdd-red)`). Testes escritos **antes** da implementação: unidade (`AgendamentoServiceTest`: cancelar 1h59, 1h30 e 30 min antes deve ser recusado; exatamente 2h deve ser aceito) e integração (`CancelamentoAntecedenciaIntegracaoTest`, MockMvc com relógio fixo em 18/11/2026 09:00: cancelar 1h30 antes → 422). `./mvnw test`: **4 falhas pelo motivo esperado** — "Expecting code to raise a throwable" (3) e "Status expected:<422> but was:<200>" (1). Saída: `tdd/01_RED_mvnw_test.log`. |
| GREEN — implementação mínima | Commit `c9c6e4c` (`feat(tdd-green)`). Verificação do prazo em `AgendamentoService.cancelarPeloCliente` e `CancelamentoForaDoPrazoException` → 422 no `TratadorErros`. `./mvnw test`: **58 testes, 0 falhas**. Saída: `tdd/02_GREEN_mvnw_test.log`. |
| REFACTOR — melhoria | Commit `78b44e3` (`refactor(tdd)`). Regra isolada em `PoliticaCancelamento` (constante `ANTECEDENCIA_MINIMA` de 2h, mensagem única), usando o `Clock` injetável; comportamento inalterado. `./mvnw test`: **58 testes, 0 falhas**. Saída: `tdd/03_REFACTOR_mvnw_test.log`. |
| Commits relacionados | `35ce2a2` → `c9c6e4c` → `78b44e3`; versão 1.2.0 (tag `v1.2.0-sistema`, commit `3848e26`) com P02 v1.1 (RF-09, R-12), especificação v1.3 e CT-036 |
| Pipeline — arquivo e gatilho | `.github/workflows/ci.yml` — gatilhos `push` (todas as branches), `pull_request` para `main` e execução manual. Jobs: **testes** (Java 21 com cache do Maven → `./mvnw -B verify`: unidade, integração e JaCoCo), **api** (sobe a aplicação no perfil `test` → Newman) e **interface** (`./mvnw test -Pe2e`, Chrome headless). Relatórios Surefire, JaCoCo, Newman e capturas do Selenium publicados como artefatos. |
| Pipeline — execução aprovada | Run [44441467718](https://github.com/ZangrandeG/barberagenda/actions/runs/44441467718) (push na `main`, commit do workflow): **3 jobs com sucesso**. |
| Pipeline — execução com falha | Branch `demo/falha-pipeline`: commit que altera de propósito o teste do CT-007 para esperar 20 horários em vez de 19 (**demonstração controlada — não é defeito do sistema e não foi registrada como defeito**). Run [44441895872](https://github.com/ZangrandeG/barberagenda/actions/runs/44441895872): **falhou como planejado** — job "Unidade + integração + cobertura" reprovado (`Expected size: 20 but was: 19`, trecho em `cicd/run_44441895872_falha_trecho.txt`); jobs de API e interface pulados por dependerem dele. |
| Pipeline — correção | Commit seguinte na mesma branch desfazendo a quebra. Run [44442093641](https://github.com/ZangrandeG/barberagenda/actions/runs/44442093641): **3 jobs com sucesso**. A branch de demonstração não foi integrada à `main` (fica no repositório como evidência). |
| Aprendizados e melhoria | O teste escrito antes obrigou a definir o limite exato (2h é permitido; 1h59 não) e o código HTTP (422) antes de programar. O relógio injetável permitiu testar uma regra dependente da hora atual a qualquer momento — já a execução manual do CT-036 só é possível em horário comercial (ficou **Bloqueada** quando executada às 23h). O pipeline barra a integração de mudanças que quebram testes, como a demonstração mostrou. |

## 2. Análise de qualidade: linha de base × final (SonarQube Community Build 26.11)

| Medida | Linha de base (Marco 5, v1.1.0) | Final (Marco 9, v1.2.0) | Variação |
|---|---|---|---|
| Bugs | 3 | **0** | −3 |
| Vulnerabilidades | 2 | 2 | = (justificadas, ver abaixo) |
| Code smells | 0 | 0 | = |
| Cobertura | 38,9% | **72,3%** | +33,4 p.p. |
| Cobertura de linhas / ramos | 36,4% / 50,9% | 74,4% / 62,7% | +38,0 / +11,8 p.p. |
| Duplicação | 0,0% | 0,0% | = |
| Dívida técnica | 0 min | 0 min | = |
| Nota de confiabilidade | D | **A** | melhorou |
| Nota de segurança | D | D | = |
| Nota de manutenibilidade | A | A | = |
| Testes considerados | 52 (unidade) | 58 (unidade + integração) | +6 |
| Quality gate (Sonar way, código novo) | OK (sem código novo) | **OK** (cobertura do código novo 95,8%) | — |

Ambas as análises: `./mvnw [clean] verify sonar:sonar` no SonarQube local; exportações em `entrega/11_METRICAS_E_QUALIDADE/sonar_baseline/` e `sonar_final/` (`resumo.md`, `medidas.json`, `problemas.json`, `quality_gate.json`, log).

**O que mudou e por quê:**
- **3 bugs (`java:S8696`)** — comparação `getDayOfWeek() == DayOfWeek.SUNDAY`. Como `DayOfWeek` é enum, o `==` já era correto (falso positivo da regra), mas a comparação foi reescrita com `equals()` para eliminar o alerta, sem mudança de comportamento (testes de regressão aprovados). A 2ª análise intermediária apontou o mesmo padrão no código de teste (`TesteE2EBase`), que também foi ajustado.
- **Cobertura** — subiu porque os testes de integração com `@SpringBootTest` (criados no TDD) passaram a exercitar controllers, segurança e carga de dados, que os testes de unidade não alcançam.
- **2 vulnerabilidades mantidas** — `java:S3330` (cookie `XSRF-TOKEN` sem `HttpOnly`) e `java:S4502` (proteção CSRF restrita). São decisões de projeto documentadas: o JavaScript precisa ler o cookie para enviar o token CSRF, e a proteção é exigida justamente nas alterações feitas com sessão; as rotas públicas não usam sessão e as chamadas HTTP Basic não usam cookie. Ficam como risco aceito no plano de melhoria (ação M-03).

## 3. Plano de melhoria contínua

| ID | Ação | Origem | Prioridade | Responsável | Critério de verificação |
|---|---|---|---|---|---|
| M-01 | Executar a aceitação (CA-01 a CA-04) e a usabilidade (TNF-08) com pessoa externa e tratar o que ela apontar | P09 pendente | Alta | José Paulo Dassie Felippi | 4 decisões registradas no P09; RNF-05 com resultado; ajustes registrados como issues |
| M-02 | Executar o CT-036 manualmente em horário comercial | CT-036 bloqueado | Média | José Paulo Dassie Felippi | Execução registrada como Aprovado/Reprovado em `dados/execucoes.csv` |
| M-03 | Reavaliar as vulnerabilidades S3330/S4502: aplicar `SameSite=Strict` e cabeçalho de origem nas alterações administrativas, ou registrar a aceitação formal do risco no SonarQube | 2ª análise Sonar | Média | Guilherme Ribeiro Zangrande | Nota de segurança ≥ B, ou risco aceito com justificativa na ferramenta |
| M-04 | Limitar tentativas na consulta por código de acesso (ex.: 10 por minuto por IP) | Problemas conhecidos (README) | Média | Guilherme Ribeiro Zangrande | Teste automatizado: a 11ª tentativa no mesmo minuto recebe HTTP 429 |
| M-05 | Testar concorrência real de agendamento (dois pedidos simultâneos para o mesmo horário) | Fora do escopo do P02 | Baixa | Guilherme Ribeiro Zangrande | Teste com 2 threads: exatamente 1 resposta 201 e 1 resposta 409 |
| M-06 | Incluir a análise do SonarQube no pipeline (SonarCloud, se o repositório for público) e falhar o build quando o quality gate reprovar | Marco 9 | Baixa | Guilherme Ribeiro Zangrande | Job "qualidade" no `ci.yml`; execução com o quality gate visível no GitHub |
| M-07 | Validar o perfil PostgreSQL (docker-compose) | Problemas conhecidos (README) | Baixa | José Paulo Dassie Felippi | Suítes de unidade, integração e API aprovadas com `dev,postgres` |
