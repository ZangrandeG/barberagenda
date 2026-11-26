# P01 — Ficha de Proposta e Aprovação do Sistema (Apêndice A)

**Projeto Integrado P2 — Testes e Qualidade de Software**
UNISAGRADO — Ciência da Computação — 2026
Professor: Prof. Dr. Elvio Gilberto da Silva

| Versão | Data | Descrição | Autor |
|---|---|---|---|
| v1.0 | 2026-11-18 | Primeira versão da ficha, com duas opções de sistema para aprovação | Guilherme Ribeiro Zangrande; José Paulo Dassie Felippi |
| v1.1 | 2026-11-18 | Opção 1: sistema base implementado e verificado (tag `v1.0-sistema-base`) | Guilherme Ribeiro Zangrande; José Paulo Dassie Felippi |
| v1.2 | 2026-11-18 | Opção 1: consulta/cancelamento por código de acesso aleatório + e-mail (versão 1.1.0, tag `v1.1.0-sistema-base`) | Guilherme Ribeiro Zangrande; José Paulo Dassie Felippi |
| v1.3 | 2026-11-25 | Registro da decisão do professor: Opção 1 (BarberAgenda) aprovada em 2026-11-19 | Guilherme Ribeiro Zangrande; José Paulo Dassie Felippi |

> Conforme a seção 5.5 do manual, o grupo apresenta **duas opções** de sistema. A documentação definitiva (P02 em diante) só será iniciada após a decisão do professor.
>
> **Opção preferencial do grupo:** Opção 1 — BarberAgenda.
>
> **Decisão:** o professor aprovou a Opção 1 (BarberAgenda) em 2026-11-19.

---

## Opção 1 — BarberAgenda (Sistema de Agendamento de Barbearia)

| Campo | Preenchimento do grupo |
|---|---|
| **Turma e grupo** | Turma A — Grupo Guilherme e José Paulo |
| **Integrantes** | Guilherme Ribeiro Zangrande (RA 23110757); José Paulo Dassie Felippi (RA 24111563) |
| **Nome do sistema** | BarberAgenda — Sistema de Agendamento de Barbearia (versão prevista para teste: 1.0) |
| **Origem do sistema** | Sistema acadêmico desenvolvido pelo próprio grupo para esta disciplina (seção 5.2, segundo item). A construção é feita com apoio de ferramenta de inteligência artificial generativa (Claude Code), uso declarado conforme a seção 15 e sujeito às orientações do professor. **Situação atual:** versão base implementada e executável desde 2026-11-18 (versão atual 1.1.0, tag `v1.1.0-sistema-base`); funcionamento verificado conforme `entrega/01_SISTEMA_ALVO/verificacao_v1.1.0_2026-11-18.txt`. |
| **Link do repositório** | https://github.com/ZangrandeG/barberagenda (atualmente privado; acesso do professor a definir) |
| **Licença/autorização** | Código próprio do grupo; licença proposta: MIT [CONFIRMAR PELO GRUPO]. Dependências de código aberto com licenças que permitem uso acadêmico (Spring Boot — Apache 2.0; Selenium — Apache 2.0; JUnit 5 — EPL 2.0; H2 — MPL 2.0/EPL 1.0). Somente dados fictícios. |
| **Tecnologias principais** | Java 21; Spring Boot 3 (Web, Data JPA, Validation, Security); Maven Wrapper; banco H2 (arquivo em desenvolvimento, memória em testes), PostgreSQL opcional via Docker; front-end em HTML, CSS e JavaScript puro consumindo a API REST. Testes: JUnit 5, AssertJ, Mockito, MockMvc, Postman/Newman, Selenium WebDriver, JaCoCo, SonarQube. Gestão: GitHub Issues e GitHub Actions. |
| **Como executar** | Pré-requisito: JDK 21. Comando: `./mvnw spring-boot:run` (no Windows, `mvnw.cmd spring-boot:run`). Acesso: `http://localhost:8080`. Área administrativa em `/admin` com credencial fictícia `admin` / `admin123`. Testes: `./mvnw test`. |
| **Fluxos selecionados** | 1. Cadastro de cliente (**formulário**). 2. Criação de agendamento: escolha de barbeiro, serviço, data e horário disponível (**formulário**). 3. Consulta e cancelamento de agendamento pelo cliente (código de acesso recebido ao agendar + e-mail). 4. Login do administrador. 5. Cadastro, edição e exclusão de barbeiros e serviços (**formulários**, área administrativa). 6. Agenda do dia por barbeiro, com marcação de atendimento concluído. |
| **Integrações existentes** | Interface web (JavaScript) ↔ API REST (HTTP/JSON); camada de controle ↔ camada de serviço (regras de negócio) ↔ repositórios Spring Data JPA ↔ banco H2; Spring Security ↔ área administrativa; repositório GitHub ↔ pipeline GitHub Actions. |
| **Justificativa da escolha** | (a) Domínio simples e conhecido, fácil de explicar e de avaliar do ponto de vista do usuário (cliente e dono da barbearia), o que favorece os testes de aceitação. (b) Regras de negócio com intervalos, tamanhos, quantidades e datas — tamanho do nome, quantidade de dígitos do telefone, horário de funcionamento, intervalos de 30 minutos, antecedência máxima de 30 dias, limite de agendamentos ativos, duração e preço de serviços —, adequadas ao particionamento de equivalência e à análise de valor limite. (c) API REST própria, que permite testes de integração com Postman/Newman, incluindo encadeamento de dados. (d) Interface web com fluxos ponta a ponta para Selenium. (e) Código-fonte completo sob controle do grupo, viabilizando testes unitários, TDD, análise com SonarQube e CI/CD. (f) Banco H2 sem instalação, o que facilita a execução no laboratório. (g) Tamanho compatível com o período da disciplina. |
| **Riscos de viabilidade** | 1. Sistema construído pelo próprio grupo no início do projeto: mudanças de escopo pedidas pelo professor exigem ajuste de código — mitigação: escopo fechado nesta ficha e versão base já disponível. 2. Regras que dependem de data e hora podem gerar testes instáveis — mitigação: relógio (`Clock`) injetável e dados com datas relativas. 3. Ambiente: SonarQube local exige Docker caso o repositório seja privado. 4. Sistema recém-construído pode apresentar poucos defeitos — serão registrados apenas os defeitos reais (seção 9.7). 5. A política do professor sobre uso de IA pode restringir esta opção — nesse caso, a Opção 2 é a alternativa. |
| **Decisão do professor** | (X) Aprovado  ( ) Aprovado com ajustes  ( ) Não aprovado |
| **Ajustes solicitados** | Nenhum |
| **Data da aprovação** | 2026-11-19 |

