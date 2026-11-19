# SonarQube — sonar_baseline

Exportado em 2026-11-18 21:58 por `scripts/sonar_relatorio.py`.

- Servidor: SonarQube local http://localhost:9000 (Community Build)
- Análise: 2026-11-18T21:57:40-0300 — tarefa a4a943ec-4b03-4502-90fc-6cdb04cbf7cc — situação SUCCESS
- Quality gate (Sonar way): **OK**

## Medidas

| Medida | Valor |
|---|---|
| Bugs | 3 |
| Vulnerabilidades | 2 |
| Pontos sensíveis de segurança | 0 |
| Code smells | 0 |
| Cobertura (%) | 38.9 |
| Cobertura de linhas (%) | 36.4 |
| Cobertura de ramos (%) | 50.9 |
| Linhas duplicadas (%) | 0.0 |
| Blocos duplicados | 0 |
| Dívida técnica (min) | 0 |
| Razão de dívida técnica (%) | 0.0 |
| Nota de confiabilidade | D |
| Nota de segurança | D |
| Nota de manutenibilidade | A |
| Linhas de código | 1756 |
| Complexidade ciclomática | 241 |
| Testes de unidade | 52 |

## Problemas em aberto (5)

| Severidade | Quantidade |
|---|---|
| CRITICAL | 4 |
| MINOR | 1 |

| Tipo | Quantidade |
|---|---|
| BUG | 3 |
| VULNERABILITY | 2 |

| Regra | Quantidade | Exemplo |
|---|---|---|
| `java:S8696` | 3 | src/main/java/br/com/barberagenda/seed/CargaDadosFicticios.java:118 — Use ".equals()" instead of "==" or "!=" to compare objects of value-based types. |
| `java:S3330` | 1 | src/main/java/br/com/barberagenda/security/SecurityConfig.java:75 — Make sure creating this cookie without the "HttpOnly" flag is safe. |
| `java:S4502` | 1 | src/main/java/br/com/barberagenda/security/SecurityConfig.java:77 — Make sure disabling Spring Security's CSRF protection is safe here. |
