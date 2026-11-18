# Especificação do sistema BarberAgenda — versão 1.0

| Versão | Data | Descrição |
|---|---|---|
| v1.0 | 2026-11-18 | Especificação da versão base (tag `v1.0-sistema-base`) |
| v1.1 | 2026-11-18 | `POST /api/dev/reset` passa a exigir administrador (versão 1.0.1) |

Documento de referência para os requisitos (P02) e para os casos de teste (P04). Descreve o comportamento **implementado** na versão base.

## 1. Perfis de usuário

| Perfil | Acesso | Autenticação |
|---|---|---|
| Cliente | Páginas públicas (`/index.html`, `/cadastro.html`, `/agendar.html`, `/consulta.html`) e API pública | Nenhuma. O cliente se identifica pelo e-mail cadastrado. |
| Administrador | Páginas `/admin/**` e API `/api/admin/**` | Login por formulário (sessão) nas páginas; sessão ou HTTP Basic na API. |

## 2. Regras de negócio

| ID | Regra | Onde é verificada | Resposta quando violada |
|---|---|---|---|
| RN-01 | Nome do cliente obrigatório, de 3 a 60 caracteres (espaços nas extremidades são ignorados). | `ClienteRequest` | 400, campo `nome` |
| RN-02 | Telefone somente com dígitos, 10 ou 11 dígitos. | `ClienteRequest` | 400, campo `telefone` |
| RN-03 | E-mail em formato válido (`usuario@dominio.ext`) e único entre clientes, sem diferenciar maiúsculas de minúsculas. | `ClienteRequest` e `ClienteService` | 400, campo `email` (formato); 409 (repetido) |
| RN-04 | Atendimento de segunda a sábado, das 09:00 às 19:00. O serviço precisa terminar até 19:00. Domingo fechado. | `RegrasAgendamento.validarFuncionamento` | 400, campo `dataHoraInicio` |
| RN-05 | O início do agendamento deve cair em intervalos de 30 minutos (minutos 00 ou 30, segundos 00). | `RegrasAgendamento.validarIntervalo` | 400, campo `dataHoraInicio` |
| RN-06 | Não é permitido agendar em data/horário que já passou. A data do agendamento pode ser no máximo 30 dias após a data de hoje (hoje + 30 é aceito; hoje + 31 é recusado). | `RegrasAgendamento.validarAntecedencia` | 400, campo `dataHoraInicio` |
| RN-07 | Um barbeiro não pode ter dois agendamentos `AGENDADO` com horários sobrepostos. Intervalos encostados (um termina 10:30 e outro começa 10:30) não se sobrepõem. | `AgendamentoService.agendar` | 409 |
| RN-08 | Um cliente pode ter no máximo 3 agendamentos com status `AGENDADO` ao mesmo tempo (o 4º é recusado). | `AgendamentoService.agendar` | 409 |
| RN-09 | Serviço: duração de 15 a 180 minutos, múltipla de 15; preço de R$ 1,00 a R$ 1.000,00, com até 2 casas decimais. | `ServicoRequest` | 400, campos `duracaoMinutos` / `preco` |
| RN-10 | Somente barbeiros e serviços ativos recebem agendamentos e aparecem para o cliente. | `AgendamentoService` e consultas públicas | 400, campo `barbeiroId` / `servicoId` |
| RN-11 | Área administrativa somente com autenticação. Sem credenciais: consultas (GET) respondem 401; alterações (POST, PUT, PATCH, DELETE) respondem 403, porque o token CSRF é verificado antes da autenticação. Com sessão do navegador e token CSRF ausente ou inválido: 403. Com HTTP Basic e senha errada: 401. Páginas `/admin/**` sem login redirecionam para o login. | `SecurityConfig` | 401 / 403 / 302 |

