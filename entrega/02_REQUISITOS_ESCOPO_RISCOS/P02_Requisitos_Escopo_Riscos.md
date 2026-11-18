# P02 — Requisitos, escopo e riscos

**Projeto Integrado P2 — Testes e Qualidade de Software — UNISAGRADO 2026**
**Sistema:** BarberAgenda 1.1.0 (tag `v1.1.0-sistema-base`) — https://github.com/ZangrandeG/barberagenda
**Grupo:** Turma A — Guilherme Ribeiro Zangrande (RA 23110757) e José Paulo Dassie Felippi (RA 24111563)

| Versão | Data | Descrição |
|---|---|---|
| v1.0 | 2026-11-18 | Primeira versão: 8 requisitos funcionais, 5 não funcionais, escopo e 11 riscos |

> **Situação:** elaborado antes da decisão do professor sobre a ficha P01 (por decisão do grupo). Se houver ajustes na aprovação, este documento ganha nova versão.
>
> **Fontes:** especificação da versão testada (`docs/ESPECIFICACAO_SISTEMA.md`), observação do sistema em execução e regras de negócio RN-01 a RN-11.

## 1. Catálogo de requisitos (Apêndice B)

**Prioridade:** Alta = falha impede o uso principal ou compromete dados; Média = prejudica parte do uso, mas há alternativa; Baixa = incômodo sem prejuízo funcional.

### 1.1 Requisitos funcionais

| ID | Descrição verificável | Tipo | Prioridade | Critério de aceitação verificável |
|---|---|---|---|---|
| RF-01 | O cliente se cadastra informando nome, telefone e e-mail. Regras RN-01 (nome com 3 a 60 caracteres), RN-02 (telefone só com dígitos, 10 ou 11) e RN-03 (e-mail válido e único). | Funcional | Alta | (a) Dados válidos → HTTP 201, cliente criado com id e mensagem "Cadastro realizado com sucesso!" na tela. (b) Nome com 2 ou 61 caracteres, telefone com 9 ou 12 dígitos ou com letras, e-mail sem "@" ou sem domínio → HTTP 400 com a mensagem do campo correspondente, e nenhum cliente criado. (c) E-mail já cadastrado, mesmo com letras maiúsculas → HTTP 409 e nenhum cliente criado. |
| RF-02 | O sistema informa os horários de início disponíveis para um barbeiro ativo, um serviço ativo e uma data. | Funcional | Alta | (a) São listados somente horários a partir de 09:00, de 30 em 30 minutos, cujo término (início + duração) seja até 19:00. (b) Não são listados horários que se sobrepõem a agendamentos `AGENDADO` do barbeiro nem horários que já passaram. (c) Domingo, data passada ou data além de hoje + 30 dias → lista vazia. (d) Barbeiro ou serviço inativo → HTTP 400; inexistente → HTTP 404. |
| RF-03 | O cliente cadastrado cria um agendamento escolhendo barbeiro, serviço, data e horário. Regras RN-04, RN-05, RN-06 e RN-10. | Funcional | Alta | (a) Pedido válido → HTTP 201, status `AGENDADO`, término = início + duração do serviço e código de acesso de 8 caracteres exibido ao cliente. (b) Início antes de 09:00, término depois de 19:00, domingo, minuto diferente de 00/30, horário passado ou data além de hoje + 30 → HTTP 400 com mensagem da regra, sem agendamento criado. (c) Barbeiro ou serviço inativo → HTTP 400. (d) E-mail não cadastrado → HTTP 404. |
| RF-04 | O sistema impede conflito de horário do barbeiro (RN-07) e limita a 3 os agendamentos ativos por cliente (RN-08). | Funcional | Alta | (a) Pedido que se sobrepõe a agendamento `AGENDADO` do mesmo barbeiro → HTTP 409. (b) Horário encostado (um termina 10:30 e o outro começa 10:30) e o mesmo horário com outro barbeiro → aceitos (201). (c) 3º agendamento ativo do cliente → aceito; 4º → HTTP 409. (d) Após o cancelamento de um deles, um novo agendamento é aceito. |
| RF-05 | O cliente consulta e cancela o próprio agendamento informando o código de acesso e o e-mail. | Funcional | Alta | (a) Código (maiúsculas ou minúsculas) e e-mail corretos → HTTP 200 com barbeiro, serviço, data/hora, valor e status. (b) E-mail divergente, código inexistente ou id numérico → HTTP 404 com a mesma mensagem. (c) Cancelar agendamento `AGENDADO` → status `CANCELADO` e o horário volta a aparecer como disponível. (d) Cancelar agendamento `CANCELADO` ou `CONCLUIDO` → HTTP 409. |
| RF-06 | O administrador acessa a área administrativa com usuário e senha (RN-11). | Funcional | Alta | (a) Credencial válida → acesso ao painel com o nome do usuário exibido. (b) Senha errada → mensagem "Usuário ou senha inválidos." e permanência na tela de login. (c) Página `/admin/*` sem login → redirecionamento para a tela de login. (d) API administrativa sem credenciais → HTTP 401 (consulta) ou 403 (alteração), sem dados no corpo. (e) "Sair" encerra a sessão: a página administrativa volta a exigir login. |
| RF-07 | O administrador cadastra, edita, desativa e exclui barbeiros e serviços. Regras RN-09 e RN-10. | Funcional | Média | (a) Serviço com duração 15 a 180 minutos, múltipla de 15, e preço de R$ 1,00 a R$ 1.000,00 → HTTP 201. (b) Duração 14, 20 ou 195 e preço 0,99 ou 1.000,01 → HTTP 400 com mensagem do campo. (c) Barbeiro ou serviço desativado deixa de aparecer para o cliente. (d) Excluir item sem agendamentos → HTTP 204; com agendamentos → HTTP 409. |
| RF-08 | O administrador consulta a agenda do dia de um barbeiro e marca atendimentos como concluídos. | Funcional | Média | (a) A agenda lista todos os agendamentos do barbeiro na data (qualquer status), em ordem de horário, sem exibir códigos de acesso. (b) Concluir agendamento `AGENDADO` → status `CONCLUIDO`. (c) Concluir agendamento já `CANCELADO` ou `CONCLUIDO` → HTTP 409. |

