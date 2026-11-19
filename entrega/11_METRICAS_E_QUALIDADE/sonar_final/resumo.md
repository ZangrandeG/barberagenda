# SonarQube — sonar_final

Exportado em 2026-11-18 23:06 por `scripts/sonar_relatorio.py`.

- Servidor: SonarQube local http://localhost:9000 (Community Build)
- Análise: 2026-11-18T23:06:15-0300 — tarefa 3acf3263-3cef-481d-a5c7-a5e62611cb87 — situação SUCCESS
- Quality gate (Sonar way): **OK**

## Medidas

| Medida | Valor |
|---|---|
| Bugs | 0 |
| Vulnerabilidades | 2 |
| Pontos sensíveis de segurança | 0 |
| Code smells | 0 |
| Cobertura (%) | 72.3 |
| Cobertura de linhas (%) | 74.4 |
| Cobertura de ramos (%) | 62.7 |
| Linhas duplicadas (%) | 0.0 |
| Blocos duplicados | 0 |
| Dívida técnica (min) | 0 |
| Razão de dívida técnica (%) | 0.0 |
| Nota de confiabilidade | A |
| Nota de segurança | D |
| Nota de manutenibilidade | A |
| Linhas de código | 1813 |
| Complexidade ciclomática | 245 |
| Testes de unidade | 58 |

## Problemas em aberto (2)

| Severidade | Quantidade |
|---|---|
| MINOR | 1 |
| CRITICAL | 1 |

| Tipo | Quantidade |
|---|---|
| VULNERABILITY | 2 |

| Regra | Quantidade | Exemplo |
|---|---|---|
| `java:S3330` | 1 | src/main/java/br/com/barberagenda/security/SecurityConfig.java:75 — Make sure creating this cookie without the "HttpOnly" flag is safe. |
| `java:S4502` | 1 | src/main/java/br/com/barberagenda/security/SecurityConfig.java:77 — Make sure disabling Spring Security's CSRF protection is safe here. |