### Escopo funcional previsto (resumo das regras de negócio)

| ID | Regra |
|---|---|
| RN-01 | Nome do cliente obrigatório, de 3 a 60 caracteres. |
| RN-02 | Telefone somente com dígitos, 10 ou 11 dígitos (com DDD). |
| RN-03 | E-mail em formato válido e único entre clientes. |
| RN-04 | Funcionamento de segunda a sábado, das 09:00 às 19:00; o serviço precisa terminar até 19:00. Domingo fechado. |
| RN-05 | Agendamentos iniciam em intervalos de 30 minutos. |
| RN-06 | Não é permitido agendar no passado; antecedência máxima de 30 dias. |
| RN-07 | Um barbeiro não pode ter dois agendamentos ativos com horários sobrepostos. |
| RN-08 | Um cliente pode ter no máximo 3 agendamentos ativos ao mesmo tempo. |
| RN-09 | Serviço com duração de 15 a 180 minutos (múltiplo de 15) e preço de R$ 1,00 a R$ 1.000,00. |
| RN-10 | Somente barbeiros e serviços ativos recebem agendamentos. |
| RN-11 | Área administrativa acessível somente com autenticação; a API administrativa retorna 401/403 sem credenciais. |

> A evolução que será feita por TDD (seção 9.14) **não** faz parte da versão base: regra de antecedência mínima para cancelamento, a ser implementada pelo ciclo Red-Green-Refactor.

---

## Opção 2 — Spring PetClinic

