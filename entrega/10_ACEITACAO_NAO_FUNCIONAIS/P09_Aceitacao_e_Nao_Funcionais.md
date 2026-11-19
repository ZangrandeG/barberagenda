# P09 — Testes de aceitação e não funcionais (Marco 7)

**Projeto Integrado P2 — BarberAgenda 1.1.0** — Turma A — Guilherme Ribeiro Zangrande e José Paulo Dassie Felippi

| Versão | Data | Descrição |
|---|---|---|
| v1.0 | 2026-11-18 | 4 cenários de aceitação (a executar por pessoa externa) e 8 testes não funcionais em 5 categorias (7 executados) |

## Parte A — Testes de aceitação

Cenários escritos do ponto de vista do **cliente** e do **dono da barbearia**, para execução por uma **pessoa que não participou da construção dos testes** (manual, seção 9.11). O grupo prepara o ambiente (perfil `dev`, dados restaurados com `scripts/reset-dados`) e apenas observa: não orienta a execução.

> **Situação:** cenários prontos; **ainda não executados**. Os campos de resultado só podem ser preenchidos com a execução real pela pessoa externa.

**Participante:** [PREENCHER PELO GRUPO — nome e papel (ex.: colega de outro grupo, cliente de barbearia)] — **Data:** [PREENCHER] — **Versão:** BarberAgenda 1.1.0

### CA-01 — Cliente novo agenda o primeiro corte (RF-01, RF-02, RF-03)

| Campo | Conteúdo |
|---|---|
| Objetivo | Verificar se um cliente sem cadastro consegue se cadastrar e agendar sozinho |
| Dado que | sou um cliente que nunca usou o sistema |
| Quando | me cadastro e agendo um "Corte de cabelo" com qualquer barbeiro, no primeiro horário livre de um dia útil da próxima semana |
| Então | vejo a confirmação com um **código de acesso** e o resumo (barbeiro, serviço, data e horário) igual ao que escolhi |
| Dados | Nome e telefone fictícios à escolha; e-mail `aceitacao.<data>@exemplo.com` |
| Critério de sucesso | Concluído sem ajuda, em até 5 minutos, com o resumo correto |
| Resultado observado / dificuldades | [PREENCHER PELO GRUPO] |
| Decisão | [PREENCHER] Aceito / Aceito com ressalvas / Não aceito |

### CA-02 — Cliente desiste e cancela o agendamento (RF-05)

| Campo | Conteúdo |
|---|---|
| Objetivo | Verificar se o cliente consegue cancelar sozinho e se o horário volta a ficar livre |
| Dado que | tenho o agendamento de código `SEMENTE2` (e-mail `ana.rocha@exemplo.com`) |
| Quando | consulto meu agendamento e o cancelo |
| Então | o status passa a CANCELADO e o mesmo horário volta a aparecer para novos agendamentos |
| Critério de sucesso | Cancelamento concluído sem ajuda e horário liberado |
| Resultado observado / dificuldades | [PREENCHER PELO GRUPO] |
| Decisão | [PREENCHER] Aceito / Aceito com ressalvas / Não aceito |

### CA-03 — O sistema protege a agenda do barbeiro (RF-04)

| Campo | Conteúdo |
|---|---|
| Objetivo | Verificar, do ponto de vista do dono, que nenhum barbeiro recebe dois clientes ao mesmo tempo |
| Dado que | Rafael Tesoura já atende das 14:00 às 15:00 no próximo dia de funcionamento (massa fictícia) |
| Quando | tento agendar Rafael Tesoura nesse dia, com um serviço de 30 minutos |
| Então | os horários 14:00 e 14:30 não são oferecidos, e 13:30 e 15:00 são |
| Critério de sucesso | Nenhum horário em conflito oferecido |
| Resultado observado / dificuldades | [PREENCHER PELO GRUPO] |
| Decisão | [PREENCHER] Aceito / Aceito com ressalvas / Não aceito |

