# P13 — Roteiro da apresentação, da demonstração e do vídeo de contingência

**BarberAgenda 1.2.0** — tempo total: 12 a 15 minutos + até 5 minutos de perguntas. Todos os integrantes falam (manual, seção 13.2).

## 1. Divisão da fala (slides em `P13_Apresentacao.pptx`; notas do apresentador em cada slide)

| Slide | Conteúdo (seção 13.1 do manual) | Quem fala | Tempo |
|---|---|---|---|
| 1–3 | Abertura, o sistema e como foi construído | Guilherme | 2 min |
| 4–5 | Riscos e estratégia de teste (pirâmide) | José Paulo | 2 min |
| 6 | Casos de teste, execução e defeitos | José Paulo | 2 min |
| 7 | Automação + **demonstração 1** | Guilherme | 3 min |
| 8–9 | Não funcionais e métricas | José Paulo | 2 min |
| 10–11 | TDD e pipeline CI/CD + **demonstração 2** | Guilherme | 2 min |
| 12–13 | Qualidade do código (SonarQube) e conclusão | José Paulo | 1–2 min |

Os slides têm pouco texto de propósito: o que falar está nas **notas do apresentador** de cada slide. O texto completo de cada fala, as demonstrações e as perguntas prováveis estão em **`P13_Roteiro_de_Fala.md`** (e no PDF de mesmo nome, para imprimir).

## 2. Preparação (antes da aula)

1. `git pull`, `./mvnw -DskipTests package` e `npm install -g newman` (se ainda não instalado).
2. Abrir **dois terminais** na pasta do projeto e o navegador com as abas: README no GitHub, GitHub Actions (runs 44441467718, 44441895872, 44442093641), `P05_Matriz_Rastreabilidade.xlsx`, `P04` (CT-012) e uma evidência (`entrega/05_EXECUCAO_MANUAL/evidencias/EX-012_CT-012_2026-11-18.txt`).
3. Terminal 1: `java -jar target/barberagenda-1.2.0.jar --spring.profiles.active=test` (deixar rodando).
4. Testar o roteiro inteiro uma vez e conferir que o vídeo de contingência abre no computador da sala.

## 3. Demonstração 1 — automação (slide 7)

```bash
./mvnw test                                   # 58 testes de unidade e integração, ~30 s
newman run postman/BarberAgenda.postman_collection.json -e postman/BarberAgenda.postman_environment.json
```

Mostrar: "Tests run: 58, Failures: 0" e a tabela final do Newman (26 requisições, 63 asserções, 0 falhas). Se houver tempo: `./mvnw test -Pe2e -Dtest=AgendamentoE2ETest -Dheadless=false` para o navegador abrir e agendar sozinho.

## 4. Demonstração 2 — TDD e pipeline (slides 10–11)

```bash
git log --oneline 35ce2a2 -1    # RED
git log --oneline c9c6e4c -1    # GREEN
git log --oneline 78b44e3 -1    # REFACTOR
```

Abrir `entrega/12_TDD_CICD_MELHORIA/tdd/01_RED_mvnw_test.log` (falha "Status expected:<422> but was:<200>") e as três runs no GitHub Actions (verde → falha proposital → correção).

## 5. Plano B (falha de rede, de equipamento ou de execução)

| Problema | O que fazer |
|---|---|
| Sem internet (GitHub fora) | Usar o PDF da apresentação e os arquivos locais: logs em `entrega/12_TDD_CICD_MELHORIA/` e `cicd/execucoes_pipeline.md` |
| Aplicação não sobe | Mostrar `entrega/01_SISTEMA_ALVO/verificacao_*.txt` e as capturas em `entrega/09_SISTEMA_INTERFACE/capturas/` |
| Teste demora ou trava | Mostrar o relatório já gerado: `entrega/07_AUTOMACAO_UNITARIA/surefire/` e `entrega/08_INTEGRACAO_API/relatorios/newman_2026-11-18.html` |
| Computador da sala não funciona | Reproduzir o vídeo de contingência (seção 6) do pendrive ou do link |

## 6. Roteiro do vídeo de contingência (gravar até 5 minutos, MP4)

Gravar a tela (ex.: Xbox Game Bar `Win + Alt + R` ou OBS) com narração dos dois integrantes:

1. (0:00–0:30) Apresentação do grupo e do sistema (tela inicial do BarberAgenda).
2. (0:30–1:30) Agendamento pela tela: cadastro, escolha de horário e código de acesso; consulta e cancelamento.
3. (1:30–2:30) `./mvnw test` e Newman rodando até o fim, com os totais na tela.
4. (2:30–3:30) Teste Selenium com o navegador visível (`-Dheadless=false`).
5. (3:30–4:30) GitHub Actions: run verde, falha proposital e correção; commits do TDD.
6. (4:30–5:00) Planilha P05 (aba Métricas) e conclusão.

Salvar como `P13_Video_Contingencia.mp4` nesta pasta (ou link acessível sem pedir permissão). **[PREENCHER PELO GRUPO — gravação do vídeo]**
