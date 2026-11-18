# P04 — Catálogo de casos de teste

**Projeto Integrado P2 — Testes e Qualidade de Software — UNISAGRADO 2026**
**Sistema:** BarberAgenda 1.1.0 (tag `v1.1.0-sistema-base`)
**Grupo:** Turma A — Guilherme Ribeiro Zangrande (RA 23110757) e José Paulo Dassie Felippi (RA 24111563)

| Versão | Data | Descrição |
|---|---|---|
| v1.0 | 2026-11-18 | Primeira versão: 35 casos manuais com partições, valores limite, transição de estados e tabela de decisão |

> **Arquivo gerado.** Este documento e a planilha P05 são gerados por `scripts/gerar_artefatos.py` a partir de `dados/casos.json`, `dados/requisitos.json` e `dados/riscos.json`. Para alterar um caso, edite o JSON e rode `python scripts/gerar_artefatos.py`.

## 1. Convenções para a execução

**Pré-condição padrão (PC-PADRÃO):** aplicação em execução em `http://localhost:8080` (perfil `dev` ou `test`) e dados restaurados com `bash scripts/reset-dados.sh` (ou `scripts\reset-dados.ps1`) **imediatamente antes de cada caso**. Assim cada caso é independente dos demais.

**Datas relativas** (calculadas no dia da execução e anotadas na evidência):

| Símbolo | Significado |
|---|---|
| D | Data da execução |
| DF1, DF2, DF3 | 1º, 2º e 3º dias de funcionamento (segunda a sábado) depois de D |
| ONTEM | D − 1 |
| DOM | Próximo domingo depois de D |
| D+30, D+31 | D somado a 30 e a 31 dias corridos |
| `<AAAAMMDD>` | Data da execução, usada para criar e-mails únicos (ex.: `marina.20261120@exemplo.com`) |

**Massa de dados usada pelos casos** (`docs/ESPECIFICACAO_SISTEMA.md`, seção 6):

| Código | Cliente | Barbeiro | Serviço | Quando | Status |
|---|---|---|---|---|---|
| SEMENTE2 | ana.rocha@exemplo.com | Carlos Navalha | Corte de cabelo (30 min) | DF1 10:00 | AGENDADO |
| SEMENTE3 | bruno.lima@exemplo.com | Rafael Tesoura | Corte e barba (60 min) | DF1 14:00–15:00 | AGENDADO |
| SEMENTE4 | camila.prado@exemplo.com | Carlos Navalha | Barba (30 min) | DF2 09:30 | CANCELADO |
| SEMENTE5 | daniel.alves@exemplo.com | Rafael Tesoura | Corte de cabelo | dia de funcionamento anterior a D, 11:00 | CONCLUIDO |
| SEMENTE6 | eduarda.costa@exemplo.com | Carlos Navalha | Sobrancelha (15 min) | DF2 16:00–16:15 | AGENDADO |

Barbeiro inativo: Diego Máquina. Serviço inativo: Relaxamento capilar (90 min).

**Casos executados pela API:** algumas regras não podem ser violadas pela tela (ela só oferece horários válidos). Esses casos são executados com o Postman ou com `curl`, enviando JSON para `http://localhost:8080`. Os ids de barbeiros e serviços mudam a cada restauração e devem ser obtidos antes, em `GET /api/barbeiros` e `GET /api/servicos` (inativos: `GET /api/admin/barbeiros` e `/api/admin/servicos` com `admin:admin123`). Formato da data e hora: `AAAA-MM-DDTHH:MM:SS`.

**Resultado de cada execução:** Aprovado, Reprovado, Bloqueado ou Não executado (registro no P06).

## 2. Técnicas aplicadas

### 2.1 Particionamento de equivalência e valores limite por regra