### 1.2 Requisitos não funcionais

| ID | Descrição verificável | Tipo | Prioridade | Critério de aceitação verificável |
|---|---|---|---|---|
| RNF-01 | Desempenho básico das operações principais do cliente. | Não funcional (desempenho) | Média | Em ambiente local (perfil `test`), 30 requisições de `GET /api/horarios-disponiveis` e 30 de `POST /api/agendamentos`, após 5 requisições de aquecimento: **p95 < 500 ms** em cada operação; média e p95 registrados. |
| RNF-02 | Segurança básica: controle de acesso, proteção de credenciais e de dados exibidos. | Não funcional (segurança) | Alta | (a) Nenhuma rota `/api/admin/**` nem `GET /api/clientes` devolve dados sem credencial. (b) A senha do administrador é armazenada apenas como hash BCrypt (valor iniciando com `$2a$`, `$2b$` ou `$2y$`), nunca em texto. (c) Nome com `<script>alert(1)</script>` é exibido como texto, sem executar. (d) Nenhuma resposta de erro contém stack trace ou nome de classe Java. |
| RNF-03 | Compatibilidade de navegador e resolução. | Não funcional (compatibilidade) | Média | Os fluxos de cadastro, agendamento e consulta são concluídos no Chrome e no Firefox, nas resoluções 1366×768 e 375×667, sem rolagem horizontal da página e com todos os campos e botões visíveis. |
| RNF-04 | Confiabilidade: persistência e tratamento de falhas. | Não funcional (confiabilidade) | Média | (a) Após reinício controlado da aplicação no perfil `dev`, 100% dos clientes e agendamentos criados antes do reinício continuam disponíveis com os mesmos dados. (b) Entradas inválidas (JSON malformado, tipos errados, parâmetros ausentes) nunca produzem HTTP 500. |
| RNF-05 | Usabilidade do fluxo de agendamento. | Não funcional (usabilidade) | Média | Participante externo ao grupo, sem instruções além do objetivo da tarefa, conclui cadastro + agendamento em **até 5 minutos**, sem ajuda, e avalia a facilidade com nota **≥ 4 em 5**. |

**Totais:** 8 requisitos funcionais e 5 não funcionais (13 no escopo; mínimo do manual: 8, com ≥ 6 RF e ≥ 2 RNF).

## 2. Escopo

### 2.1 Dentro do escopo

- Os requisitos RF-01 a RF-08 e RNF-01 a RNF-05 acima, na versão 1.1.0.
- Interface web (páginas públicas e administrativas), API REST e persistência no H2 (perfis `dev` e `test`).
- Navegadores Chrome e Firefox (versões instaladas no ambiente de testes).
- A evolução por TDD (Marco 9), que acrescentará um requisito (antecedência mínima para cancelamento) com nova versão deste documento.

### 2.2 Fora do escopo

