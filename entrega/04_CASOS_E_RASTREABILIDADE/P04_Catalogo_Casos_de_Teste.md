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

## 3. Casos de teste (Apêndice E)

### CT-001 — Cadastrar cliente com dados válidos

| Campo | Conteúdo |
|---|---|
| ID do caso | CT-001 |
| Título | Cadastrar cliente com dados válidos |
| Requisito relacionado | RF-01 (regras: RN-01, RN-02, RN-03; riscos: R-05) |
| Nível/tipo | Sistema / Funcional — classificação: Positivo; interface: Tela |
| Técnica aplicada | Particionamento de equivalência (classes válidas) |
| Prioridade | Média |
| Pré-condições | PC-PADRÃO. |
| Dados de entrada | Nome: Marina Lopes Teixeira; Telefone: 14988776655; E-mail: marina.<AAAAMMDD>@exemplo.com |
| Passos numerados | 1. Abrir http://localhost:8080/cadastro.html.<br>2. Preencher Nome, Telefone e E-mail com os dados.<br>3. Clicar em "Cadastrar". |
| Resultado esperado | Mensagem "Cadastro realizado com sucesso! Código do cliente: N." (N = número) e botão "Agendar um horário" visível. Campos do formulário limpos. |
| Candidato à automação | Sim — Interface (Selenium) e API (Postman). Fluxo principal e repetido em toda regressão. **Automatizado: Parcial** (Unidade: CadastroServiceTest#deveCadastrarClienteComDadosValidos) |
| Responsável | [PREENCHER PELO GRUPO] |

### CT-002 — Cadastro aceita nome e telefone nos limites válidos

| Campo | Conteúdo |
|---|---|
| ID do caso | CT-002 |
| Título | Cadastro aceita nome e telefone nos limites válidos |
| Requisito relacionado | RF-01 (regras: RN-01, RN-02; riscos: R-05) |
| Nível/tipo | Sistema / Funcional — classificação: Fronteira; interface: Tela |
| Técnica aplicada | Análise de valor limite |
| Prioridade | Média |
| Pré-condições | PC-PADRÃO. |
| Dados de entrada | (a) Nome com 3 caracteres "Léa", telefone com 10 dígitos 1432221100, e-mail lea.<AAAAMMDD>@exemplo.com. (b) Nome com 60 caracteres "Maria Eduarda Fernandes Albuquerque Cavalcanti Souza Ribeiro", telefone com 11 dígitos 14999990000, e-mail maria.eduarda.<AAAAMMDD>@exemplo.com |
| Passos numerados | 1. Abrir a tela de cadastro.<br>2. Preencher com os dados (a) e clicar em "Cadastrar".<br>3. Preencher com os dados (b) e clicar em "Cadastrar". |
| Resultado esperado | Nos dois cadastros, mensagem "Cadastro realizado com sucesso!" com o código do cliente. |
| Candidato à automação | Sim — Unidade (validação de ClienteRequest). Limites são regras estáveis e baratas de verificar a cada build. **Automatizado: Sim** (Unidade: ValidacaoEntradaTest#deveAceitarNomeETelefoneNosLimitesValidos) |
| Responsável | [PREENCHER PELO GRUPO] |

### CT-003 — Cadastro recusa nome com 2 e com 61 caracteres

| Campo | Conteúdo |
|---|---|
| ID do caso | CT-003 |
| Título | Cadastro recusa nome com 2 e com 61 caracteres |
| Requisito relacionado | RF-01 (regras: RN-01; riscos: R-05) |
| Nível/tipo | Sistema / Funcional — classificação: Fronteira; interface: Tela |
| Técnica aplicada | Análise de valor limite |
| Prioridade | Média |
| Pré-condições | PC-PADRÃO. |
| Dados de entrada | (a) Nome "Al" (2 caracteres). (b) Nome com 61 caracteres "Maria Eduarda Fernandes Albuquerque Cavalcanti Souza Ribeiros". Telefone 14988776655 e e-mail nome.limite.<AAAAMMDD>@exemplo.com nos dois. |
| Passos numerados | 1. Abrir a tela de cadastro.<br>2. Preencher com o nome (a) e os demais dados; clicar em "Cadastrar".<br>3. Trocar o nome para (b) e clicar em "Cadastrar". |
| Resultado esperado | Nas duas tentativas: mensagem "O nome deve ter entre 3 e 60 caracteres." abaixo do campo Nome, mensagem geral "Existem campos inválidos." e nenhum código de cliente exibido. |
| Candidato à automação | Sim — Unidade (validação de ClienteRequest). Limites inválidos complementam CT-002 na mesma suíte. **Automatizado: Sim** (Unidade: ValidacaoEntradaTest#deveRejeitarNomeForaDoLimite) |
| Responsável | [PREENCHER PELO GRUPO] |

### CT-004 — Cadastro recusa telefone fora do padrão

| Campo | Conteúdo |
|---|---|
| ID do caso | CT-004 |
| Título | Cadastro recusa telefone fora do padrão |
| Requisito relacionado | RF-01 (regras: RN-02; riscos: R-05) |
| Nível/tipo | Sistema / Funcional — classificação: Negativo; interface: Tela |
| Técnica aplicada | Análise de valor limite e particionamento (classe com não dígitos) |
| Prioridade | Média |
| Pré-condições | PC-PADRÃO. |
| Dados de entrada | Nome: Rodrigo Teste; e-mail rodrigo.<AAAAMMDD>@exemplo.com; telefones: (a) 149887766 (9 dígitos); (b) 149887766551 (12 dígitos); (c) 14-98877-6655 (com hífens). |
| Passos numerados | 1. Abrir a tela de cadastro.<br>2. Para cada telefone (a), (b) e (c): preencher os dados e clicar em "Cadastrar". |
| Resultado esperado | Nas três tentativas: mensagem "O telefone deve conter somente dígitos, com 10 ou 11 dígitos (incluindo DDD)." abaixo do campo Telefone e nenhum cadastro realizado. |
| Candidato à automação | Sim — Unidade (validação de ClienteRequest). Regra de formato estável, rápida de verificar. **Automatizado: Sim** (Unidade: ValidacaoEntradaTest#deveRejeitarTelefoneForaDoPadrao) |
| Responsável | [PREENCHER PELO GRUPO] |

### CT-005 — Cadastro recusa e-mail em formato inválido

| Campo | Conteúdo |
|---|---|
| ID do caso | CT-005 |
| Título | Cadastro recusa e-mail em formato inválido |
| Requisito relacionado | RF-01 (regras: RN-03; riscos: R-05) |
| Nível/tipo | Sistema / Funcional — classificação: Negativo; interface: Tela |
| Técnica aplicada | Particionamento de equivalência (classes inválidas) |
| Prioridade | Média |
| Pré-condições | PC-PADRÃO. |
| Dados de entrada | Nome: Paula Teste; telefone 14988776655; e-mails: (a) paula.exemplo.com (sem @); (b) paula@exemplo (sem domínio de topo). |
| Passos numerados | 1. Abrir a tela de cadastro.<br>2. Para cada e-mail (a) e (b): preencher os dados e clicar em "Cadastrar". |
| Resultado esperado | Nas duas tentativas: mensagem "O e-mail informado é inválido." abaixo do campo E-mail e nenhum cadastro realizado. |
| Candidato à automação | Sim — API (Postman, fluxo negativo de POST /api/clientes). Operação crítica precisa de ao menos um fluxo negativo na coleção. **Automatizado: Parcial** (Unidade: ValidacaoEntradaTest#deveRejeitarEmailEmFormatoInvalido) |
| Responsável | [PREENCHER PELO GRUPO] |

### CT-006 — Cadastro recusa e-mail já cadastrado, mesmo com maiúsculas

| Campo | Conteúdo |
|---|---|
| ID do caso | CT-006 |
| Título | Cadastro recusa e-mail já cadastrado, mesmo com maiúsculas |
| Requisito relacionado | RF-01 (regras: RN-03; riscos: R-05) |
| Nível/tipo | Sistema / Funcional — classificação: Exceção; interface: Tela |
| Técnica aplicada | Particionamento de equivalência (e-mail existente) |
| Prioridade | Média |
| Pré-condições | PC-PADRÃO (cliente ana.rocha@exemplo.com existe na massa). |
| Dados de entrada | Nome: Ana Repetida; telefone 14988776655; e-mail ANA.ROCHA@EXEMPLO.COM |
| Passos numerados | 1. Abrir a tela de cadastro.<br>2. Preencher os dados e clicar em "Cadastrar". |
| Resultado esperado | Mensagem "Já existe um cliente cadastrado com este e-mail." (HTTP 409) e nenhum cadastro realizado. |
| Candidato à automação | Sim — Unidade (ClienteService com mock) e API (Postman). Regra de unicidade crítica para identificar o cliente no agendamento. **Automatizado: Parcial** (Unidade: CadastroServiceTest#deveRejeitarCadastroComEmailJaCadastrado) |
| Responsável | [PREENCHER PELO GRUPO] |

### CT-007 — Horários disponíveis respeitam funcionamento, intervalo e duração do serviço

| Campo | Conteúdo |
|---|---|
| ID do caso | CT-007 |
| Título | Horários disponíveis respeitam funcionamento, intervalo e duração do serviço |
| Requisito relacionado | RF-02 (regras: RN-04, RN-05; riscos: R-02) |
| Nível/tipo | Sistema / Funcional — classificação: Positivo; interface: Tela |
| Técnica aplicada | Análise de valor limite (último início possível) |
| Prioridade | Alta |
| Pré-condições | PC-PADRÃO. Carlos Navalha não tem agendamentos em DF3. |
| Dados de entrada | Barbeiro: Carlos Navalha; Serviço: Corte e barba (60 min); Data: DF3 |
| Passos numerados | 1. Abrir http://localhost:8080/agendar.html.<br>2. Selecionar barbeiro, serviço e data.<br>3. Clicar em "Ver horários disponíveis". |
| Resultado esperado | 19 horários, de 09:00 a 18:00, de 30 em 30 minutos (09:00, 09:30, ..., 18:00). Não aparecem 18:30 nem horários antes de 09:00. |
| Candidato à automação | Sim — Unidade (RegrasAgendamento.gerarHorariosDoDia com Clock fixo). Cálculo determinístico e central para o agendamento. **Automatizado: Sim** (Unidade: RegrasAgendamentoTest#deveGerarHorariosDe09hA18hParaServicoDe60Minutos) |
| Responsável | [PREENCHER PELO GRUPO] |

### CT-008 — Horários ocupados pelo barbeiro não são oferecidos

| Campo | Conteúdo |
|---|---|
| ID do caso | CT-008 |
| Título | Horários ocupados pelo barbeiro não são oferecidos |
| Requisito relacionado | RF-02, RF-04 (regras: RN-07; riscos: R-01, R-02) |
| Nível/tipo | Sistema / Funcional — classificação: Alternativo; interface: Tela |
| Técnica aplicada | Análise de valor limite (vizinhos do horário ocupado) |
| Prioridade | Alta |
| Pré-condições | PC-PADRÃO. Rafael Tesoura tem agendamento (SEMENTE3) em DF1, 14:00–15:00. |
| Dados de entrada | Barbeiro: Rafael Tesoura; Serviço: Corte de cabelo (30 min); Data: DF1 |
| Passos numerados | 1. Abrir a tela de agendamento.<br>2. Selecionar barbeiro, serviço e data.<br>3. Clicar em "Ver horários disponíveis". |
| Resultado esperado | Não aparecem 14:00 nem 14:30. Aparecem 13:30 e 15:00. Total de 18 horários (09:00 a 18:30, menos os 2 ocupados). |
| Candidato à automação | Sim — Unidade (AgendamentoService.horariosDisponiveis com mocks). Filtro de ocupação é regra de alto risco (R-01). **Automatizado: Sim** (Unidade: AgendamentoServiceTest#naoDeveOferecerHorariosOcupadosPeloBarbeiro) |
| Responsável | [PREENCHER PELO GRUPO] |

### CT-009 — Datas sem atendimento retornam lista de horários vazia

| Campo | Conteúdo |
|---|---|
| ID do caso | CT-009 |
| Título | Datas sem atendimento retornam lista de horários vazia |
| Requisito relacionado | RF-02 (regras: RN-04, RN-06; riscos: R-04) |
| Nível/tipo | Sistema / Funcional — classificação: Alternativo; interface: API |
| Técnica aplicada | Particionamento de equivalência (datas inválidas) |
| Prioridade | Média |
| Pré-condições | PC-PADRÃO. Ids de Carlos Navalha e Corte de cabelo obtidos em GET /api/barbeiros e GET /api/servicos. |
| Dados de entrada | Datas: (a) DOM; (b) D+31; (c) ONTEM |
| Passos numerados | 1. Para cada data, enviar GET /api/horarios-disponiveis?barbeiroId={Carlos}&servicoId={Corte}&data=<data>. |
| Resultado esperado | As três respostas têm HTTP 200 e "horarios": [] (lista vazia). |
| Candidato à automação | Sim — Unidade (RegrasAgendamento.dataAceitaAgendamentos com Clock fixo). Regra de data sensível a limites; deve ser verificada a cada build. **Automatizado: Sim** (Unidade: RegrasAgendamentoTest#deveRetornarListaVaziaParaDataSemAtendimento) |
| Responsável | [PREENCHER PELO GRUPO] |

### CT-010 — Agendar horário pela tela com sucesso

| Campo | Conteúdo |
|---|---|
| ID do caso | CT-010 |
| Título | Agendar horário pela tela com sucesso |
| Requisito relacionado | RF-03 (regras: RN-04, RN-05, RN-06, RN-10; riscos: R-02) |
| Nível/tipo | Sistema / Funcional — classificação: Positivo; interface: Tela |
| Técnica aplicada | Caso de uso (fluxo principal) |
| Prioridade | Alta |
| Pré-condições | PC-PADRÃO. Cliente camila.prado@exemplo.com sem agendamentos ativos. |
| Dados de entrada | E-mail: camila.prado@exemplo.com; Barbeiro: Carlos Navalha; Serviço: Barba; Data: DF3; Horário: 11:00 |
| Passos numerados | 1. Abrir a tela de agendamento.<br>2. Informar o e-mail; selecionar barbeiro, serviço e data.<br>3. Clicar em "Ver horários disponíveis" e escolher 11:00.<br>4. Clicar em "Confirmar agendamento". |
| Resultado esperado | Mensagem "Agendamento realizado com sucesso! Código de acesso: XXXXXXXX." e quadro "Agendamento confirmado" com código de 8 caracteres, Carlos Navalha, Barba, data DF3 11:00 e status AGENDADO. |
| Candidato à automação | Sim — Interface (Selenium) e API (Postman). Fluxo mais importante do sistema. |
| Responsável | [PREENCHER PELO GRUPO] |

### CT-011 — Agendamento aceito no primeiro e no último horário do dia

| Campo | Conteúdo |
|---|---|
| ID do caso | CT-011 |
| Título | Agendamento aceito no primeiro e no último horário do dia |
| Requisito relacionado | RF-03 (regras: RN-04; riscos: R-02) |
| Nível/tipo | Sistema / Funcional — classificação: Fronteira; interface: Tela |
| Técnica aplicada | Análise de valor limite (abertura 09:00; término 19:00) |
| Prioridade | Alta |
| Pré-condições | PC-PADRÃO. Cliente felipe.nunes@exemplo.com sem agendamentos ativos. |
| Dados de entrada | E-mail: felipe.nunes@exemplo.com; Barbeiro: Carlos Navalha; Serviço: Corte de cabelo (30 min); Data: DF3; Horários: (a) 09:00; (b) 18:30 (termina 19:00) |
| Passos numerados | 1. Na tela de agendamento, agendar o horário (a).<br>2. Recarregar a página e agendar o horário (b). |
| Resultado esperado | Os dois agendamentos são confirmados com status AGENDADO e código de acesso. |
| Candidato à automação | Sim — Unidade (RegrasAgendamento.validarFuncionamento). Limites da regra de maior risco. **Automatizado: Sim** (Unidade: RegrasAgendamentoTest#deveAceitarAgendamentoNosLimitesDoFuncionamento) |
| Responsável | [PREENCHER PELO GRUPO] |

### CT-012 — Agendamento recusado quando começa antes de 09:00 ou termina depois de 19:00

| Campo | Conteúdo |
|---|---|
| ID do caso | CT-012 |
| Título | Agendamento recusado quando começa antes de 09:00 ou termina depois de 19:00 |
| Requisito relacionado | RF-03 (regras: RN-04; riscos: R-02) |
| Nível/tipo | Sistema / Funcional — classificação: Fronteira; interface: API |
| Técnica aplicada | Análise de valor limite |
| Prioridade | Alta |
| Pré-condições | PC-PADRÃO. Ids de Carlos Navalha, Corte de cabelo (30 min) e Corte e barba (60 min) obtidos nas consultas públicas. |
| Dados de entrada | emailCliente: gabriela.teixeira@exemplo.com; barbeiro Carlos; (a) Corte de cabelo, DF3T08:30:00; (b) Corte e barba, DF3T18:30:00 (terminaria 19:30); (c) Corte e barba, DF3T18:00:00 (termina 19:00) |
| Passos numerados | 1. Para cada combinação, enviar POST /api/agendamentos com {"emailCliente", "barbeiroId", "servicoId", "dataHoraInicio"}. |
| Resultado esperado | (a) e (b): HTTP 400 com mensagem "O atendimento deve ocorrer entre 09:00 e 19:00 e o serviço precisa terminar até 19:00." (c): HTTP 201, status AGENDADO. |
| Candidato à automação | Sim — Unidade (RegrasAgendamento.validarFuncionamento). Limites só alcançáveis pela API; regra de maior risco. **Automatizado: Sim** (Unidade: RegrasAgendamentoTest#deveRejeitarAgendamentoForaDoHorarioDeFuncionamento) |
| Responsável | [PREENCHER PELO GRUPO] |

### CT-013 — Agendamento recusado fora dos intervalos de 30 minutos

| Campo | Conteúdo |
|---|---|
| ID do caso | CT-013 |
| Título | Agendamento recusado fora dos intervalos de 30 minutos |
| Requisito relacionado | RF-03 (regras: RN-05; riscos: R-02) |
| Nível/tipo | Sistema / Funcional — classificação: Negativo; interface: API |
| Técnica aplicada | Particionamento de equivalência (minutos diferentes de 00 e 30) e valor limite |
| Prioridade | Alta |
| Pré-condições | PC-PADRÃO. Ids de Carlos Navalha e Corte de cabelo obtidos nas consultas públicas. |
| Dados de entrada | emailCliente: gabriela.teixeira@exemplo.com; dataHoraInicio: (a) DF3T10:15:00; (b) DF3T10:01:00 |
| Passos numerados | 1. Para cada horário, enviar POST /api/agendamentos. |
| Resultado esperado | HTTP 400 com mensagem "Os agendamentos devem começar em intervalos de 30 minutos (ex.: 09:00, 09:30)." e campo dataHoraInicio em "campos". |
| Candidato à automação | Sim — Unidade (RegrasAgendamento.validarIntervalo). Regra simples e estável. **Automatizado: Sim** (Unidade: RegrasAgendamentoTest#deveRejeitarInicioForaDoIntervaloDe30Minutos) |
| Responsável | [PREENCHER PELO GRUPO] |

### CT-014 — Agendamento recusado no domingo

| Campo | Conteúdo |
|---|---|
| ID do caso | CT-014 |
| Título | Agendamento recusado no domingo |
| Requisito relacionado | RF-03 (regras: RN-04; riscos: R-02) |
| Nível/tipo | Sistema / Funcional — classificação: Negativo; interface: API |
| Técnica aplicada | Particionamento de equivalência (dia da semana) |
| Prioridade | Alta |
| Pré-condições | PC-PADRÃO. Ids de Carlos Navalha e Corte de cabelo obtidos nas consultas públicas. |
| Dados de entrada | emailCliente: gabriela.teixeira@exemplo.com; dataHoraInicio: DOMT10:00:00 |
| Passos numerados | 1. Enviar POST /api/agendamentos com os dados. |
| Resultado esperado | HTTP 400 com mensagem "A barbearia não abre aos domingos." |
| Candidato à automação | Sim — Unidade (RegrasAgendamento.validarFuncionamento). Regra de calendário verificável com Clock fixo. **Automatizado: Sim** (Unidade: RegrasAgendamentoTest#deveRejeitarAgendamentoNoDomingo) |
| Responsável | [PREENCHER PELO GRUPO] |

### CT-015 — Antecedência: aceita D+30 e recusa D+31

| Campo | Conteúdo |
|---|---|
| ID do caso | CT-015 |
| Título | Antecedência: aceita D+30 e recusa D+31 |
| Requisito relacionado | RF-03 (regras: RN-06; riscos: R-04) |
| Nível/tipo | Sistema / Funcional — classificação: Fronteira; interface: API |
| Técnica aplicada | Análise de valor limite |
| Prioridade | Média |
| Pré-condições | PC-PADRÃO. D+30 não pode cair em domingo (se cair, registrar "Bloqueado" e executar no dia seguinte). Ids de Carlos Navalha e Corte de cabelo obtidos. |
| Dados de entrada | emailCliente: heitor.moreira@exemplo.com; dataHoraInicio: (a) D+30T10:00:00; (b) D+31T10:00:00 |
| Passos numerados | 1. Enviar POST /api/agendamentos com a data (a).<br>2. Enviar POST /api/agendamentos com a data (b). |
| Resultado esperado | (a): HTTP 201, status AGENDADO. (b): HTTP 400 com mensagem "A antecedência máxima para agendamento é de 30 dias." |
| Candidato à automação | Sim — Unidade (RegrasAgendamento.validarAntecedencia com Clock fixo). Limite dependente de data; Clock fixo torna o teste estável. **Automatizado: Sim** (Unidade: RegrasAgendamentoTest#deveAceitarAgendamentoComTrintaDiasDeAntecedencia; #deveRejeitarAgendamentoComTrintaEUmDiasDeAntecedencia) |
| Responsável | [PREENCHER PELO GRUPO] |

### CT-016 — Agendamento recusado em data ou horário que já passou

| Campo | Conteúdo |
|---|---|
| ID do caso | CT-016 |
| Título | Agendamento recusado em data ou horário que já passou |
| Requisito relacionado | RF-03 (regras: RN-06; riscos: R-04) |
| Nível/tipo | Sistema / Funcional — classificação: Negativo; interface: API |
| Técnica aplicada | Análise de valor limite (agora) e particionamento (passado) |
| Prioridade | Média |
| Pré-condições | PC-PADRÃO. Para o dado (b), executar de segunda a sábado depois das 09:30. |
| Dados de entrada | emailCliente: heitor.moreira@exemplo.com; Carlos; Corte de cabelo; dataHoraInicio: (a) ONTEMT10:00:00; (b) hoje às 09:00 |
| Passos numerados | 1. Enviar POST /api/agendamentos com (a).<br>2. Enviar POST /api/agendamentos com (b). |
| Resultado esperado | Nas duas: HTTP 400 com mensagem "Não é permitido agendar em data ou horário que já passou." |
| Candidato à automação | Sim — Unidade (RegrasAgendamento.validarAntecedencia com Clock fixo). Depende do momento atual; automação com Clock fixo elimina a restrição de horário. **Automatizado: Sim** (Unidade: RegrasAgendamentoTest#deveRejeitarAgendamentoNoPassado; #deveAceitarProximoHorarioDoDiaDeHoje) |
| Responsável | [PREENCHER PELO GRUPO] |

### CT-017 — Barbeiro e serviço inativos não são oferecidos nem aceitos

| Campo | Conteúdo |
|---|---|
| ID do caso | CT-017 |
| Título | Barbeiro e serviço inativos não são oferecidos nem aceitos |
| Requisito relacionado | RF-03 (regras: RN-10; riscos: R-02) |
| Nível/tipo | Sistema / Funcional — classificação: Exceção; interface: Tela e API |
| Técnica aplicada | Particionamento de equivalência (ativo × inativo) |
| Prioridade | Média |
| Pré-condições | PC-PADRÃO (Diego Máquina e Relaxamento capilar estão inativos na massa). Ids obtidos em GET /api/admin/barbeiros e /api/admin/servicos (admin:admin123). |
| Dados de entrada | emailCliente: gabriela.teixeira@exemplo.com; DF3T10:00:00; (a) Diego Máquina + Corte de cabelo; (b) Carlos Navalha + Relaxamento capilar |
| Passos numerados | 1. Abrir a tela de agendamento e abrir as listas de barbeiros e serviços.<br>2. Enviar POST /api/agendamentos com (a).<br>3. Enviar POST /api/agendamentos com (b). |
| Resultado esperado | Passo 1: Diego Máquina e Relaxamento capilar não aparecem. (a): HTTP 400 "O barbeiro selecionado está inativo." (b): HTTP 400 "O serviço selecionado está inativo." |
| Candidato à automação | Sim — Unidade (AgendamentoService com mocks). Regra simples de verificar isoladamente. **Automatizado: Sim** (Unidade: AgendamentoServiceTest#deveRejeitarAgendamentoComBarbeiroInativo; #deveRejeitarAgendamentoComServicoInativo) |
| Responsável | [PREENCHER PELO GRUPO] |

### CT-018 — Agendamento com e-mail não cadastrado é recusado

| Campo | Conteúdo |
|---|---|
| ID do caso | CT-018 |
| Título | Agendamento com e-mail não cadastrado é recusado |
| Requisito relacionado | RF-03 (regras: —; riscos: R-05) |
| Nível/tipo | Sistema / Funcional — classificação: Exceção; interface: Tela |
| Técnica aplicada | Particionamento de equivalência (cliente inexistente) |
| Prioridade | Média |
| Pré-condições | PC-PADRÃO. |
| Dados de entrada | E-mail: nao.cadastrado@exemplo.com; Carlos Navalha; Barba; DF3; 15:00 |
| Passos numerados | 1. Na tela de agendamento, preencher os dados, buscar horários e escolher 15:00.<br>2. Clicar em "Confirmar agendamento". |
| Resultado esperado | Mensagem "Cliente não encontrado para o e-mail informado. Faça o cadastro antes de agendar." e nenhum código de acesso exibido. |
| Candidato à automação | Sim — API (Postman, fluxo negativo de POST /api/agendamentos). Fluxo negativo da operação crítica de agendamento. **Automatizado: Parcial** (Unidade: AgendamentoServiceTest#deveRejeitarAgendamentoDeClienteNaoCadastrado) |
| Responsável | [PREENCHER PELO GRUPO] |

### CT-019 — Agendamento sobreposto ao de outro cliente com o mesmo barbeiro é recusado

| Campo | Conteúdo |
|---|---|
| ID do caso | CT-019 |
| Título | Agendamento sobreposto ao de outro cliente com o mesmo barbeiro é recusado |
| Requisito relacionado | RF-04 (regras: RN-07; riscos: R-01) |
| Nível/tipo | Sistema / Funcional — classificação: Negativo; interface: API |
| Técnica aplicada | Análise de valor limite (sobreposição parcial no início e no fim) |
| Prioridade | Alta |
| Pré-condições | PC-PADRÃO. Rafael Tesoura tem SEMENTE3 em DF1, 14:00–15:00. Ids obtidos nas consultas públicas. |
| Dados de entrada | emailCliente: joao.mendes@exemplo.com; Rafael; (a) Corte de cabelo DF1T14:30:00 (14:30–15:00); (b) Corte e barba DF1T13:30:00 (13:30–14:30) |
| Passos numerados | 1. Enviar POST /api/agendamentos com (a).<br>2. Enviar POST /api/agendamentos com (b). |
| Resultado esperado | Nas duas: HTTP 409 com mensagem "O barbeiro já possui agendamento nesse horário." |
| Candidato à automação | Sim — Unidade (AgendamentoService com mock) e API (Postman). Risco mais alto do produto (R-01). **Automatizado: Parcial** (Unidade: AgendamentoServiceTest#deveRejeitarAgendamentoQuandoHorarioConflitaComOutroDoMesmoBarbeiro) |
| Responsável | [PREENCHER PELO GRUPO] |

### CT-020 — Horário encostado e mesmo horário com outro barbeiro são aceitos

| Campo | Conteúdo |
|---|---|
| ID do caso | CT-020 |
| Título | Horário encostado e mesmo horário com outro barbeiro são aceitos |
| Requisito relacionado | RF-04 (regras: RN-07; riscos: R-01) |
| Nível/tipo | Sistema / Funcional — classificação: Fronteira; interface: API |
| Técnica aplicada | Análise de valor limite (intervalos que se tocam) |
| Prioridade | Alta |
| Pré-condições | PC-PADRÃO. Rafael Tesoura tem SEMENTE3 em DF1, 14:00–15:00. Ids obtidos. |
| Dados de entrada | emailCliente: isabela.pires@exemplo.com; Corte de cabelo (30 min); (a) Rafael DF1T13:30:00 (termina 14:00); (b) Rafael DF1T15:00:00 (começa às 15:00); (c) Carlos DF1T14:00:00 |
| Passos numerados | 1. Enviar POST /api/agendamentos com (a), (b) e (c), nesta ordem. |
| Resultado esperado | As três respostas: HTTP 201 com status AGENDADO. |
| Candidato à automação | Sim — API (Postman). O limite depende da consulta ao banco; precisa de teste integrado. |
| Responsável | [PREENCHER PELO GRUPO] |

### CT-021 — Limite de agendamentos ativos: 3º aceito e 4º recusado

| Campo | Conteúdo |
|---|---|
| ID do caso | CT-021 |
| Título | Limite de agendamentos ativos: 3º aceito e 4º recusado |
| Requisito relacionado | RF-04 (regras: RN-08; riscos: R-06) |
| Nível/tipo | Sistema / Funcional — classificação: Fronteira; interface: API |
| Técnica aplicada | Análise de valor limite (3 e 4) |
| Prioridade | Média |
| Pré-condições | PC-PADRÃO. Ids de Carlos Navalha e Corte de cabelo obtidos. |
| Dados de entrada | Cliente novo: nome "Cliente Limite", telefone 14977770021, e-mail ct021.<AAAAMMDD>@exemplo.com; agendamentos com Carlos, Corte de cabelo, DF3: 09:00, 09:30, 10:00 e 10:30 |
| Passos numerados | 1. Cadastrar o cliente: POST /api/clientes.<br>2. Enviar POST /api/agendamentos para 09:00, 09:30 e 10:00.<br>3. Enviar POST /api/agendamentos para 10:30. |
| Resultado esperado | Passo 2: três respostas HTTP 201 (o 3º agendamento é aceito). Passo 3: HTTP 409 com mensagem "O cliente já possui 3 agendamentos ativos, que é o limite permitido." |
| Candidato à automação | Sim — Unidade (AgendamentoService com mock da contagem). Limite numérico estável. **Automatizado: Sim** (Unidade: AgendamentoServiceTest#deveRejeitarQuartoAgendamentoAtivoDoCliente; #deveAceitarTerceiroAgendamentoAtivoDoCliente) |
| Responsável | [PREENCHER PELO GRUPO] |

### CT-022 — Após cancelar um agendamento, cliente no limite volta a poder agendar

| Campo | Conteúdo |
|---|---|
| ID do caso | CT-022 |
| Título | Após cancelar um agendamento, cliente no limite volta a poder agendar |
| Requisito relacionado | RF-04, RF-05 (regras: RN-08; riscos: R-06) |
| Nível/tipo | Sistema / Funcional — classificação: Alternativo; interface: Tela e API |
| Técnica aplicada | Transição de estados (AGENDADO → CANCELADO libera vaga) |
| Prioridade | Média |
| Pré-condições | PC-PADRÃO. Cliente ct022.<AAAAMMDD>@exemplo.com cadastrado com 3 agendamentos ativos com Carlos em DF3 (09:00, 09:30, 10:00), criados como em CT-021; anotar o código de acesso do agendamento das 09:00. |
| Dados de entrada | Código de acesso do agendamento das 09:00; e-mail ct022.<AAAAMMDD>@exemplo.com; novo agendamento: Carlos, Corte de cabelo, DF3T10:30:00 |
| Passos numerados | 1. Abrir http://localhost:8080/consulta.html, informar código e e-mail e clicar em "Consultar".<br>2. Clicar em "Cancelar agendamento" e em "Sim, cancelar".<br>3. Enviar POST /api/agendamentos para DF3T10:30:00. |
| Resultado esperado | Passo 2: status CANCELADO. Passo 3: HTTP 201 (o cliente volta a ter 3 ativos). |
| Candidato à automação | Não. Cenário com várias etapas e estado; o limite já é automatizado em CT-021 e o cancelamento em CT-025. |
| Responsável | [PREENCHER PELO GRUPO] |

### CT-023 — Consultar agendamento com código de acesso (em minúsculas) e e-mail

| Campo | Conteúdo |
|---|---|
| ID do caso | CT-023 |
| Título | Consultar agendamento com código de acesso (em minúsculas) e e-mail |
| Requisito relacionado | RF-05 (regras: —; riscos: R-07) |
| Nível/tipo | Sistema / Funcional — classificação: Positivo; interface: Tela |
| Técnica aplicada | Tabela de decisão (código certo × e-mail certo) |
| Prioridade | Média |
| Pré-condições | PC-PADRÃO (SEMENTE2 pertence a ana.rocha@exemplo.com). |
| Dados de entrada | Código: semente2 (minúsculas); E-mail: ana.rocha@exemplo.com |
| Passos numerados | 1. Abrir http://localhost:8080/consulta.html.<br>2. Informar código e e-mail e clicar em "Consultar". |
| Resultado esperado | Quadro "Agendamento SEMENTE2" com Cliente Ana Beatriz Rocha, Barbeiro Carlos Navalha, Serviço Corte de cabelo (30 min), Data DF1 10:00, Valor R$ 45,00, Status AGENDADO e botão "Cancelar agendamento" visível. |
| Candidato à automação | Sim — API (Postman, GET encadeado após o agendamento) e Interface (Selenium, no fluxo de cancelamento). Operação usada em todo cancelamento. |
| Responsável | [PREENCHER PELO GRUPO] |

### CT-024 — Consulta recusada quando código e e-mail não conferem

| Campo | Conteúdo |
|---|---|
| ID do caso | CT-024 |
| Título | Consulta recusada quando código e e-mail não conferem |
| Requisito relacionado | RF-05 (regras: —; riscos: R-07) |
| Nível/tipo | Sistema / Funcional (segurança) — classificação: Negativo; interface: Tela |
| Técnica aplicada | Tabela de decisão |
| Prioridade | Média |
| Pré-condições | PC-PADRÃO. |
| Dados de entrada | (a) SEMENTE2 + bruno.lima@exemplo.com (e-mail de outro cliente); (b) ZZZZ9999 + ana.rocha@exemplo.com (código inexistente); (c) 1 + ana.rocha@exemplo.com (número sequencial) |
| Passos numerados | 1. Abrir a tela de consulta.<br>2. Para cada combinação, informar código e e-mail e clicar em "Consultar". |
| Resultado esperado | Nas três: mensagem "Agendamento não encontrado para o código de acesso e o e-mail informados." e nenhum dado de agendamento exibido. |
| Candidato à automação | Sim — API (Postman, fluxo negativo de GET /api/agendamentos/{codigo}). Protege dados de terceiros (R-07). **Automatizado: Parcial** (Unidade: AgendamentoServiceTest#deveRecusarConsultaComEmailDeOutroCliente) |
| Responsável | [PREENCHER PELO GRUPO] |

### CT-025 — Cancelar agendamento pela tela libera o horário

| Campo | Conteúdo |
|---|---|
| ID do caso | CT-025 |
| Título | Cancelar agendamento pela tela libera o horário |
| Requisito relacionado | RF-05 (regras: —; riscos: R-07) |
| Nível/tipo | Sistema / Funcional — classificação: Positivo; interface: Tela |
| Técnica aplicada | Transição de estados (AGENDADO → CANCELADO) |
| Prioridade | Média |
| Pré-condições | PC-PADRÃO (SEMENTE6: eduarda.costa@exemplo.com, Carlos Navalha, Sobrancelha, DF2 16:00, AGENDADO). |
| Dados de entrada | Código: SEMENTE6; E-mail: eduarda.costa@exemplo.com |
| Passos numerados | 1. Na tela de consulta, consultar o agendamento.<br>2. Clicar em "Cancelar agendamento" e depois em "Sim, cancelar".<br>3. Abrir a tela de agendamento e listar horários de Carlos Navalha, Sobrancelha, DF2. |
| Resultado esperado | Passo 2: mensagem "Agendamento cancelado com sucesso.", status CANCELADO e botão de cancelar oculto. Passo 3: o horário 16:00 aparece na lista. |
| Candidato à automação | Sim — Interface (Selenium). Fluxo ponta a ponta exigido pelo manual (cancelamento). **Automatizado: Parcial** (Unidade: AgendamentoServiceTest#deveCancelarAgendamentoAtivoDoCliente; #deveOferecerHorarioDeAgendamentoCancelado) |
| Responsável | [PREENCHER PELO GRUPO] |

### CT-026 — Cancelar agendamento já cancelado ou concluído é recusado

| Campo | Conteúdo |
|---|---|
| ID do caso | CT-026 |
| Título | Cancelar agendamento já cancelado ou concluído é recusado |
| Requisito relacionado | RF-05 (regras: —; riscos: R-07) |
| Nível/tipo | Sistema / Funcional — classificação: Alternativo; interface: Tela e API |
| Técnica aplicada | Transição de estados (transições inválidas) |
| Prioridade | Média |
| Pré-condições | PC-PADRÃO (SEMENTE4: camila.prado, CANCELADO; SEMENTE5: daniel.alves, CONCLUIDO). |
| Dados de entrada | (a) SEMENTE4 + camila.prado@exemplo.com; (b) SEMENTE5 + daniel.alves@exemplo.com |
| Passos numerados | 1. Na tela de consulta, consultar (a).<br>2. Enviar PATCH /api/agendamentos/SEMENTE4/cancelar com {"email": "camila.prado@exemplo.com"}.<br>3. Enviar PATCH /api/agendamentos/SEMENTE5/cancelar com {"email": "daniel.alves@exemplo.com"}. |
| Resultado esperado | Passo 1: status CANCELADO e botão "Cancelar agendamento" não exibido. Passos 2 e 3: HTTP 409 com mensagem "Somente agendamentos com status AGENDADO podem ser cancelados." |
| Candidato à automação | Sim — API (Postman). Transição inválida só alcançável pela API. **Automatizado: Parcial** (Unidade: AgendamentoServiceTest#deveRejeitarCancelamentoDeAgendamentoJaCancelado) |
| Responsável | [PREENCHER PELO GRUPO] |

### CT-027 — Login do administrador com credencial válida e saída

| Campo | Conteúdo |
|---|---|
| ID do caso | CT-027 |
| Título | Login do administrador com credencial válida e saída |
| Requisito relacionado | RF-06 (regras: RN-11; riscos: R-03) |
| Nível/tipo | Sistema / Funcional — classificação: Positivo; interface: Tela |
| Técnica aplicada | Caso de uso (fluxo principal) |
| Prioridade | Alta |
| Pré-condições | PC-PADRÃO. Navegador sem sessão administrativa aberta. |
| Dados de entrada | Usuário: admin; Senha: admin123 (credencial fictícia) |
| Passos numerados | 1. Abrir http://localhost:8080/admin/.<br>2. Informar usuário e senha e clicar em "Entrar".<br>3. Clicar em "Sair".<br>4. Abrir novamente http://localhost:8080/admin/index.html. |
| Resultado esperado | Passo 1: tela de login. Passo 2: "Painel administrativo" com "Usuário: admin". Passo 3: tela de login com "Você saiu da área administrativa." Passo 4: redirecionamento para a tela de login. |
| Candidato à automação | Sim — Interface (Selenium, junto com o cadastro de serviço). Fluxo ponta a ponta exigido pelo manual (login admin). |
| Responsável | [PREENCHER PELO GRUPO] |

### CT-028 — Login com senha incorreta é recusado

| Campo | Conteúdo |
|---|---|
| ID do caso | CT-028 |
| Título | Login com senha incorreta é recusado |
| Requisito relacionado | RF-06 (regras: RN-11; riscos: R-03) |
| Nível/tipo | Sistema / Funcional (segurança) — classificação: Negativo; interface: Tela |
| Técnica aplicada | Particionamento de equivalência (credencial inválida) |
| Prioridade | Alta |
| Pré-condições | PC-PADRÃO. |
| Dados de entrada | Usuário: admin; Senha: senhaerrada |
| Passos numerados | 1. Abrir http://localhost:8080/admin/login.html.<br>2. Informar usuário e senha e clicar em "Entrar". |
| Resultado esperado | Mensagem "Usuário ou senha inválidos." e permanência na tela de login. |
| Candidato à automação | Não. Verificação simples e de baixo custo manual; o controle de acesso já é automatizado em CT-029. |
| Responsável | [PREENCHER PELO GRUPO] |

### CT-029 — Área administrativa e dados de clientes inacessíveis sem login

| Campo | Conteúdo |
|---|---|
| ID do caso | CT-029 |
| Título | Área administrativa e dados de clientes inacessíveis sem login |
| Requisito relacionado | RF-06 (regras: RN-11; riscos: R-03) |
| Nível/tipo | Sistema / Funcional (segurança) — classificação: Exceção; interface: Tela e API |
| Técnica aplicada | Particionamento de equivalência (sem credencial) |
| Prioridade | Alta |
| Pré-condições | PC-PADRÃO. Navegador e ferramenta de API sem sessão nem credenciais. |
| Dados de entrada | Página /admin/agenda.html; GET /api/admin/barbeiros; GET /api/clientes; POST /api/admin/servicos com {"nome": "Serviço Invasor", "duracaoMinutos": 30, "preco": 10.00} |
| Passos numerados | 1. Abrir http://localhost:8080/admin/agenda.html.<br>2. Enviar GET /api/admin/barbeiros.<br>3. Enviar GET /api/clientes.<br>4. Enviar POST /api/admin/servicos com o corpo dos dados.<br>5. Enviar GET /api/servicos. |
| Resultado esperado | Passo 1: redirecionamento para a tela de login. Passos 2 e 3: HTTP 401 com mensagem "Autenticação necessária." e sem dados. Passo 4: HTTP 403. Passo 5: "Serviço Invasor" não aparece. |
| Candidato à automação | Sim — API (Postman). Controle de acesso é risco Alto (R-03) e deve entrar em toda regressão. |
| Responsável | [PREENCHER PELO GRUPO] |

### CT-030 — Cadastrar serviços com duração e preço nos limites válidos

| Campo | Conteúdo |
|---|---|
| ID do caso | CT-030 |
| Título | Cadastrar serviços com duração e preço nos limites válidos |
| Requisito relacionado | RF-07 (regras: RN-09; riscos: R-05) |
| Nível/tipo | Sistema / Funcional — classificação: Fronteira; interface: Tela |
| Técnica aplicada | Análise de valor limite |
| Prioridade | Média |
| Pré-condições | PC-PADRÃO. Administrador autenticado. |
| Dados de entrada | (a) Nome "Acabamento", duração 15, preço 1,00; (b) Nome "Tratamento completo", duração 180, preço 1000,00 |
| Passos numerados | 1. Abrir http://localhost:8080/admin/servicos.html.<br>2. Preencher (a) e clicar em "Salvar".<br>3. Preencher (b) e clicar em "Salvar". |
| Resultado esperado | Para cada um: mensagem "Serviço cadastrado (código N)." e linha na tabela com "15 min / R$ 1,00" e "180 min / R$ 1.000,00", situação Ativo. |
| Candidato à automação | Sim — Interface (Selenium, junto com o login do administrador). Fluxo ponta a ponta exigido pelo manual (cadastro de serviço). **Automatizado: Parcial** (Unidade: ValidacaoEntradaTest#deveAceitarServicoNosLimitesValidos) |
| Responsável | [PREENCHER PELO GRUPO] |

### CT-031 — Cadastro de serviço recusa duração e preço fora dos limites

| Campo | Conteúdo |
|---|---|
| ID do caso | CT-031 |
| Título | Cadastro de serviço recusa duração e preço fora dos limites |
| Requisito relacionado | RF-07 (regras: RN-09; riscos: R-05) |
| Nível/tipo | Sistema / Funcional — classificação: Negativo; interface: Tela |
| Técnica aplicada | Análise de valor limite e particionamento (múltiplo de 15) |
| Prioridade | Média |
| Pré-condições | PC-PADRÃO. Administrador autenticado. |
| Dados de entrada | Nome "Serviço Limite"; (a) duração 14, preço 10; (b) duração 20, preço 10; (c) duração 195, preço 10; (d) duração 30, preço 0,99; (e) duração 30, preço 1000,01 |
| Passos numerados | 1. Abrir a tela de serviços.<br>2. Para cada combinação, preencher e clicar em "Salvar". |
| Resultado esperado | (a) Mensagem de erro no campo Duração — 14 viola o mínimo e o múltiplo de 15 ao mesmo tempo, então "A duração deve ser de no mínimo 15 minutos." ou "A duração deve ser múltipla de 15 minutos." é aceita. (b) "A duração deve ser múltipla de 15 minutos." (c) "A duração deve ser de no máximo 180 minutos." (d) "O preço deve ser de no mínimo R$ 1,00." (e) "O preço deve ser de no máximo R$ 1.000,00." Nenhum serviço cadastrado. |
| Candidato à automação | Sim — Unidade (validação de ServicoRequest). Cinco limites verificáveis em milissegundos. **Automatizado: Sim** (Unidade: ValidacaoEntradaTest#deveRejeitarDuracaoForaDosLimites; #deveRejeitarPrecoForaDosLimites) |
| Responsável | [PREENCHER PELO GRUPO] |

### CT-032 — Barbeiro desativado deixa de aparecer para o cliente

| Campo | Conteúdo |
|---|---|
| ID do caso | CT-032 |
| Título | Barbeiro desativado deixa de aparecer para o cliente |
| Requisito relacionado | RF-07 (regras: RN-10; riscos: R-05) |
| Nível/tipo | Sistema / Funcional — classificação: Alternativo; interface: Tela |
| Técnica aplicada | Particionamento de equivalência (ativo × inativo) |
| Prioridade | Baixa |
| Pré-condições | PC-PADRÃO. Administrador autenticado. Restaurar os dados ao final. |
| Dados de entrada | Barbeiro: Rafael Tesoura |
| Passos numerados | 1. Abrir http://localhost:8080/admin/barbeiros.html.<br>2. Clicar em "Editar" na linha de Rafael Tesoura, desmarcar "Ativo" e clicar em "Salvar".<br>3. Abrir http://localhost:8080/agendar.html e abrir a lista de barbeiros. |
| Resultado esperado | Passo 2: mensagem "Barbeiro atualizado." e situação Inativo. Passo 3: Rafael Tesoura não aparece. |
| Candidato à automação | Não. Prioridade baixa; a regra de inativos já é automatizada em CT-017. |
| Responsável | [PREENCHER PELO GRUPO] |

### CT-033 — Excluir barbeiro: recusado com agendamentos e aceito sem agendamentos

| Campo | Conteúdo |
|---|---|
| ID do caso | CT-033 |
| Título | Excluir barbeiro: recusado com agendamentos e aceito sem agendamentos |
| Requisito relacionado | RF-07 (regras: —; riscos: R-05) |
| Nível/tipo | Sistema / Funcional — classificação: Exceção; interface: Tela |
| Técnica aplicada | Particionamento de equivalência (com × sem agendamentos) |
| Prioridade | Média |
| Pré-condições | PC-PADRÃO. Administrador autenticado. |
| Dados de entrada | (a) Carlos Navalha (tem agendamentos); (b) novo barbeiro "Barbeiro Temporário" |
| Passos numerados | 1. Na tela de barbeiros, clicar em "Excluir" e em "Confirmar exclusão" na linha de Carlos Navalha.<br>2. Cadastrar "Barbeiro Temporário".<br>3. Clicar em "Excluir" e em "Confirmar exclusão" na linha de Barbeiro Temporário. |
| Resultado esperado | Passo 1: mensagem "O barbeiro possui agendamentos e não pode ser excluído. Desative-o em vez de excluir." e Carlos continua na tabela. Passo 3: mensagem "Barbeiro excluído." e a linha some. |
| Candidato à automação | Sim — Unidade (BarbeiroService.excluir com mock). Regra de integridade simples de isolar. **Automatizado: Sim** (Unidade: CadastroServiceTest#deveRejeitarExclusaoDeBarbeiroComAgendamentos; #deveExcluirBarbeiroSemAgendamentos) |
| Responsável | [PREENCHER PELO GRUPO] |

### CT-034 — Agenda do dia exibe os agendamentos e permite concluir atendimento

| Campo | Conteúdo |
|---|---|
| ID do caso | CT-034 |
| Título | Agenda do dia exibe os agendamentos e permite concluir atendimento |
| Requisito relacionado | RF-08 (regras: —; riscos: R-03) |
| Nível/tipo | Sistema / Funcional — classificação: Positivo; interface: Tela |
| Técnica aplicada | Transição de estados (AGENDADO → CONCLUIDO) |
| Prioridade | Média |
| Pré-condições | PC-PADRÃO. Administrador autenticado. |
| Dados de entrada | Barbeiro: Rafael Tesoura; Data: DF1 |
| Passos numerados | 1. Abrir http://localhost:8080/admin/agenda.html.<br>2. Selecionar barbeiro e data e clicar em "Ver agenda".<br>3. Clicar em "Concluir" na linha das 14:00. |
| Resultado esperado | Passo 2: linha "14:00 – 15:00", Bruno Henrique Lima, Corte e barba, status AGENDADO, botão "Concluir"; nenhum código de acesso exibido. Passo 3: mensagem "Atendimento #N marcado como concluído.", status CONCLUIDO e botão oculto. |
| Candidato à automação | Não. Fluxo administrativo de menor risco; a transição inválida é automatizada em CT-035. **Automatizado: Sim** (Unidade: AgendamentoServiceTest#deveConcluirAgendamentoAtivo) |
| Responsável | [PREENCHER PELO GRUPO] |

### CT-035 — Concluir agendamento cancelado é recusado

| Campo | Conteúdo |
|---|---|
| ID do caso | CT-035 |
| Título | Concluir agendamento cancelado é recusado |
| Requisito relacionado | RF-08 (regras: —; riscos: R-03) |
| Nível/tipo | Sistema / Funcional — classificação: Alternativo; interface: API |
| Técnica aplicada | Transição de estados (transição inválida) |
| Prioridade | Média |
| Pré-condições | PC-PADRÃO. Credencial de administrador (admin:admin123) via HTTP Basic. |
| Dados de entrada | Barbeiro: Carlos Navalha; Data: DF2; agendamento das 09:30 (SEMENTE4, CANCELADO) |
| Passos numerados | 1. Enviar GET /api/admin/agenda?barbeiroId={Carlos}&data=DF2 e anotar o id do agendamento das 09:30.<br>2. Enviar PATCH /api/admin/agendamentos/{id}/concluir. |
| Resultado esperado | Passo 1: o agendamento das 09:30 tem status CANCELADO. Passo 2: HTTP 409 com mensagem "Somente agendamentos com status AGENDADO podem ser concluídos." |
| Candidato à automação | Sim — Unidade (AgendamentoService.concluir com mock). Transição inválida simples de isolar. **Automatizado: Sim** (Unidade: AgendamentoServiceTest#deveRejeitarConclusaoDeAgendamentoCancelado) |
| Responsável | [PREENCHER PELO GRUPO] |

## 4. Resumo

### 4.1 Casos por requisito

| Requisito | Casos | Quantidade |
|---|---|---|
| RF-01 | CT-001, CT-002, CT-003, CT-004, CT-005, CT-006 | 6 |
| RF-02 | CT-007, CT-008, CT-009 | 3 |
| RF-03 | CT-010, CT-011, CT-012, CT-013, CT-014, CT-015, CT-016, CT-017, CT-018 | 9 |
| RF-04 | CT-008, CT-019, CT-020, CT-021, CT-022 | 5 |
| RF-05 | CT-022, CT-023, CT-024, CT-025, CT-026 | 5 |
| RF-06 | CT-027, CT-028, CT-029 | 3 |
| RF-07 | CT-030, CT-031, CT-032, CT-033 | 4 |
| RF-08 | CT-034, CT-035 | 2 |
| RNF-01 | — (testes não funcionais no P09, Marco 7) | 0 |
| RNF-02 | — (testes não funcionais no P09, Marco 7) | 0 |
| RNF-03 | — (testes não funcionais no P09, Marco 7) | 0 |
| RNF-04 | — (testes não funcionais no P09, Marco 7) | 0 |
| RNF-05 | — (testes não funcionais no P09, Marco 7) | 0 |

### 4.2 Casos por classificação

| Classificação | Quantidade |
|---|---|
| Alternativo | 6 |
| Exceção | 5 |
| Fronteira | 8 |
| Negativo | 9 |
| Positivo | 7 |

### 4.3 Casos por prioridade

| Prioridade | Quantidade |
|---|---|
| Alta | 12 |
| Média | 22 |
| Baixa | 1 |

### 4.4 Candidatos à automação

31 de 35 casos são candidatos à automação (base da taxa de automação, P10).

| Nível da automação | Casos |
|---|---|
| Unidade (JUnit) | CT-002, CT-003, CT-004, CT-006, CT-007, CT-008, CT-009, CT-011, CT-012, CT-013, CT-014, CT-015, CT-016, CT-017, CT-019, CT-021, CT-031, CT-033, CT-035 |
| API (Postman) | CT-001, CT-005, CT-006, CT-010, CT-018, CT-019, CT-020, CT-023, CT-024, CT-026, CT-029 |
| Interface (Selenium) | CT-001, CT-010, CT-023, CT-025, CT-027, CT-030 |

Situação da automação dos candidatos: 17 automatizados em todos os níveis planejados, 9 parcialmente (faltam API/interface) e 5 ainda não automatizados.

**Total de casos manuais: 35** (mínimo do manual: 24).