**Ordem das verificações ao criar um agendamento:** cliente, barbeiro e serviço existem (404) → barbeiro e serviço ativos, RN-10 (400) → RN-06, RN-04, RN-05, nesta ordem (400) → limite de ativos, RN-08 (409) → sobreposição, RN-07 (409).

**Fuso horário:** todas as datas e horas são locais da barbearia (`America/Sao_Paulo`), sem indicação de fuso no JSON.

**Fora da versão base (reservado para a etapa de TDD):** regra de antecedência mínima para cancelamento pelo cliente.

## 3. Status de agendamento

| Status | Significado | Transições permitidas |
|---|---|---|
| `AGENDADO` | Horário reservado | → `CANCELADO` (cliente) ou → `CONCLUIDO` (administrador) |
| `CANCELADO` | Cancelado pelo cliente | nenhuma |
| `CONCLUIDO` | Atendimento realizado | nenhuma |

Tentar cancelar ou concluir um agendamento que não está `AGENDADO` retorna 409.

## 4. API REST

Base: `http://localhost:8080`. Corpo e respostas em JSON (UTF-8). Datas: `AAAA-MM-DD`; data e hora: `AAAA-MM-DDTHH:MM:SS`.

### 4.1 Pública

| Método e rota | Descrição | Sucesso | Erros |
|---|---|---|---|
| `POST /api/clientes` | Cadastra cliente `{nome, telefone, email}` | 201 + `Location` | 400, 409 |
| `GET /api/barbeiros` | Barbeiros ativos | 200 | — |
| `GET /api/servicos` | Serviços ativos | 200 | — |
| `GET /api/horarios-disponiveis?barbeiroId=&servicoId=&data=` | Horários de início livres (`["09:00", ...]`). Data de domingo, passada ou além de 30 dias devolve lista vazia. | 200 | 400 (parâmetro ausente/inválido; barbeiro ou serviço inativo), 404 |
| `POST /api/agendamentos` | Agenda `{emailCliente, barbeiroId, servicoId, dataHoraInicio}` | 201 + `Location` | 400, 404, 409 |
| `GET /api/agendamentos/{id}?email=` | Consulta pelo cliente (o e-mail precisa ser o do agendamento) | 200 | 400, 404 |
| `PATCH /api/agendamentos/{id}/cancelar` | Cancela `{email}` | 200 | 400, 404, 409 |

### 4.2 Administrativa (exige perfil ADMIN)

Na coluna Erros, "401" nas rotas de alteração significa credencial inválida via HTTP Basic. Sem nenhuma credencial, as alterações respondem 403 (ver RN-11).

| Método e rota | Descrição | Sucesso | Erros |
|---|---|---|---|
| `GET /api/clientes` | Lista clientes (dados pessoais) | 200 | 401 |
| `GET /api/clientes/{id}` | Consulta cliente | 200 | 401, 404 |
| `GET /api/admin/barbeiros` | Todos os barbeiros (ativos e inativos) | 200 | 401 |
| `POST /api/admin/barbeiros` | Cadastra `{nome, ativo}` | 201 | 400, 401 |
| `PUT /api/admin/barbeiros/{id}` | Atualiza `{nome, ativo}` | 200 | 400, 401, 404 |
| `DELETE /api/admin/barbeiros/{id}` | Exclui (recusado se houver agendamentos — desative em vez de excluir) | 204 | 401, 404, 409 |
| `GET /api/admin/servicos` | Todos os serviços | 200 | 401 |
| `POST /api/admin/servicos` | Cadastra `{nome, duracaoMinutos, preco, ativo}` | 201 | 400, 401 |
| `PUT /api/admin/servicos/{id}` | Atualiza | 200 | 400, 401, 404 |
| `DELETE /api/admin/servicos/{id}` | Exclui (recusado se houver agendamentos) | 204 | 401, 404, 409 |
| `GET /api/admin/agenda?barbeiroId=&data=` | Agenda do barbeiro no dia (todos os status) | 200 | 400, 401, 404 |
| `PATCH /api/admin/agendamentos/{id}/concluir` | Marca como concluído | 200 | 401, 404, 409 |
| `GET /api/admin/sessao` | Usuário autenticado | 200 | 401 |
| `POST /admin/login` | Login por formulário (`username`, `password`) | 200 `{login}` | 401 |
| `POST /admin/logout` | Encerra a sessão | 204 | 403 (sem CSRF) |