### CA-04 — Dono organiza o dia de trabalho (RF-06, RF-07, RF-08)

| Campo | Conteúdo |
|---|---|
| Objetivo | Verificar se o dono consegue administrar serviços e a agenda do dia |
| Dado que | sou o dono e tenho acesso à área administrativa (`admin` / `admin123`, credencial fictícia) |
| Quando | cadastro o serviço "Pezinho" (15 min, R$ 10,00), abro a agenda de Rafael Tesoura no próximo dia de funcionamento e marco o atendimento das 14:00 como concluído |
| Então | o serviço aparece para os clientes na tela de agendamento e o atendimento fica CONCLUIDO |
| Critério de sucesso | As três tarefas concluídas sem ajuda |
| Resultado observado / dificuldades | [PREENCHER PELO GRUPO] |
| Decisão | [PREENCHER] Aceito / Aceito com ressalvas / Não aceito |

## Parte B — Testes não funcionais (Apêndice I)

**Ambiente comum:** Windows 11 Pro 10.0.26200; Java 21.0.13; BarberAgenda 1.1.0 local (`http://localhost:8080`), perfil `test` (H2 em memória) salvo indicação; Chrome 157, Firefox 160; Python 3.11 (scripts em `scripts/nf/`). Executados em 2026-11-18 por Claude (IA), por scripts e testes automatizados, a pedido do grupo. Evidências em `evidencias/`.

| ID | Categoria | Requisito | Resultado | Conclusão |
|---|---|---|---|---|
| TNF-01 | Desempenho básico | RNF-01 | p95 26,2 ms (horários) e 33,6 ms (agendar) | Atende |
| TNF-02 | Segurança básica — acesso | RNF-02 (a, d) | 28/28 respostas 401/403 sem dados nem detalhes internos | Atende |
| TNF-03 | Segurança básica — senha | RNF-02 (b) | Hash BCrypt `$2a$10$…` (60 caracteres); texto da senha ausente do banco | Atende |
| TNF-04 | Segurança básica — HTML/script | RNF-02 (c) | Exibido como texto; nenhum alerta executado (Chrome e Firefox) | Atende |
| TNF-05 | Confiabilidade — reinício | RNF-04 (a) | Cliente e agendamento iguais após parar e subir a aplicação | Atende |
| TNF-06 | Confiabilidade — entradas inválidas | RNF-04 (b) | 16/16 entradas inválidas com 4xx, nenhuma 500 | Atende |
| TNF-07 | Compatibilidade | RNF-03 | 11/11 testes em cada uma das 4 combinações navegador × resolução | Atende |
| TNF-08 | Usabilidade | RNF-05 | Não executado (requer participante externo) | — |

### TNF-01 — Desempenho básico

| Campo | Conteúdo |
|---|---|
| ID e categoria | TNF-01 — Desempenho básico |
| Objetivo | Medir o tempo de resposta das operações principais do cliente |
| Ambiente | Comum (perfil `test`); cliente e servidor na mesma máquina |
| Métrica/critério | Média e percentil 95 (posto mais próximo) do tempo de resposta; critério **p95 < 500 ms** por operação |
| Procedimento | `python scripts/nf/desempenho.py <pasta>`: restaura os dados, faz 5 requisições de aquecimento e mede 30 de cada operação (tempo da requisição até a leitura completa da resposta) |
| Dados e repetições | `GET /api/horarios-disponiveis` (Carlos Navalha, Corte de cabelo, data 7 dias à frente); `POST /api/agendamentos` com 35 pedidos válidos em horários livres distintos (12 clientes criados, até 3 agendamentos por cliente). 30 medições por operação |
| Resultado obtido | Horários: média 16,3 ms, p95 26,2 ms, máximo 30,2 ms. Agendar: média 17,4 ms, p95 33,6 ms, máximo 33,8 ms |
| Conclusão | **Atende** |
| Evidências | `evidencias/TNF-01_desempenho_resultado.json`, `evidencias/TNF-01_desempenho_amostras.csv` (as 60 medições) |

