# BarberAgenda — Projeto Integrado P2 (Testes e Qualidade de Software)

Sistema web de agendamento para uma barbearia **fictícia**, usado como objeto de teste do Projeto Integrado P2 da disciplina Testes e Qualidade de Software (UNISAGRADO — Ciência da Computação — 2026, Prof. Dr. Elvio Gilberto da Silva).

> As seções abaixo seguem a ordem exigida na seção 11.4 do manual do projeto.

## 1. Integrantes

| Nome | RA | GitHub |
|---|---|---|
| Guilherme Ribeiro Zangrande | 23110757 | `ZangrandeG` |
| José Paulo Dassie Felippi | 24111563 | `zepadf` |

Turma A — Grupo [PREENCHER número do grupo]

## 2. Nome e versão do sistema

**BarberAgenda 1.1.0** — tag Git `v1.1.0-sistema-base` (versão que será testada).

| Versão | Tag | Data | Mudança |
|---|---|---|---|
| 1.0.0 | `v1.0-sistema-base` | 2026-11-18 | Versão base |
| 1.0.1 | `v1.0.1-sistema-base` | 2026-11-18 | A restauração de dados (`POST /api/dev/reset`) passa a exigir administrador e CSRF, apontado pela revisão de segurança do código antes do início dos testes |
| 1.1.0 | `v1.1.0-sistema-base` | 2026-11-18 | Consulta e cancelamento pelo cliente passam a exigir um código de acesso aleatório (em vez do id sequencial) + e-mail, também apontado pela revisão de segurança |

## 3. Link do repositório

https://github.com/ZangrandeG/barberagenda

## 4. Tecnologias

| Camada | Tecnologia |
|---|---|
| Linguagem | Java 21 |
| Framework | Spring Boot 3.5.16 (Web, Data JPA, Validation, Security) |
| Build | Maven 3.10.1 via Maven Wrapper (`mvnw` / `mvnw.cmd`) |
| Banco de dados | H2 2.3 (arquivo no perfil `dev`, memória no perfil `test`); PostgreSQL 16 opcional (perfil `postgres`) |
| Interface | HTML, CSS e JavaScript puro em `src/main/resources/static`, consumindo a API REST com `fetch` |
| Testes (planejado) | JUnit 5, AssertJ, Mockito, MockMvc, Postman/Newman, Selenium WebDriver, JaCoCo, SonarQube |
| Gestão | GitHub Issues (defeitos) e GitHub Actions (CI/CD) |

Arquitetura em camadas: `controller` (API REST) → `service` (regras de negócio) → `repository` (Spring Data JPA) → banco. Detalhes em [docs/ESPECIFICACAO_SISTEMA.md](docs/ESPECIFICACAO_SISTEMA.md).

## 5. Pré-requisitos

- **JDK 21** (ex.: Eclipse Temurin 21). Não é preciso instalar o Maven: o wrapper baixa a versão correta na primeira execução.
- Git.
- Navegador atualizado (Chrome recomendado; necessário para os testes Selenium).
- Opcionais, conforme a etapa de testes: Node.js + Newman (testes de API), Python 3 (planilhas e métricas), Docker (PostgreSQL e SonarQube local).

Versões exatas usadas pelo grupo: [entrega/01_SISTEMA_ALVO/ambiente.md](entrega/01_SISTEMA_ALVO/ambiente.md) (gerado por `scripts/registrar-ambiente.ps1`).

## 6. Instalação

```bash
git clone https://github.com/ZangrandeG/barberagenda.git
cd barberagenda
./mvnw -DskipTests package        # Windows (PowerShell/CMD): .\mvnw.cmd -DskipTests package
```

Se houver mais de um Java instalado, aponte a variável `JAVA_HOME` para o JDK 21 antes de rodar o wrapper. Exemplo no PowerShell:

```powershell
$env:JAVA_HOME = 'C:\Program Files\Eclipse Adoptium\jdk-21.0.13.9-hotspot'
```

## 7. Configuração