| Campo | Preenchimento do grupo |
|---|---|
| **Turma e grupo** | Turma A — Grupo Guilherme e José Paulo |
| **Integrantes** | Guilherme Ribeiro Zangrande (RA 23110757); José Paulo Dassie Felippi (RA 24111563) |
| **Nome do sistema** | Spring PetClinic — aplicação de exemplo do ecossistema Spring para gestão de uma clínica veterinária (versão: commit a ser fixado no fork do grupo — [PREENCHER hash do commit]) |
| **Origem do sistema** | Projeto de código aberto (seção 5.2, terceiro item), utilizado somente em ambiente local e de testes, por meio de fork no GitHub do grupo. |
| **Link do repositório** | Original: https://github.com/spring-projects/spring-petclinic — Fork do grupo: [PREENCHER] |
| **Licença/autorização** | Apache License 2.0 (arquivo `LICENSE.txt` do repositório), que permite estudo, modificação e redistribuição, mantidos os avisos de autoria. |
| **Tecnologias principais** | Java 17 ou superior; Spring Boot 4.1 (conforme `pom.xml` consultado em 2026-11-18); Spring MVC com Thymeleaf (páginas geradas no servidor); Spring Data JPA; Bean Validation; H2 em memória por padrão, com perfis para MySQL e PostgreSQL; Maven Wrapper e Gradle Wrapper. |
| **Como executar** | `./mvnw spring-boot:run` e acesso em `http://localhost:8080/` (instruções do README oficial). |
| **Fluxos selecionados** | 1. Busca de proprietários por sobrenome. 2. Cadastro de proprietário (**formulário**). 3. Edição de proprietário (**formulário**). 4. Cadastro de pet vinculado a proprietário (**formulário**). 5. Registro de visita ao veterinário (**formulário**). 6. Listagem de veterinários e especialidades. |
| **Integrações existentes** | Navegador ↔ controladores Spring MVC/Thymeleaf ↔ repositórios Spring Data JPA ↔ banco H2 (ou MySQL/PostgreSQL por perfil). |
| **Justificativa da escolha** | Projeto maduro, documentado e de instalação simples; código Java (JUnit aplicável); formulários com validações (por exemplo, telefone com exatamente 10 dígitos e campos obrigatórios); licença compatível com uso acadêmico e modificação. |
| **Riscos de viabilidade** | 1. Não possui API REST no repositório principal; os testes com Postman ficariam restritos a requisições HTTP de formulário, reduzindo o valor dos testes de integração/API. 2. Poucas regras numéricas, o que limita a aplicação de valor limite. 3. O projeto já contém testes dos autores; os testes do grupo precisariam ser separados e identificados (seção 15). 4. Projeto muito conhecido: risco de semelhança com trabalhos de outros grupos. 5. Banco em memória por padrão: os dados se perdem ao reiniciar, exigindo perfil persistente para o teste de confiabilidade. |
| **Decisão do professor** | Não se aplica — a Opção 1 foi aprovada |
| **Ajustes solicitados** | — |
| **Data da aprovação** | — |

---

## Verificação dos requisitos mínimos (seção 5.3)

| Requisito mínimo | Opção 1 — BarberAgenda | Opção 2 — PetClinic |
|---|---|---|
| Código-fonte disponível para instalação, execução, automação, TDD e análise de qualidade | Sim (código do grupo) | Sim (fork, Apache 2.0) |
| Execução em ambiente local ou de testes, sem produção | Sim (local, H2) | Sim (local, H2) |
| No mínimo 4 fluxos funcionais, com ao menos 2 formulários | Sim (6 fluxos, 3 com formulário) | Sim (6 fluxos, 4 com formulário) |
| Persistência de dados | Sim (H2 via JPA) | Sim (H2 via JPA) |
| Ao menos uma integração entre componentes | Sim (interface ↔ API ↔ serviço ↔ banco) | Sim (interface ↔ controlador ↔ banco) |
| Dados fictícios e repetição dos testes sem afetar usuários reais | Sim (massa fictícia e rotina de restauração) | Sim (massa de exemplo carregada na inicialização) |
| Disponível ao grupo durante todo o semestre | Sim (repositório do grupo) | Sim (fork do grupo) |
| Instruções de instalação | A produzir no README (seção 11.4) | README oficial, a complementar |

## Declaração de uso de inteligência artificial (seção 15)

O grupo declara que utiliza ferramenta de IA generativa (Claude Code) como apoio na construção do sistema da Opção 1 e na elaboração de documentos e scripts. Todos os resultados de testes, defeitos e métricas serão obtidos de execuções reais, e os integrantes são responsáveis por compreender, validar e explicar todo o conteúdo entregue. [CONFIRMAR COM AS ORIENTAÇÕES DO PROFESSOR]