### TNF-02 — Segurança básica: controle de acesso e exposição indevida

| Campo | Conteúdo |
|---|---|
| ID e categoria | TNF-02 — Segurança básica |
| Objetivo | Garantir que rotas administrativas e de dados pessoais não respondam dados sem credencial válida e que erros não exponham detalhes internos |
| Ambiente | Comum (perfil `test`) |
| Métrica/critério | Toda requisição sem credencial ou com senha errada recebe 401 ou 403, com corpo contendo apenas `{status, erro, mensagem, campos}` e sem stack trace, nomes de classes ou SQL |
| Procedimento | `python scripts/nf/seguranca_robustez.py <pasta>` — 14 rotas restritas (GET/POST/PUT/DELETE/PATCH de `/api/admin/**`, `GET /api/clientes`, `/api/clientes/{id}`, `POST /api/dev/reset`) × 2 cenários (sem credencial; senha errada). Os dados são restaurados ao final |
| Dados e repetições | 28 requisições |
| Resultado obtido | 28/28 conforme o critério (consultas sem credencial: 401; alterações sem credencial: 403, pois o token CSRF é verificado antes; senha errada: 401) |
| Conclusão | **Atende** |
| Evidências | `evidencias/TNF-02_seguranca_acesso.json`, `evidencias/TNF-02_TNF-06_saida.txt` |

### TNF-03 — Segurança básica: armazenamento da senha

| Campo | Conteúdo |
|---|---|
| ID e categoria | TNF-03 — Segurança básica |
| Objetivo | Verificar que a senha do administrador não é armazenada em texto |
| Ambiente | Aplicação no perfil `dev` com banco H2 em arquivo temporário (porta 8099) |
| Métrica/critério | Valor da coluna `SENHA_HASH` é um hash BCrypt (`$2a$`/`$2b$`/`$2y$`, 60 caracteres) e o texto `admin123` não aparece no banco |
| Procedimento | `python scripts/nf/reinicio_e_senha.py <pasta>`: com a aplicação parada, consulta direta ao arquivo do banco com o H2 Shell (`SELECT LOGIN, SENHA_HASH FROM USUARIO`) |
| Dados e repetições | 1 consulta |
| Resultado obtido | Prefixo `$2a$10$` (BCrypt, custo 10), 60 caracteres; texto da senha ausente |
| Conclusão | **Atende** |
| Evidências | `evidencias/TNF-05_TNF-03_resultado.json` (somente prefixo e tamanho do hash) |

### TNF-04 — Segurança básica: HTML/script digitado pelo usuário

| Campo | Conteúdo |
|---|---|
| ID e categoria | TNF-04 — Segurança básica |
| Objetivo | Verificar que conteúdo HTML/JavaScript digitado não é executado na interface |
| Ambiente | Chrome 157 e Firefox 160, headless, 1366×768 e 375×667 |
| Métrica/critério | O nome `<img src=x onerror=alert('xss')>` aparece literalmente, nenhum elemento `<img>` é criado e nenhum alerta é aberto |
| Procedimento | Teste Selenium `SegurancaE2ETest`: cadastra o cliente com esse nome pela tela, agenda e consulta o agendamento |
| Dados e repetições | 4 execuções (2 navegadores × 2 resoluções) |
| Resultado obtido | 4/4 aprovadas |
| Conclusão | **Atende** |
| Evidências | `evidencias/TNF-07_compatibilidade/` (logs, relatórios e capturas `SegurancaE2ETest_*`) |

### TNF-05 — Confiabilidade: recuperação após reinício