| Perfil Spring | Uso | Banco |
|---|---|---|
| `dev` (padrão) | Desenvolvimento e testes manuais | H2 em arquivo (`./data/barberagenda.mv.db`), dados preservados entre reinícios |
| `test` | Testes automatizados e pipeline | H2 em memória, recriado a cada inicialização |
| `postgres` (opcional) | PostgreSQL local; combine com `dev` para carregar a massa fictícia | Variáveis `DB_URL`, `DB_USUARIO`, `DB_SENHA` |

Variáveis de ambiente opcionais:

| Variável | Padrão | Finalidade |
|---|---|---|
| `PORTA` | `8080` | Porta HTTP |
| `ADMIN_LOGIN` / `ADMIN_SENHA` | `admin` / `admin123` | Administrador criado na primeira inicialização (valores padrão fictícios) |

## 8. Banco e dados

- O esquema é criado automaticamente pelo Hibernate.
- Nos perfis `dev` e `test`, uma **massa de dados fictícios** é carregada quando o banco está vazio: 3 barbeiros (1 inativo), 5 serviços (1 inativo), 10 clientes e 5 agendamentos com datas relativas ao dia atual. Detalhes na seção 6 de [docs/ESPECIFICACAO_SISTEMA.md](docs/ESPECIFICACAO_SISTEMA.md).
- **Restaurar o ambiente entre execuções** (apaga os dados e recarrega a massa; disponível somente em `dev` e `test` e somente para o administrador — os scripts usam a credencial fictícia ou as variáveis `ADMIN_LOGIN`/`ADMIN_SENHA`):

```bash
bash scripts/reset-dados.sh                                         # Linux/macOS/Git Bash
powershell -ExecutionPolicy Bypass -File scripts\reset-dados.ps1    # Windows
```

- Para começar do zero no perfil `dev`, também é possível parar a aplicação e apagar a pasta `data/`.
- Todos os dados são fictícios (nomes inventados, e-mails `@exemplo.com`).

## 9. Execução

```bash
./mvnw spring-boot:run                                        # perfil dev
./mvnw spring-boot:run -Dspring-boot.run.profiles=test        # perfil test (banco em memória)
java -jar target/barberagenda-1.2.0.jar                       # a partir do pacote gerado
```

Acesse:

| Página | Endereço |
|---|---|
| Início | http://localhost:8080 |
| Cadastro de cliente | http://localhost:8080/cadastro.html |
| Agendamento | http://localhost:8080/agendar.html |
| Consulta e cancelamento | http://localhost:8080/consulta.html |
| Área administrativa | http://localhost:8080/admin/ |

PostgreSQL opcional (exige Docker): `docker compose up -d` e depois `./mvnw spring-boot:run -Dspring-boot.run.profiles=dev,postgres`.

## 10. Execução dos testes

