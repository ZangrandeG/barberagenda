# P10 — Métricas e indicadores (Marco 8)

**Projeto Integrado P2 — BarberAgenda 1.2.0** — Turma A — Guilherme Ribeiro Zangrande e José Paulo Dassie Felippi

| Versão | Data | Descrição |
|---|---|---|
| v1.0 | 2026-11-18 | 8 métricas da seção 9.13 calculadas com os dados reais ao final do Marco 9 |

**Fonte dos dados:** `dados/casos.json` (36 casos manuais), `dados/testes_complementares.json` (8 testes não funcionais e 4 cenários de aceitação), `dados/requisitos.json` (14 requisitos), `dados/execucoes.csv` (46 execuções: EX-001 a EX-046) e `dados/defeitos.csv` (exportado do GitHub Issues). **Cálculo:** `python scripts/metricas.py` (valores em `metricas/metricas.json`, gráficos em `metricas/*.png`); as mesmas fórmulas estão na aba Métricas da planilha P05. **Regra de contagem:** o resultado de cada caso é o da execução mais recente; "executado" = Aprovado ou Reprovado (Bloqueado e Não executado não contam).

## 1. Painel de métricas (Apêndice K)

| Indicador | Valor | Cálculo | Fonte dos dados | Interpretação |
|---|---|---|---|---|
| Percentual de execução | **87,5%** | 42 executados / 48 planejados × 100 | P05 (Casos, Execuções) | Ver 2.1 |
| Taxa de aprovação | **100%** | 42 aprovados / 42 executados × 100 | P05 | Ver 2.2 |
| Taxa de reprovação | **0%** | 0 reprovados / 42 executados × 100 | P05 | Ver 2.3 |
| Cobertura de requisitos | **85,7%** | 12 requisitos com teste executado / 14 no escopo × 100 | P05 (Requisitos) | Ver 2.4 |
| Taxa de automação | **100%** | 39 automatizados / 39 planejados para automação × 100 | P04/P05 (Casos) | Ver 2.5 |
| Defeitos por severidade | **0** em todas (Crítica 0, Alta 0, Média 0, Baixa 0) | contagem por categoria | GitHub Issues (`exportar_defeitos.py`) | Ver 2.6 |
| Defeitos por status | **0** em todos os status | contagem por estado | GitHub Issues | Ver 2.7 |
| Taxa de reabertura | **não se aplica** (0 reabertos / 0 retestados) | reabertos / retestados × 100 | GitHub Issues | Ver 2.8 |

**Figura 1** — Resultado atual dos 48 casos planejados: `metricas/01_resultado_dos_casos.png`
**Figura 2** — Indicadores percentuais: `metricas/02_indicadores_percentuais.png`
**Figura 3** — Defeitos por severidade: `metricas/03_defeitos_por_severidade.png`
**Figura 4** — Defeitos por status: `metricas/04_defeitos_por_status.png`

## 2. Interpretação

### 2.1 Percentual de execução — 87,5%
Dos 48 casos planejados, 42 foram executados. Os 6 restantes são: **5 que dependem de uma pessoa externa ao grupo** (4 cenários de aceitação e o teste de usabilidade, ainda não aplicados) e **1 bloqueado** (CT-036, que exige horário comercial porque cria um agendamento para menos de 2 horas à frente; foi tentado às 23h). Os 36 casos manuais e os 7 testes não funcionais automatizáveis foram executados — o avanço só depende agora de atividades humanas planejadas (ações M-01 e M-02 do P11).

### 2.2 Taxa de aprovação — 100%
Todos os 42 casos executados obtiveram o resultado esperado na primeira execução. O número é alto, mas precisa ser lido com o contexto: o sistema é pequeno, foi construído pelo próprio grupo com a especificação já pensada para os testes, e os problemas mais relevantes foram encontrados **antes** da execução dos casos, por revisão de código e análise estática (rota de restauração sem autenticação, consulta por código sequencial e 3 alertas do SonarQube), e corrigidos nas versões 1.0.1, 1.1.0 e 1.2.0. Não indica ausência de defeitos, e sim que, no escopo e com as técnicas aplicadas, nenhuma falha foi observada.

### 2.3 Taxa de reprovação — 0%
Complementar à anterior: nenhuma execução falhou. Nenhum defeito foi inventado para "ter o que registrar" (manual, seção 9.7). As únicas falhas registradas no projeto foram: a do script de execução assistida no ensaio (erro do script, não do sistema — por isso o ensaio foi feito fora do registro oficial) e a falha **proposital** do pipeline (demonstração de CI, seção 9.15), nenhuma delas defeito do sistema.

### 2.4 Cobertura de requisitos — 85,7%
12 dos 14 requisitos têm teste executado. Faltam: **RNF-05** (usabilidade, depende do participante externo) e **RF-09**, cujo caso manual (CT-036) ficou bloqueado. Ressalva: o RF-09 está coberto pelos testes automatizados de unidade e de integração criados no TDD (4 métodos de teste, 6 execuções com os parametrizados, aprovados em todas as rodadas e no pipeline); considerando também a automação, a cobertura seria de 13/14 = 92,9%. A métrica oficial usa apenas os casos do catálogo.

### 2.5 Taxa de automação — 100%
Todos os 39 casos marcados como candidatos à automação têm teste automatizado em todos os níveis planejados: 58 testes de unidade e integração (JUnit/Mockito/MockMvc), 26 requisições com 63 asserções no Postman/Newman e 11 testes Selenium (executados em 4 combinações de navegador e resolução). Os 9 casos não candidatos são os que exigem pessoas (aceitação e usabilidade) ou têm baixo valor de automação (justificativas no P04). A automação permite repetir toda a regressão em minutos e roda no pipeline a cada envio de código.

### 2.6 Defeitos por severidade — nenhum
Não houve defeito registrado no GitHub Issues durante a execução dos testes dinâmicos. O processo está pronto para registrá-los (modelo do Apêndice G, etiquetas de severidade, prioridade e status, exportação automática), e as correções feitas antes dos testes estão documentadas como achados de revisão/análise estática no `docs/PROGRESSO.md` e no P11.

### 2.7 Defeitos por status — nenhum
Sem defeitos, não há itens em aberto: o critério de saída "nenhum defeito Crítico ou Alto aberto" (P03, seção 13) está atendido.

### 2.8 Taxa de reabertura — não se aplica
A fórmula exige defeitos retestados (denominador). Com zero defeitos retestados, a taxa é indefinida (e não 0%): não há evidência de correções incompletas porque não houve correções de defeitos registrados.

## 3. Indicadores complementares de qualidade (SonarQube e cobertura)

| Indicador | Linha de base | Final |
|---|---|---|
| Bugs | 3 | 0 |
| Vulnerabilidades | 2 | 2 (decisões de projeto justificadas) |
| Code smells / duplicação | 0 / 0% | 0 / 0% |
| Cobertura (Sonar) | 38,9% | 72,3% |

Detalhes e comparação no P11, seção 2.
