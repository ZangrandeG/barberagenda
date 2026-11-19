# P08 — Testes de integração/API (Postman + Newman) — Marco 6

**Projeto Integrado P2 — BarberAgenda 1.1.0** — Turma A — Guilherme Ribeiro Zangrande e José Paulo Dassie Felippi

| Versão | Data | Descrição |
|---|---|---|
| v1.0 | 2026-11-18 | Coleção com 26 requisições e 63 asserções; execução com Newman |

## 1. O que é verificado

A comunicação real entre os componentes: requisição HTTP → controller → regras (service) → banco H2 → resposta JSON (manual, seção 9.9). Para cada requisição, a coleção verifica:

- **código de status** (201, 200, 204, 400, 401, 403, 404, 409);
- **contrato básico**: campos e tipos da resposta (ex.: `id` numérico, `codigoAcesso` com 8 caracteres do alfabeto sem ambíguos, cabeçalho `Location`);
- **mensagens de erro** no formato padronizado `{status, erro, mensagem, campos}` e **ausência de stack trace**;
- **encadeamento de dados**: o cliente cadastrado é usado no agendamento; o código de acesso devolvido é usado na consulta e no cancelamento; os horários de conflito são calculados a partir do agendamento SEMENTE3;
- **preparação e limpeza**: a coleção começa e termina restaurando a massa fictícia (`POST /api/dev/reset`, como administrador) e cria e-mails únicos por execução.

## 2. Arquivos

| Arquivo | Conteúdo |
|---|---|
| `BarberAgenda.postman_collection.json` | Coleção (formato Postman v2.1), importável no Postman |
| `BarberAgenda.postman_environment.json` | Ambiente: `baseUrl`, `adminUsuario`, `adminSenha` (credencial **fictícia**) |
| `relatorios/newman_2026-11-18.html` | Relatório HTML (htmlextra) |
| `relatorios/newman_2026-11-18.xml` | Relatório JUnit (para o pipeline) |
| `relatorios/newman_cli_2026-11-18.txt` | Saída completa do terminal |

Fonte da coleção: `scripts/gerar_colecao_postman.py` (gera os dois JSON em `postman/`).

## 3. Como executar

```bash
java -jar target/barberagenda-1.2.0.jar --spring.profiles.active=test     # terminal 1
npm install -g newman newman-reporter-htmlextra                          # uma vez
newman run postman/BarberAgenda.postman_collection.json \
       -e postman/BarberAgenda.postman_environment.json \
       --reporters cli,junit,htmlextra                                    # terminal 2
```

## 4. Resultado da execução (2026-11-18)

Newman 6.2.3, aplicação no perfil `test`, versão 1.1.0:

| Item | Executados | Falhas |
|---|---|---|
| Requisições | 26 | 0 |
| Scripts de teste | 26 | 0 |
| Asserções | 63 | 0 |

Duração total: 2,1 s.

## 5. Requisições, casos e requisitos

| Pasta | Requisição | Caso / requisito | Esperado |
|---|---|---|---|
| 00 Preparação | Restaurar dados; listar barbeiros e serviços ativos | RN-10 | 200; inativos não listados |
| 01 Clientes | Cadastrar cliente válido | CT-001 / RF-01 | 201, contrato, `Location` |
| | E-mail em formato inválido | CT-005 / RF-01 | 400, `campos.email` |
| | E-mail já cadastrado (maiúsculas) | CT-006 / RF-01 | 409 |
| 02 Agendamento encadeado | Agendar para o cliente recém-cadastrado | CT-010 / RF-03 | 201, código de acesso, término = início + 30 min |
| | Consultar pelo código e e-mail | CT-023 / RF-05 | 200, AGENDADO |
| | Cancelar | CT-025 / RF-05 | 200, CANCELADO |
| | Cancelar de novo | CT-026 / RF-05 | 409 |
| 03 Regras de agendamento | Sobreposição com o mesmo barbeiro | CT-019 / RF-04 | 409 |
| | Horário encostado no término | CT-020 / RF-04 | 201 |
| | Início às 08:30 | CT-012 / RF-03 | 400, `campos.dataHoraInicio` |
| | E-mail não cadastrado | CT-018 / RF-03 | 404 |
| 04 Consulta | Código certo, e-mail de outro cliente; número sequencial | CT-024 / RF-05 | 404, mesma mensagem, sem dados de terceiros |
| 05 Segurança | Admin e clientes sem credenciais; cadastro sem credenciais; serviço não criado | CT-029 / RF-06, RNF-02 | 401, 401, 403; nada criado |
| 06 Administração | Cadastrar serviço; duração 20; excluir; agenda do dia | RF-07, CT-031, RF-08 | 201, 400, 204, 200 sem códigos de acesso |
| 07 Limpeza | Restaurar dados | — | 200 |

**Positivo e negativo por operação crítica:** cadastro de cliente (1 positivo, 2 negativos), agendamento (2 positivos, 3 negativos), consulta (1 positivo, 2 negativos), cancelamento (1 positivo, 1 negativo), cadastro de serviço (1 positivo, 2 negativos), área administrativa (1 positivo, 3 negativos sem credencial).