| Tipo | Comando | Situação |
|---|---|---|
| Verificação rápida da versão base | Com a aplicação rodando: `bash scripts/verificar-sistema.sh` | Disponível — 46 verificações; resultados em [entrega/01_SISTEMA_ALVO](entrega/01_SISTEMA_ALVO) |
| Unitários (JUnit 5 + Mockito + AssertJ) | `./mvnw test` | Disponível — 35 métodos, 52 execuções, 0 falhas ([P08](entrega/07_AUTOMACAO_UNITARIA/P08_Testes_Unitarios.md)) |
| Cobertura (JaCoCo 0.8.16) | `./mvnw test` → `target/site/jacoco/index.html` | Disponível — 36,4% das linhas (serviços: 76,8%) |
| Análise de qualidade (SonarQube) | Ver "SonarQube local" abaixo; `./mvnw verify sonar:sonar -Dsonar.host.url=http://localhost:9000` com a variável `SONAR_TOKEN` | Linha de base em [entrega/11_METRICAS_E_QUALIDADE/sonar_baseline](entrega/11_METRICAS_E_QUALIDADE/sonar_baseline) |
| Integração/API (Postman + Newman) | Com a aplicação no ar (perfil `test`): `newman run postman/BarberAgenda.postman_collection.json -e postman/BarberAgenda.postman_environment.json --reporters cli,junit,htmlextra` | Disponível — 26 requisições, 63 asserções, 0 falhas ([P08 API](entrega/08_INTEGRACAO_API/P08_Testes_Integracao_API.md)) |
| Sistema/interface (Selenium) | `./mvnw test -Pe2e` (opções `-Dnavegador=chrome\|firefox`, `-Djanela=375x667`, `-Dheadless=false`) | Disponível — 5 testes, 0 falhas ([P08 interface](entrega/09_SISTEMA_INTERFACE/P08_Testes_Sistema_Interface.md)) |
| Não funcionais (P09) | Aplicação no ar (perfil `test`): `python scripts/nf/desempenho.py <pasta>`, `python scripts/nf/seguranca_robustez.py <pasta>`; com o pacote gerado: `python scripts/nf/reinicio_e_senha.py <pasta>`; compatibilidade: `./mvnw test -Pe2e -Dnavegador=firefox -Djanela=375x667` | Disponível — 7 de 8 executados e aprovados ([P09](entrega/10_ACEITACAO_NAO_FUNCIONAIS/P09_Aceitacao_e_Nao_Funcionais.md)) |
| Aceitação (P09) | Roteiro com 4 cenários para pessoa externa | Preparado — execução pendente |
| Gerar catálogo (P04), matriz (P05), checklist e registro de execução (P06) | `python scripts/gerar_artefatos.py` (requer `pip install openpyxl`; com LibreOffice instalado, a planilha já sai com os valores calculados) | Disponível |
| Execução manual (P06) | Roteiro em `entrega/05_EXECUCAO_MANUAL/P06_Roteiro_Execucao.md`; datas e ids do dia: `python scripts/datas_teste.py` | Executado — 35/35 aprovados; execução assistida: `python scripts/execucao_assistida.py` (aplicação no ar) |
| Exportar defeitos do GitHub Issues (P07) | `python scripts/exportar_defeitos.py` (requer `gh auth login`) | Disponível |