| Regra | Variável | Classes válidas | Classes inválidas | Valores limite testados | Casos |
|---|---|---|---|---|---|
| RN-01 | Tamanho do nome | 3 a 60 caracteres | menos de 3; mais de 60 | 2 ✗, 3 ✓, 60 ✓, 61 ✗ | CT-002, CT-003 |
| RN-02 | Telefone | só dígitos, 10 ou 11 | menos de 10 dígitos; mais de 11; com caracteres não numéricos | 9 ✗, 10 ✓, 11 ✓, 12 ✗; com hífens ✗ | CT-002, CT-004 |
| RN-03 | E-mail | formato `usuario@dominio.ext` ainda não cadastrado | sem `@`; sem domínio de topo; já cadastrado (qualquer caixa) | — | CT-001, CT-005, CT-006 |
| RN-04 | Dia e horário | segunda a sábado, início ≥ 09:00 e término ≤ 19:00 | domingo; início < 09:00; término > 19:00 | início 08:30 ✗ / 09:00 ✓; término 19:00 ✓ / 19:30 ✗ (serviço de 60 min às 18:00 e 18:30); último início de serviço de 30 min 18:30 ✓ | CT-007, CT-011, CT-012, CT-014 |
| RN-05 | Minuto de início | 00 ou 30 | qualquer outro minuto | 10:01 ✗, 10:15 ✗ (10:00 e 10:30 ✓ nos demais casos) | CT-013 |
| RN-06 | Momento do início | depois de agora e data ≤ D+30 | passado (antes de agora); data > D+30 | ONTEM ✗; hoje às 09:00 depois das 09:30 ✗; D+30 ✓; D+31 ✗ | CT-009, CT-015, CT-016 |
| RN-07 | Intervalo × agendamentos do barbeiro | sem interseção com `AGENDADO` do mesmo barbeiro (inclui encostar); outro barbeiro | interseção com `AGENDADO` do mesmo barbeiro | término = início do existente ✓; início = término do existente ✓; 30 min de interseção no início e no fim ✗ | CT-008, CT-019, CT-020 |
| RN-08 | Agendamentos ativos do cliente antes do pedido | 0 a 2 | 3 ou mais | 3º pedido ✓; 4º pedido ✗; após cancelar 1 ✓ | CT-021, CT-022 |
| RN-09 | Duração do serviço | 15 a 180, múltiplo de 15 | < 15; > 180; não múltiplo de 15 | 14 ✗, 15 ✓, 20 ✗, 180 ✓, 195 ✗ | CT-030, CT-031 |
| RN-09 | Preço do serviço | R$ 1,00 a R$ 1.000,00 | < 1,00; > 1.000,00 | 0,99 ✗, 1,00 ✓, 1.000,00 ✓, 1.000,01 ✗ | CT-030, CT-031 |
| RN-10 | Situação de barbeiro/serviço | ativo | inativo | — | CT-017, CT-032 |
| RN-11 | Credencial | administrador autenticado | sem credencial; senha errada | — | CT-027, CT-028, CT-029 |

### 2.2 Transição de estados do agendamento

| Estado atual | Evento | Próximo estado / resposta | Casos |
|---|---|---|---|
| (novo) | Agendar | AGENDADO | CT-010 |
| AGENDADO | Cancelar (cliente) | CANCELADO | CT-022, CT-025 |
| AGENDADO | Concluir (administrador) | CONCLUIDO | CT-034 |
| CANCELADO | Cancelar | HTTP 409, permanece CANCELADO | CT-026 |
| CONCLUIDO | Cancelar | HTTP 409, permanece CONCLUIDO | CT-026 |
| CANCELADO | Concluir | HTTP 409, permanece CANCELADO | CT-035 |

### 2.3 Tabela de decisão — consulta pelo cliente (RF-05)

| Regra | Código existe? | E-mail é o do agendamento? | Resultado | Casos |
|---|---|---|---|---|
| 1 | Sim (inclusive em minúsculas) | Sim | Exibe o agendamento | CT-023 |
| 2 | Sim | Não | "Agendamento não encontrado..." | CT-024 (a) |
| 3 | Não | Sim | "Agendamento não encontrado..." | CT-024 (b) |
| 4 | Não (número sequencial) | Sim | "Agendamento não encontrado..." | CT-024 (c) |