| Item | Motivo |
|---|---|
| Regra de antecedência mínima para cancelamento | Ainda não existe; será criada pelo ciclo de TDD no Marco 9 e só então entrará no escopo. |
| Login de clientes, recuperação de código de acesso, cadastro de vários administradores | Não existem no sistema. |
| Pagamentos, notificações por e-mail/SMS | Não existem no sistema. |
| Perfil PostgreSQL (`docker-compose.yml`) | Opcional; não há Docker no ambiente do grupo. O banco testado é o H2. |
| Testes de carga, estresse e invasão | Proibidos ou desnecessários pela seção 15 do manual; desempenho é verificado apenas de forma básica (RNF-01). |
| Concorrência real (pedidos simultâneos para o mesmo horário) | Exige carga paralela; o bloqueio existe no código, mas não será testado dinamicamente. |
| Navegadores Safari/Edge e dispositivos iOS | Indisponíveis no ambiente do grupo. |
| Conformidade formal de acessibilidade (WCAG) e outros idiomas/fusos | Não fazem parte dos objetivos do sistema; fuso fixo `America/Sao_Paulo`. |
| Rota de apoio `POST /api/dev/reset` como funcionalidade | É ferramenta de teste; seu controle de acesso entra em RNF-02. |

## 3. Matriz de riscos do produto (Apêndice C)

**Probabilidade:** Baixa (pouco provável), Média (possível), Alta (provável ou recorrente).
**Impacto:** Baixo (consequência pequena e reversível), Médio (prejudica parte do uso, mas há alternativa), Alto (bloqueia tarefa importante ou compromete dados).
**Prioridade:** combinação das duas — Alta (executar primeiro e repetir após correções), Média (ciclo principal), Baixa (após os fluxos principais).

| ID | Risco | Requisito | Probabilidade | Impacto | Prioridade | Resposta / teste |
|---|---|---|---|---|---|---|
| R-01 | Dois clientes agendados para o mesmo barbeiro em horários sobrepostos. | RF-04 | Média | Alto | **Alta** | Casos de sobreposição total, parcial e encostada (valor limite); testes de unidade da verificação de sobreposição; teste de API com 409; regressão a cada correção. |
| R-02 | Agendamento aceito fora do funcionamento, no domingo ou fora dos intervalos de 30 minutos. | RF-03, RF-02 | Média | Alto | **Alta** | Valor limite de início (08:30, 09:00) e de término (19:00, 19:15/19:30); domingo; minutos 00/15/30; testes de unidade com relógio fixo. |
| R-03 | Acesso à área administrativa ou a dados pessoais sem autenticação. | RF-06, RNF-02 | Média | Alto | **Alta** | Acesso direto às páginas e à API sem login, com senha errada e sem token CSRF; verificação de 401/403 e de corpo sem dados. |
| R-04 | Regras de data falham perto dos limites (horário que acabou de passar, 30 e 31 dias). | RF-03, RF-02 | Média | Médio | Média | Valor limite de antecedência (hoje em horário passado, hoje + 30, hoje + 31); testes de unidade com `Clock` fixo. |
| R-05 | Dados inválidos aceitos no cadastro de cliente ou de serviço. | RF-01, RF-07 | Média | Médio | Média | Partições e limites de nome, telefone, e-mail, duração e preço; verificação de que nenhum registro é criado no erro. |
| R-06 | Cliente ultrapassa o limite de 3 agendamentos ativos. | RF-04 | Baixa | Médio | Média | Casos do 3º e do 4º agendamento; cancelamento libera nova vaga. |
| R-07 | Pessoa consulta ou cancela agendamento de outra. | RF-05 | Baixa | Alto | Média | Consulta com e-mail divergente, código inexistente e id numérico; cancelamento com e-mail errado. |
| R-08 | Texto digitado com HTML/script é executado na página. | RNF-02 | Baixa | Alto | Média | Cadastro com `<script>` e `<img onerror>` e verificação visual nas telas de consulta e da agenda administrativa. |
| R-09 | Interface inutilizável no celular ou no Firefox. | RNF-03 | Média | Médio | Média | Execução dos fluxos e da suíte Selenium em Chrome/Firefox e em 375×667. |
| R-10 | Perda de agendamentos após reinício da aplicação. | RNF-04 | Baixa | Alto | Média | Criar dados, reiniciar no perfil `dev` e comparar. |
| R-11 | Consulta de horários lenta, prejudicando o agendamento. | RNF-01, RF-02 | Baixa | Baixo | Baixa | Medição de 30 repetições com média e p95. |

## 4. Relação requisito × risco

| Requisito | Riscos |
|---|---|
| RF-01 | R-05 |
| RF-02 | R-02, R-04, R-11 |
| RF-03 | R-02, R-04 |
| RF-04 | R-01, R-06 |
| RF-05 | R-07 |
| RF-06 | R-03 |
| RF-07 | R-05 |
| RF-08 | R-03 (área restrita) |
| RNF-01 | R-11 |
| RNF-02 | R-03, R-08 |
| RNF-03 | R-09 |
| RNF-04 | R-10 |
| RNF-05 | R-09 (usabilidade em telas pequenas) |

Esta relação será estendida até casos, execuções e defeitos na Matriz de Rastreabilidade (P05, Marco 3).