| Campo | Conteúdo |
|---|---|
| ID e categoria | TNF-05 — Confiabilidade |
| Objetivo | Verificar que os dados permanecem após a aplicação ser encerrada e iniciada novamente |
| Ambiente | Perfil `dev` (H2 em arquivo temporário), porta 8099 |
| Métrica/critério | 100% dos dados criados antes da parada iguais depois do reinício |
| Procedimento | `python scripts/nf/reinicio_e_senha.py <pasta>`: sobe a aplicação, cria cliente e agendamento, aguarda 3 s, encerra o processo, sobe de novo e consulta o agendamento pelo código de acesso e e-mail |
| Dados e repetições | 1 cliente e 1 agendamento (código `TDESX7X4`); 1 ciclo de parada e reinício |
| Resultado obtido | Agendamento encontrado (HTTP 200) com código, cliente, barbeiro, serviço, data/hora e status iguais |
| Conclusão | **Atende** |
| Evidências | `evidencias/TNF-05_TNF-03_resultado.json`, `evidencias/TNF-05_aplicacao.log` |

### TNF-06 — Confiabilidade: tratamento de entradas inválidas

| Campo | Conteúdo |
|---|---|
| ID e categoria | TNF-06 — Confiabilidade |
| Objetivo | Verificar que entradas inválidas são tratadas sem falha interna |
| Ambiente | Comum (perfil `test`) |
| Métrica/critério | Nenhuma resposta HTTP 500; todas 4xx sem detalhes internos |
| Procedimento | `python scripts/nf/seguranca_robustez.py <pasta>` |
| Dados e repetições | 16 entradas: JSON malformado, corpo vazio, tipo errado, data em formato inválido, campos nulos, número gigante, textos de 10.000 caracteres, parâmetro ausente, parâmetro de tipo errado, data inexistente (30/02), barbeiro inexistente, código com caracteres especiais, rota inexistente, método não suportado, tipo de conteúdo não suportado, cancelamento sem e-mail |
| Resultado obtido | 16/16 com respostas 400, 404, 405 ou 415, sem detalhes internos |
| Conclusão | **Atende** |
| Evidências | `evidencias/TNF-06_entradas_invalidas.json`, `evidencias/TNF-02_TNF-06_saida.txt` |

### TNF-07 — Compatibilidade de navegador e resolução

| Campo | Conteúdo |
|---|---|
| ID e categoria | TNF-07 — Compatibilidade |
| Objetivo | Verificar que os fluxos principais funcionam em navegadores e tamanhos de tela diferentes |
| Ambiente | Chrome 157 e Firefox 160 (headless); janelas 1366×768 (desktop) e 375×667 (celular) |
| Métrica/critério | Todos os testes E2E aprovados em cada combinação; nenhuma página com rolagem horizontal; botão principal visível |
| Procedimento | `./mvnw test -Pe2e -Dnavegador=<chrome\|firefox> -Djanela=<1366x768\|375x667>`: os 5 testes de fluxo (cadastro, agendamento, consulta/cancelamento, administração), o TNF-04 e `CompatibilidadeE2ETest` (5 páginas: largura do conteúdo ≤ largura visível) |
| Dados e repetições | 4 combinações × 11 testes = 44 execuções |
| Resultado obtido | 44/44 aprovadas (11/11 em cada combinação) |
| Conclusão | **Atende** |
| Evidências | `evidencias/TNF-07_compatibilidade/` (um log e um relatório Surefire por combinação; capturas com navegador e resolução no nome) |

### TNF-08 — Usabilidade

| Campo | Conteúdo |
|---|---|
| ID e categoria | TNF-08 — Usabilidade |
| Objetivo | Avaliar se um usuário sem treinamento consegue se cadastrar e agendar |
| Ambiente | Notebook do grupo, Chrome, perfil `dev` com dados restaurados |
| Métrica/critério | RNF-05: cadastro + agendamento em até 5 minutos, sem ajuda, e facilidade avaliada com nota ≥ 4 de 5 |
| Procedimento | Roteiro e questionário em `P09_Roteiro_Usabilidade.md` |
| Dados e repetições | 1 participante externo (mínimo) |
| Resultado obtido | [PREENCHER PELO GRUPO após a sessão] |
| Conclusão | [PREENCHER] Atende / Atende parcialmente / Não atende |
| Evidências | [PREENCHER — folha de observação e questionário respondido] |
