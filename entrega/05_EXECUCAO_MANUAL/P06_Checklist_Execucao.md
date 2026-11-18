# P06 — Checklist de execução manual

> Arquivo gerado por `scripts/gerar_artefatos.py`. Ordem de execução: prioridade do risco (Alta → Média → Baixa).
> Instruções completas em `P06_Roteiro_Execucao.md`. Use este checklist impresso ou como cópia de trabalho;
> o registro oficial dos resultados é `dados/execucoes.csv` (que gera `P06_Registro_Execucao.md` e a aba Execuções do P05).

Executor(es): [PREENCHER] — Data: [PREENCHER] — Versão sob teste: [PREENCHER tag/commit]

| ✓ | Ordem | Caso | Título | Prioridade | Interface | Requisito | Execução | Resultado | Evidência | Defeito |
|---|---|---|---|---|---|---|---|---|---|---|
| ☐ | 1 | CT-007 | Horários disponíveis respeitam funcionamento, intervalo e duração do serviço | Alta | Tela | RF-02 | EX-___ | | | |
| ☐ | 2 | CT-008 | Horários ocupados pelo barbeiro não são oferecidos | Alta | Tela | RF-02, RF-04 | EX-___ | | | |
| ☐ | 3 | CT-010 | Agendar horário pela tela com sucesso | Alta | Tela | RF-03 | EX-___ | | | |
| ☐ | 4 | CT-011 | Agendamento aceito no primeiro e no último horário do dia | Alta | Tela | RF-03 | EX-___ | | | |
| ☐ | 5 | CT-012 | Agendamento recusado quando começa antes de 09:00 ou termina depois de 19:00 | Alta | API | RF-03 | EX-___ | | | |
| ☐ | 6 | CT-013 | Agendamento recusado fora dos intervalos de 30 minutos | Alta | API | RF-03 | EX-___ | | | |
| ☐ | 7 | CT-014 | Agendamento recusado no domingo | Alta | API | RF-03 | EX-___ | | | |
| ☐ | 8 | CT-019 | Agendamento sobreposto ao de outro cliente com o mesmo barbeiro é recusado | Alta | API | RF-04 | EX-___ | | | |
| ☐ | 9 | CT-020 | Horário encostado e mesmo horário com outro barbeiro são aceitos | Alta | API | RF-04 | EX-___ | | | |
| ☐ | 10 | CT-027 | Login do administrador com credencial válida e saída | Alta | Tela | RF-06 | EX-___ | | | |
| ☐ | 11 | CT-028 | Login com senha incorreta é recusado | Alta | Tela | RF-06 | EX-___ | | | |
| ☐ | 12 | CT-029 | Área administrativa e dados de clientes inacessíveis sem login | Alta | Tela e API | RF-06 | EX-___ | | | |
| ☐ | 13 | CT-001 | Cadastrar cliente com dados válidos | Média | Tela | RF-01 | EX-___ | | | |
| ☐ | 14 | CT-002 | Cadastro aceita nome e telefone nos limites válidos | Média | Tela | RF-01 | EX-___ | | | |
| ☐ | 15 | CT-003 | Cadastro recusa nome com 2 e com 61 caracteres | Média | Tela | RF-01 | EX-___ | | | |
| ☐ | 16 | CT-004 | Cadastro recusa telefone fora do padrão | Média | Tela | RF-01 | EX-___ | | | |
| ☐ | 17 | CT-005 | Cadastro recusa e-mail em formato inválido | Média | Tela | RF-01 | EX-___ | | | |
| ☐ | 18 | CT-006 | Cadastro recusa e-mail já cadastrado, mesmo com maiúsculas | Média | Tela | RF-01 | EX-___ | | | |
| ☐ | 19 | CT-009 | Datas sem atendimento retornam lista de horários vazia | Média | API | RF-02 | EX-___ | | | |
| ☐ | 20 | CT-015 | Antecedência: aceita D+30 e recusa D+31 | Média | API | RF-03 | EX-___ | | | |
| ☐ | 21 | CT-016 | Agendamento recusado em data ou horário que já passou | Média | API | RF-03 | EX-___ | | | |
| ☐ | 22 | CT-017 | Barbeiro e serviço inativos não são oferecidos nem aceitos | Média | Tela e API | RF-03 | EX-___ | | | |
| ☐ | 23 | CT-018 | Agendamento com e-mail não cadastrado é recusado | Média | Tela | RF-03 | EX-___ | | | |
| ☐ | 24 | CT-021 | Limite de agendamentos ativos: 3º aceito e 4º recusado | Média | API | RF-04 | EX-___ | | | |
| ☐ | 25 | CT-022 | Após cancelar um agendamento, cliente no limite volta a poder agendar | Média | Tela e API | RF-04, RF-05 | EX-___ | | | |
| ☐ | 26 | CT-023 | Consultar agendamento com código de acesso (em minúsculas) e e-mail | Média | Tela | RF-05 | EX-___ | | | |
| ☐ | 27 | CT-024 | Consulta recusada quando código e e-mail não conferem | Média | Tela | RF-05 | EX-___ | | | |
| ☐ | 28 | CT-025 | Cancelar agendamento pela tela libera o horário | Média | Tela | RF-05 | EX-___ | | | |
| ☐ | 29 | CT-026 | Cancelar agendamento já cancelado ou concluído é recusado | Média | Tela e API | RF-05 | EX-___ | | | |
| ☐ | 30 | CT-030 | Cadastrar serviços com duração e preço nos limites válidos | Média | Tela | RF-07 | EX-___ | | | |
| ☐ | 31 | CT-031 | Cadastro de serviço recusa duração e preço fora dos limites | Média | Tela | RF-07 | EX-___ | | | |
| ☐ | 32 | CT-033 | Excluir barbeiro: recusado com agendamentos e aceito sem agendamentos | Média | Tela | RF-07 | EX-___ | | | |
| ☐ | 33 | CT-034 | Agenda do dia exibe os agendamentos e permite concluir atendimento | Média | Tela | RF-08 | EX-___ | | | |
| ☐ | 34 | CT-035 | Concluir agendamento cancelado é recusado | Média | API | RF-08 | EX-___ | | | |
| ☐ | 35 | CT-032 | Barbeiro desativado deixa de aparecer para o cliente | Baixa | Tela | RF-07 | EX-___ | | | |

Resultado: Aprovado, Reprovado, Bloqueado ou Não executado. Evidência: `EX-NNN_CT-NNN_AAAA-MM-DD.png` (tela) ou `.txt` (resposta da API).