**SonarQube local (sem Docker).** O grupo usa a distribuição oficial em zip do SonarQube Community Build 26.11 (https://binaries.sonarsource.com/Distribution/sonarqube/), que roda com o próprio Java 21:

1. Descompactar em uma pasta fora do projeto (ex.: `C:\Users\<usuario>\Ferramentas\sonarqube-26.11.0.134175`).
2. O Elasticsearch embutido exige **10% do disco livre**; se o disco tiver menos, apontar os dados para outro disco em `conf/sonar.properties` (`sonar.path.data` e `sonar.path.temp`).
3. Subir: `java -jar lib/sonar-application-26.11.0.134175.jar` (ou `bin\windows-x86-64\StartSonar.bat`) e abrir http://localhost:9000.
4. No primeiro acesso, trocar a senha padrão do `admin` e gerar um token de análise (My Account → Security). Guardar senha e token **fora do repositório**.
5. Analisar: `SONAR_TOKEN=<token> ./mvnw verify sonar:sonar -Dsonar.host.url=http://localhost:9000`.
6. Exportar o resultado: `SONAR_TOKEN=<token de usuário> python scripts/sonar_relatorio.py <pasta>`.

> A verificação rápida apenas confirma que as funções selecionadas estão disponíveis (seção 9.1 do manual). Ela não substitui os casos de teste formais nem a automação.

## 11. Acesso ao pipeline

GitHub Actions: https://github.com/ZangrandeG/barberagenda/actions — workflow `.github/workflows/ci.yml` (gatilhos: `push`, `pull_request` para `main` e manual).

| Job | O que faz |
|---|---|
| Unidade + integração + cobertura | `./mvnw -B verify` (58 testes) e JaCoCo |
| Integração/API | Sobe a aplicação no perfil `test` e roda a coleção no Newman |
| Sistema/interface | `./mvnw test -Pe2e` no Chrome headless |

Relatórios (Surefire, JaCoCo, Newman, capturas do Selenium) ficam nos artefatos de cada execução. Execuções documentadas (verde, falha proposital e correção) no [P11](entrega/12_TDD_CICD_MELHORIA/P11_TDD_CICD_Melhoria.md).

## 12. Localização dos documentos

| Local | Conteúdo |
|---|---|
| `entrega/` | Espelho das 17 pastas obrigatórias do Drive (seção 11.3 do manual) |
| `entrega/00_IDENTIFICACAO_E_README/` | Ficha de proposta do sistema (P01) |
| `entrega/01_SISTEMA_ALVO/` | Ambiente e verificação da versão base |
| `entrega/02_REQUISITOS_ESCOPO_RISCOS/` | Requisitos, escopo e riscos (P02) |
| `entrega/03_PLANO_DE_TESTES/` | Plano de testes (P03) e documento do Marco 1 (níveis, tipos e estratégia) |
| `entrega/04_CASOS_E_RASTREABILIDADE/` | Catálogo de casos de teste (P04) e matriz de rastreabilidade em XLSX (P05) |
| `entrega/05_EXECUCAO_MANUAL/` | Roteiro, checklist, registro de execução (P06) e `evidencias/` |
| `entrega/06_DEFEITOS/` | Exportação dos defeitos do GitHub Issues (P07) |
| `entrega/07_AUTOMACAO_UNITARIA/` | Testes de unidade (P08): documento, log, relatórios Surefire e JaCoCo |
| `entrega/08_INTEGRACAO_API/` | Testes de API (P08): coleção e ambiente do Postman exportados, relatórios do Newman |
| `entrega/10_ACEITACAO_NAO_FUNCIONAIS/` | Aceitação e não funcionais (P09): cenários, registros do Apêndice I, roteiro de usabilidade e evidências |
| `entrega/09_SISTEMA_INTERFACE/` | Testes Selenium (P08): documento, log, relatórios e capturas |
| `postman/` | Coleção e ambiente usados na execução (gerados por `scripts/gerar_colecao_postman.py`) |
| `entrega/11_METRICAS_E_QUALIDADE/sonar_baseline/` | Linha de base do SonarQube (medidas, problemas, quality gate, log) |
| `dados/` | Fonte única de requisitos, riscos, casos (JSON), execuções e defeitos (CSV) usada para gerar P04, P05 e P06 |
| `entrega/15_DIARIO_DE_PARTICIPACAO/` | Diário de participação (P14) |
| `docs/PROGRESSO.md` | Situação de cada fase e produto |
| `docs/ESPECIFICACAO_SISTEMA.md` | Regras de negócio, API, códigos de resposta e decisões de projeto |
| `scripts/` | Verificação, restauração de dados, registro do ambiente e geração do P04/P05 |

## 13. Credenciais fictícias

| Uso | Usuário | Senha |
|---|---|---|
| Administrador (perfis `dev` e `test`) | `admin` | `admin123` |
| Banco H2 local | `sa` | (vazia) |
| PostgreSQL do `docker-compose.yml` | `barberagenda` | `barberagenda` |

**Todas as credenciais acima são fictícias**, servem apenas para ambiente local de desenvolvimento e testes e não dão acesso a nenhum sistema real.

## 14. Problemas conhecidos

| Problema | Solução |
|---|---|
| Com mais de um Java instalado, o wrapper pode usar uma versão antiga e falhar na compilação. | Definir `JAVA_HOME` apontando para o JDK 21 (seção 6). |
| No Windows, o `curl` executado pelo Git Bash corrompe acentos passados diretamente em `--data`, e a API responde 400 ("Corpo da requisição ausente ou em formato inválido"). | Enviar o corpo por arquivo (`--data-binary @arquivo.json`), como faz `scripts/verificar-sistema.sh`. |
| O perfil `postgres` ainda não foi executado pelo grupo (Docker não instalado na máquina de desenvolvimento). | Usar o H2 (perfis `dev`/`test`), que atende a todo o escopo do projeto. |
| O cliente não tem login: o código de acesso e o e-mail funcionam como credencial do agendamento. Não há limite de tentativas na consulta. | Limitação aceita no escopo acadêmico. O código tem 8 caracteres aleatórios (~31^8 combinações), o que torna inviável adivinhá-lo. |
| Ao atualizar uma cópia local da versão 1.0.x para a 1.1.0, o banco do perfil `dev` (pasta `data/`) não tem a nova coluna de código de acesso. | Parar a aplicação e apagar a pasta `data/`; a massa fictícia é recriada na próxima inicialização. |

## 15. Contato do grupo

- Issues do repositório: https://github.com/ZangrandeG/barberagenda/issues
- E-mails institucionais: [PREENCHER PELO GRUPO]