### 4.3 Apoio aos testes (somente perfis `dev` e `test`; exige perfil ADMIN)

| Método e rota | Descrição | Sucesso | Erros |
|---|---|---|---|
| `POST /api/dev/reset` | Apaga barbeiros, serviços, clientes e agendamentos e recarrega a massa fictícia | 200 `{barbeiros, servicos, clientes, agendamentos}` | 403 (sem credenciais ou sessão sem token CSRF), 401 (HTTP Basic com senha errada) |

Em outros perfis a rota não existe (404).

### 4.4 Formato de erro

```json
{ "status": 400, "erro": "Bad Request", "mensagem": "Existem campos inválidos.", "campos": { "nome": "O nome deve ter entre 3 e 60 caracteres." } }
```

O objeto `campos` é sempre enviado (vazio quando o erro não se refere a um campo). Nenhuma resposta de erro contém stack trace.

## 5. Decisões de projeto

| Decisão | Motivo |
|---|---|
| `GET /api/clientes` e `GET /api/clientes/{id}` exigem administrador. | Expõem nome, telefone e e-mail de todos os clientes (exposição indevida de dados pessoais). |
| O agendamento identifica o cliente pelo e-mail (`emailCliente`), e não pelo id. | O cliente não tem login; o e-mail é o dado que ele conhece. O id do cliente não é exposto publicamente. |
| Consulta e cancelamento exigem código **e** e-mail; e-mail divergente responde 404. | Evita que alguém consulte agendamentos de outras pessoas apenas variando o código, sem revelar se o código existe. |
| 400 para regras que dependem só do pedido; 409 para conflito com dados existentes (e-mail repetido, horário ocupado, limite de ativos, status que não permite a operação). | Diferencia erro de preenchimento de conflito de estado. |
| Exclusão de barbeiro/serviço com agendamentos é recusada (409). | Preserva o histórico; a desativação (`ativo=false`) atende ao caso de uso. |
| Bloqueio pessimista do barbeiro ao criar agendamento. | Impede que dois pedidos simultâneos reservem o mesmo horário. |
| `Clock` injetável. | Permite fixar o "agora" nos testes de regras que dependem de data e hora. |
| CSRF por cookie `XSRF-TOKEN` + cabeçalho `X-XSRF-TOKEN` nas alterações administrativas feitas com sessão; requisições com HTTP Basic dispensam o token. | Protege a sessão do navegador sem impedir os testes de API com Postman. |
| Textos vindos da API são inseridos na tela com `textContent`. | Evita execução de HTML/script digitado pelo usuário. |

## 6. Massa de dados fictícios (perfis `dev` e `test`)

| Tipo | Registros |
|---|---|
| Barbeiros | Carlos Navalha (ativo), Rafael Tesoura (ativo), Diego Máquina (inativo) |
| Serviços | Corte de cabelo (30 min, R$ 45,00), Barba (30 min, R$ 30,00), Corte e barba (60 min, R$ 70,00), Sobrancelha (15 min, R$ 15,00), Relaxamento capilar (90 min, R$ 80,00, inativo) |
| Clientes | 10 clientes com e-mails `@exemplo.com` (ex.: `ana.rocha@exemplo.com`) |
| Agendamentos | 5, com datas relativas ao dia atual: 3 `AGENDADO` (próximos dias de funcionamento), 1 `CANCELADO`, 1 `CONCLUIDO` (dia de funcionamento anterior) |

Os ids mudam a cada restauração; testes automatizados devem obter os ids pelas consultas, e não fixá-los.
