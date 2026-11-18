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
java -jar target/barberagenda-1.1.0.jar                       # a partir do pacote gerado
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
| Unitários (JUnit 5 + Mockito) | `./mvnw test` | A implementar no Marco 5 |
| Cobertura (JaCoCo) | `./mvnw verify` → `target/site/jacoco/index.html` | A configurar no Marco 5 |
| Análise de qualidade (SonarQube) | A documentar no Marco 5 | A configurar |
| Integração/API (Postman + Newman) | A documentar no Marco 6 (`postman/`) | A implementar |
| Sistema/interface (Selenium) | A documentar no Marco 6 | A implementar |
| Gerar catálogo de casos (P04) e matriz de rastreabilidade (P05) | `python scripts/gerar_artefatos.py` (requer `pip install openpyxl`; com LibreOffice instalado, a planilha já sai com os valores calculados) | Disponível |

> A verificação rápida apenas confirma que as funções selecionadas estão disponíveis (seção 9.1 do manual). Ela não substitui os casos de teste formais nem a automação.

## 11. Acesso ao pipeline

GitHub Actions: https://github.com/ZangrandeG/barberagenda/actions (pipeline a configurar no Marco 9).

## 12. Localização dos documentos

| Local | Conteúdo |
|---|---|
| `entrega/` | Espelho das 17 pastas obrigatórias do Drive (seção 11.3 do manual) |
| `entrega/00_IDENTIFICACAO_E_README/` | Ficha de proposta do sistema (P01) |
| `entrega/01_SISTEMA_ALVO/` | Ambiente e verificação da versão base |
| `entrega/02_REQUISITOS_ESCOPO_RISCOS/` | Requisitos, escopo e riscos (P02) |
| `entrega/03_PLANO_DE_TESTES/` | Plano de testes (P03) e documento do Marco 1 (níveis, tipos e estratégia) |
| `entrega/04_CASOS_E_RASTREABILIDADE/` | Catálogo de casos de teste (P04) e matriz de rastreabilidade em XLSX (P05) |
| `dados/` | Fonte única de requisitos, riscos, casos (JSON), execuções e defeitos (CSV) usada para gerar P04 e P05 |
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
