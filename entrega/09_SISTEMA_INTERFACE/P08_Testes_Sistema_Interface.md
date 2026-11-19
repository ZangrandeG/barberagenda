# P08 — Testes de sistema/interface (Selenium) — Marco 6

**Projeto Integrado P2 — BarberAgenda 1.1.0** — Turma A — Guilherme Ribeiro Zangrande e José Paulo Dassie Felippi

| Versão | Data | Descrição |
|---|---|---|
| v1.0 | 2026-11-18 | 5 testes ponta a ponta em 4 fluxos, Chrome headless 1366×768 |

## 1. Abordagem

- **Fluxos ponta a ponta reais**: cada teste sobe a aplicação inteira (`@SpringBootTest`, perfil `test`, porta aleatória), restaura a massa fictícia e abre um navegador novo — os testes são independentes.
- **Verificações de resultado**, não só cliques: mensagens, códigos, status, conteúdo de tabelas e horários oferecidos.
- **Padrão Page Object** (`e2e/pages`): `PaginaCadastro`, `PaginaAgendamento`, `PaginaConsulta`, `PaginaAdmin`; localização estável por `id`/`data-testid`.
- **Esperas explícitas** (`WebDriverWait` + `ExpectedConditions`); nenhum `Thread.sleep`.
- **Captura de tela automática** ao final de cada teste (`EvidenciaE2EExtension`), feita antes de fechar o navegador; o sufixo `_FALHA` identifica a tela no momento de uma falha.
- **Separados dos testes de unidade** pela tag `@Tag("e2e")` e pelo perfil Maven `e2e`.
- Selenium 4.53.0; o ChromeDriver é obtido automaticamente pelo Selenium Manager.

## 2. Como executar

```bash
./mvnw test -Pe2e                                     # Chrome headless, 1366x768
./mvnw test -Pe2e -Dnavegador=firefox                 # Firefox (Marco 7, compatibilidade)
./mvnw test -Pe2e -Djanela=375x667                    # resolução de celular
./mvnw test -Pe2e -Dheadless=false                    # ver o navegador abrindo
```

Capturas em `target/selenium-evidencias/`.

## 3. Resultado da execução (2026-11-18)

Comando `./mvnw -B test -Pe2e`, Chrome 157 headless, janela 1366×768, versão 1.1.0:

| Classe | Teste | Caso / requisito | Resultado |
|---|---|---|---|
| CadastroClienteE2ETest | `deveCadastrarClientePelaTela` | CT-001 / RF-01 | Aprovado |
| CadastroClienteE2ETest | `deveRecusarNomeCurtoPelaTela` | CT-003 / RF-01 | Aprovado |
| AgendamentoE2ETest | `deveAgendarHorarioPelaTela` | CT-010 / RF-03 | Aprovado |
| CancelamentoE2ETest | `deveConsultarECancelarAgendamentoLiberandoOHorario` | CT-023 + CT-025 / RF-05 | Aprovado |
| AdminServicoE2ETest | `deveEntrarCadastrarServicoESair` | CT-027 + CT-030 / RF-06, RF-07 | Aprovado |

**Total: 5 testes, 0 falhas, 0 erros.** Evidências: `execucao_mvnw_test_e2e_2026-11-18.log`, `surefire/` e `capturas/` (uma por teste).

## 4. O que cada teste verifica

| Teste | Verificações |
|---|---|
| Cadastro válido | Mensagem "Cadastro realizado com sucesso! Código do cliente: N." e botão "Agendar um horário" visível |
| Nome com 2 caracteres | Erro no campo Nome, mensagem "Existem campos inválidos." e nenhum atalho para agendar |
| Agendamento completo | Lista de horários de 09:00 a 18:30 contendo 11:00; após confirmar: código de acesso no formato correto, barbeiro, serviço, data/hora e status AGENDADO no resumo |
| Consulta e cancelamento | Consulta com código em minúsculas; status AGENDADO → CANCELADO; botão de cancelar oculto; o horário 16:00 volta a ser oferecido na tela de agendamento |
| Administração | `/admin/` sem login redireciona ao login; após login, "Usuário: admin"; cadastro de serviço no limite mínimo (15 min, R$ 1,00) aparece na tabela; "Sair" volta ao login com a mensagem de saída |
