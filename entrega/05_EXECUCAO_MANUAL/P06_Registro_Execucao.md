# P06 — Registro de execução (Apêndice F)

> Arquivo gerado por `scripts/gerar_artefatos.py` a partir de `dados/execucoes.csv`. Não editar à mão.

## 1. Execuções

| Execução | Caso | Data | Versão | Executor | Resultado | Evidência | Defeito | Observações |
|---|---|---|---|---|---|---|---|---|
| — | — | — | — | — | Nenhuma execução registrada | — | — | |

## 2. Situação atual de cada caso

| Caso | Título | Execuções | Resultado atual |
|---|---|---|---|
| CT-001 | Cadastrar cliente com dados válidos | — | Não executado |
| CT-002 | Cadastro aceita nome e telefone nos limites válidos | — | Não executado |
| CT-003 | Cadastro recusa nome com 2 e com 61 caracteres | — | Não executado |
| CT-004 | Cadastro recusa telefone fora do padrão | — | Não executado |
| CT-005 | Cadastro recusa e-mail em formato inválido | — | Não executado |
| CT-006 | Cadastro recusa e-mail já cadastrado, mesmo com maiúsculas | — | Não executado |
| CT-007 | Horários disponíveis respeitam funcionamento, intervalo e duração do serviço | — | Não executado |
| CT-008 | Horários ocupados pelo barbeiro não são oferecidos | — | Não executado |
| CT-009 | Datas sem atendimento retornam lista de horários vazia | — | Não executado |
| CT-010 | Agendar horário pela tela com sucesso | — | Não executado |
| CT-011 | Agendamento aceito no primeiro e no último horário do dia | — | Não executado |
| CT-012 | Agendamento recusado quando começa antes de 09:00 ou termina depois de 19:00 | — | Não executado |
| CT-013 | Agendamento recusado fora dos intervalos de 30 minutos | — | Não executado |
| CT-014 | Agendamento recusado no domingo | — | Não executado |
| CT-015 | Antecedência: aceita D+30 e recusa D+31 | — | Não executado |
| CT-016 | Agendamento recusado em data ou horário que já passou | — | Não executado |
| CT-017 | Barbeiro e serviço inativos não são oferecidos nem aceitos | — | Não executado |
| CT-018 | Agendamento com e-mail não cadastrado é recusado | — | Não executado |
| CT-019 | Agendamento sobreposto ao de outro cliente com o mesmo barbeiro é recusado | — | Não executado |
| CT-020 | Horário encostado e mesmo horário com outro barbeiro são aceitos | — | Não executado |
| CT-021 | Limite de agendamentos ativos: 3º aceito e 4º recusado | — | Não executado |
| CT-022 | Após cancelar um agendamento, cliente no limite volta a poder agendar | — | Não executado |
| CT-023 | Consultar agendamento com código de acesso (em minúsculas) e e-mail | — | Não executado |
| CT-024 | Consulta recusada quando código e e-mail não conferem | — | Não executado |
| CT-025 | Cancelar agendamento pela tela libera o horário | — | Não executado |
| CT-026 | Cancelar agendamento já cancelado ou concluído é recusado | — | Não executado |
| CT-027 | Login do administrador com credencial válida e saída | — | Não executado |
| CT-028 | Login com senha incorreta é recusado | — | Não executado |
| CT-029 | Área administrativa e dados de clientes inacessíveis sem login | — | Não executado |
| CT-030 | Cadastrar serviços com duração e preço nos limites válidos | — | Não executado |
| CT-031 | Cadastro de serviço recusa duração e preço fora dos limites | — | Não executado |
| CT-032 | Barbeiro desativado deixa de aparecer para o cliente | — | Não executado |
| CT-033 | Excluir barbeiro: recusado com agendamentos e aceito sem agendamentos | — | Não executado |
| CT-034 | Agenda do dia exibe os agendamentos e permite concluir atendimento | — | Não executado |
| CT-035 | Concluir agendamento cancelado é recusado | — | Não executado |

## 3. Resumo

| Resultado atual | Casos |
|---|---|
| Aprovado | 0 |
| Reprovado | 0 |
| Bloqueado | 0 |
| Não executado | 35 |
