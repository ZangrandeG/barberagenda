---
lang: pt-BR
---

<!-- Modelo do relatório final (P12). Gerado por scripts/gerar_relatorio.py: não editar o arquivo gerado em entrega/. -->
<!-- Marcadores: {{V:nome}} = valor calculado; {{NOME}} = bloco gerado dos dados; "Tabela: título" antes de uma tabela; -->
<!-- "Quadro: título" = tabela sem número (apêndices); "![título](caminho)" sozinho na linha = figura numerada. -->

::: {custom-style="Capa"}
Centro Universitário Sagrado Coração – UNISAGRADO

Curso de Ciência da Computação

Disciplina: Testes e Qualidade de Software
:::

```{=openxml}
<w:p/><w:p/><w:p/>
```

::: {custom-style="Capa"}
Guilherme Ribeiro Zangrande

José Paulo Dassie Felippi
:::

```{=openxml}
<w:p/><w:p/><w:p/><w:p/><w:p/>
```

::: {custom-style="CapaTitulo"}
Planejamento, execução e avaliação da qualidade do sistema BarberAgenda
:::

::: {custom-style="CapaTexto"}
Relatório final do Projeto Integrado P2

Professor: Prof. Dr. Elvio Gilberto da Silva

Turma A · Grupo Guilherme e José Paulo
:::

```{=openxml}
<w:p/><w:p/><w:p/><w:p/><w:p/><w:p/><w:p/><w:p/>
```

::: {custom-style="Capa"}
Bauru

2026
:::

::: {custom-style="TituloPre"}
Folha de identificação
:::

Tabela: Identificação do projeto

| Item | Informação |
|---|---|
| Curso / disciplina | Ciência da Computação – UNISAGRADO / Testes e Qualidade de Software |
| Professor | Prof. Dr. Elvio Gilberto da Silva |
| Turma e grupo | Turma A · Grupo Guilherme e José Paulo |
| Integrantes | Guilherme Ribeiro Zangrande (RA 23110757, GitHub `ZangrandeG`); José Paulo Dassie Felippi (RA 24111563, GitHub `zepadf`) |
| Sistema testado | BarberAgenda – sistema web de agendamento de barbearia, desenvolvido pelo grupo para a disciplina |
| Versão testada | 1.1.0 (tag `v1.1.0-sistema-base`) no ciclo principal; 1.2.0 (tag `v1.2.0-sistema`) após o ciclo de TDD |
| Aprovação do sistema | Ficha P01 aprovada pelo professor em 19/11/2026, sem ajustes |
| Repositório | https://github.com/ZangrandeG/barberagenda |
| Pipeline e defeitos | GitHub Actions (`.github/workflows/ci.yml`) e GitHub Issues (etiqueta `defeito`) do repositório |
| Pasta de entrega | `P2_TQS_2026_A_GRUPO_GUILHERME_JOSEPAULO_BARBERAGENDA` (espelho em `entrega/` no repositório) |

**Declaração de participação.** Os dois integrantes participaram do planejamento, da execução e da análise do projeto e estão preparados para explicar qualquer parte do trabalho. Os papéis seguem o plano de testes (P03, seção 10); o detalhe de cada atividade está no Diário de Participação (P14).

Tabela: Principais contribuições de cada integrante

| Integrante | Papel principal | Principais contribuições |
|---|---|---|
| Guilherme Ribeiro Zangrande | Coordenação e planejamento; automação e qualidade | Plano de testes, ambiente e versões; testes de unidade e integração (JUnit, Mockito, MockMvc); coleção Postman/Newman; Selenium; SonarQube; ciclo de TDD; pipeline de CI/CD; casos CT-019 a CT-036 |
| José Paulo Dassie Felippi | Análise e execução manual | Requisitos, riscos e casos CT-001 a CT-018; dados de teste; acompanhamento da execução e das evidências; roteiros de aceitação e usabilidade; métricas e plano de melhoria |

**Uso de inteligência artificial (manual, seção 15).** O grupo usou IA generativa (Claude Code), com autorização do professor, na construção do sistema, dos scripts e dos documentos e na execução assistida dos casos, registrada como tal (seção 4.10). Todos os resultados vêm de execuções reais e verificáveis no repositório.

::: {custom-style="TituloPre"}
Lista de figuras
:::

{{LISTA_FIGURAS}}

::: {custom-style="TituloPre"}
Lista de tabelas
:::

{{LISTA_TABELAS}}

::: {custom-style="TituloPre"}
Sumário
:::

{{SUMARIO}}

# 1 INTRODUÇÃO

## 1.1 Contexto

O BarberAgenda é um sistema web de agendamento para uma barbearia fictícia. O cliente se cadastra, escolhe barbeiro, serviço, data e um horário livre e recebe um código de acesso, com o qual consulta ou cancela o próprio agendamento sem precisar de login. O dono da barbearia acessa uma área administrativa protegida por usuário e senha, onde mantém barbeiros e serviços e acompanha a agenda do dia de cada barbeiro.

Este relatório documenta o Projeto Integrado P2 da disciplina Testes e Qualidade de Software: o planejamento, a especificação, a execução, a automação e a avaliação dos testes do BarberAgenda, aplicando os nove tópicos do plano de ensino – fundamentos, níveis e tipos de teste, planejamento, técnicas de projeto de casos, execução e gestão de defeitos, automação, métricas, TDD e integração e entrega contínuas.

## 1.2 Problema

O problema orientador definido no manual da disciplina é: **como demonstrar, por meio de um processo de teste planejado, executado e documentado, que um sistema atende aos requisitos selecionados e quais riscos, defeitos e oportunidades de melhoria permanecem antes de sua disponibilização aos usuários?**

## 1.3 Justificativa

Um sistema de agendamento parece simples, mas concentra regras que falham com facilidade perto dos limites: horário de funcionamento, intervalos de 30 minutos, antecedência máxima de 30 dias, conflito entre agendamentos do mesmo barbeiro e limite de agendamentos ativos por cliente. Uma falha nessas regras gera dois clientes no mesmo horário, atendimentos fora do expediente ou horários ociosos, com prejuízo direto para a barbearia e para o cliente. Além disso, o sistema guarda dados pessoais (nome, telefone e e-mail) e tem uma área administrativa que não pode ser acessada sem autenticação. Por isso, a qualidade precisa ser demonstrada com evidências, e não apenas presumida.

O sistema também foi escolhido porque permite aplicar todos os níveis e ferramentas previstos na disciplina: regras de negócio isoláveis para testes de unidade e TDD, uma API REST própria para testes de integração com Postman/Newman, uma interface web para testes de sistema com Selenium e código-fonte completo para análise estática com SonarQube e para um pipeline de CI/CD.

## 1.4 Objetivos

**Objetivo geral:** elaborar e executar uma estratégia integrada de testes e qualidade para o BarberAgenda, produzindo evidências técnicas e gerenciais que permitam avaliar seu comportamento, sua confiabilidade, sua usabilidade e sua prontidão para uso dentro do escopo definido.

**Objetivos específicos:**

- definir o escopo, os requisitos, os riscos, os recursos e os critérios do processo de teste;

- especificar casos de teste com técnicas de projeto (particionamento de equivalência, análise de valor limite, transição de estados e tabela de decisão) e executá-los com evidências;

- registrar e acompanhar defeitos de forma reproduzível e rastreável;

- automatizar testes de unidade, de integração/API e de sistema/interface e integrá-los a um pipeline de CI/CD;

- aplicar TDD na criação de uma nova regra de negócio;

- calcular métricas com os dados reais do projeto, interpretá-las e propor melhorias contínuas.

## 1.5 Resultado em resumo

::: {custom-style="Destaque"}
**Principais números.** {{V:NRF}} requisitos funcionais e {{V:NRNF}} não funcionais; {{V:NRISCOS}} riscos de produto. {{V:NCASOS}} casos de teste manuais especificados e {{V:EXEC_REG}} execuções registradas; dos {{V:PLANEJADOS}} casos e testes planejados (36 manuais, 8 não funcionais e 4 cenários de aceitação), {{V:EXECUTADOS}} foram executados ({{V:EXECUCAO}}%) e todos foram aprovados ({{V:APROVACAO}}%); 1 caso ficou bloqueado e 5 atividades dependem de uma pessoa externa ao grupo.

**Automação em três níveis:** {{V:NUNIT}} testes de unidade e integração (JUnit), {{V:NREQ_API}} requisições com {{V:NASSERT_API}} asserções de API (Postman/Newman) e {{V:NE2E}} testes de interface (Selenium) repetidos em 2 navegadores e 2 resoluções, todos aprovados e executados em um pipeline de 3 jobs no GitHub Actions. Taxa de automação de {{V:AUTOMACAO}}%.

**Qualidade do código (SonarQube):** bugs de 3 para 0, cobertura de 38,9% para 72,3% e nota de confiabilidade de D para A.

**Defeitos:** nenhum defeito foi observado na execução dos casos. Os problemas relevantes do projeto foram encontrados antes, por revisão de código e análise estática, e corrigidos nas versões 1.0.1, 1.1.0 e 1.2.0.

**Conclusão:** dentro do escopo testado, o BarberAgenda está apto para uso em ambiente de demonstração. Para uso real, faltam a aceitação e a usabilidade com pessoas externas e as melhorias de segurança do plano (seção 11.4).
:::

## 1.6 Organização do relatório

A seção 2 caracteriza o sistema; a seção 3 apresenta escopo, requisitos e riscos; a seção 4 traz o plano de testes; a seção 5 resume a especificação dos casos; as seções 6 a 9 relatam a execução manual e os defeitos, a automação, os testes de integração e de sistema e os testes de aceitação e não funcionais; a seção 10 apresenta as métricas; a seção 11 trata de TDD, CI/CD, análise estática e melhoria contínua; as seções 12 e 13 discutem os resultados e concluem. Os apêndices trazem o catálogo completo dos casos, o registro de cada execução com o resultado obtido, os relatórios de defeito e achados, a matriz de rastreabilidade, os registros dos testes não funcionais e de aceitação, a lista de testes automatizados, o registro de TDD e CI/CD, as pendências, o inventário de evidências e a declaração final do grupo.

# 2 CARACTERIZAÇÃO DO SISTEMA

## 2.1 Finalidade e usuários

O BarberAgenda organiza a agenda de uma barbearia. O sistema tem dois tipos de usuário, com permissões bem separadas:

Tabela: Usuários do BarberAgenda e o que cada um pode fazer

| Usuário | Quem é | O que pode fazer | Autenticação |
|---|---|---|---|
| Cliente | Pessoa que agenda um serviço | Cadastrar-se; ver horários livres; agendar; consultar e cancelar o próprio agendamento | Sem login: usa o código de acesso de 8 caracteres recebido ao agendar, junto com o e-mail |
| Administrador (dono) | Responsável pela barbearia | Cadastrar, editar, desativar e excluir barbeiros e serviços; ver a agenda do dia de cada barbeiro; marcar atendimentos como concluídos | Usuário e senha (login por formulário ou HTTP Basic na API) |

![Tela inicial do BarberAgenda](../14_APRESENTACAO_E_VIDEO_CONTINGENCIA/imagens/tela_inicio.png){width=78%}

## 2.2 Tecnologias e arquitetura

O sistema segue uma arquitetura em camadas. A interface, feita em HTML, CSS e JavaScript sem frameworks, chama a API REST por HTTP/JSON. Os controllers recebem as requisições e validam a entrada; os services aplicam as regras de negócio; os repositories do Spring Data JPA gravam no banco H2. Todas as regras que dependem de data e hora recebem o "agora" de um relógio injetável (`Clock`), o que permite testá-las com uma data fixa. Os erros são devolvidos sempre no mesmo formato JSON (`status`, `erro`, `mensagem`, `campos`), sem detalhes internos.

![Arquitetura em camadas do BarberAgenda](../14_APRESENTACAO_E_VIDEO_CONTINGENCIA/imagens/arquitetura.png){width=92%}

Tabela: Tecnologias e responsabilidades de cada camada

| Camada | Tecnologia | Papel |
|---|---|---|
| Interface | HTML, CSS e JavaScript (páginas estáticas servidas pelo Spring Boot) | Telas do cliente e da área administrativa; chamadas à API com `fetch` |
| API | Java 21, Spring Boot 3.5.16 (Spring Web, Bean Validation) | Rotas REST, validação de entrada, tratamento padronizado de erros (`TratadorErros`) |
| Regras de negócio | Services (`AgendamentoService`, `RegrasAgendamento`, `PoliticaCancelamento`, `ClienteService`, `BarbeiroService`) | Funcionamento, intervalos, antecedência, conflito, limite de ativos, cancelamento |
| Persistência | Spring Data JPA, H2 2.3.232 (arquivo no perfil `dev`, memória no perfil `test`) | Clientes, barbeiros, serviços, agendamentos e usuário administrador |
| Segurança | Spring Security 6 | Login por formulário e HTTP Basic, senha com hash BCrypt, proteção CSRF por cookie e cabeçalho |
| Build | Maven Wrapper (Maven 3.10.1) | Compilação, testes, cobertura (JaCoCo) e empacotamento em um único `.jar` |

## 2.3 Integrações entre componentes

Tabela: Integrações do BarberAgenda e onde cada uma foi verificada

| Integração | Mecanismo | Como foi testada |
|---|---|---|
| Interface ↔ API | HTTP/JSON (`fetch`), cookie e cabeçalho CSRF nas alterações administrativas | Casos manuais pela tela; Selenium (cadastro, agendamento, consulta, cancelamento, administração) |
| API ↔ regras de negócio | Chamadas entre camadas, injeção de dependência | Testes de integração com MockMvc (RF-09); Newman (26 requisições) |
| Regras ↔ banco H2 | Spring Data JPA | Encadeamento no Newman (cadastro → agendamento → consulta → cancelamento); TNF-05 (dados preservados após reinício) |
| Spring Security ↔ área administrativa | Sessão, HTTP Basic e CSRF | CT-027 a CT-029; TNF-02 (28 requisições sem credencial ou com senha errada) |
| Repositório ↔ pipeline | GitHub Actions a cada `push` e `pull_request` | 3 execuções documentadas: aprovada, falha proposital e correção (seção 11.2) |

## 2.4 Regras de negócio

Tabela: Regras de negócio do BarberAgenda (base dos valores limite)

| ID | Regra |
|---|---|
| RN-01 | Nome do cliente obrigatório, de 3 a 60 caracteres |
| RN-02 | Telefone somente com dígitos, 10 ou 11 dígitos (com DDD) |
| RN-03 | E-mail em formato válido e único entre clientes (sem diferenciar maiúsculas) |
| RN-04 | Funcionamento de segunda a sábado, das 09:00 às 19:00; o serviço precisa terminar até 19:00; domingo fechado |
| RN-05 | Agendamentos começam em intervalos de 30 minutos (minuto 00 ou 30) |
| RN-06 | Não é permitido agendar no passado; antecedência máxima de 30 dias |
| RN-07 | Um barbeiro não pode ter dois agendamentos ativos com horários sobrepostos |
| RN-08 | Um cliente pode ter no máximo 3 agendamentos ativos ao mesmo tempo |
| RN-09 | Serviço com duração de 15 a 180 minutos (múltipla de 15) e preço de R\$ 1,00 a R\$ 1.000,00 |
| RN-10 | Somente barbeiros e serviços ativos recebem agendamentos |
| RN-11 | Área administrativa acessível somente com autenticação |
| RF-09 | Cancelamento pelo cliente somente com no mínimo 2 horas de antecedência (criada por TDD, versão 1.2.0) |

## 2.5 Versões e ambiente testado

Todos os testes rodaram em ambiente local, com dados fictícios restaurados antes de cada rodada, e nenhum teste foi executado contra um ambiente de produção ou contra sistemas de terceiros. O sistema passou por quatro versões, todas identificadas por tag no Git:

Tabela: Versões do BarberAgenda e motivo de cada mudança

| Versão (tag) | Mudança | Origem |
|---|---|---|
| 1.0.0 (`v1.0-sistema-base`) | Versão base: cadastro, horários, agendamento, consulta, cancelamento, área administrativa | Construção do sistema |
| 1.0.1 (`v1.0.1-sistema-base`) | A rota de restauração dos dados de teste (`POST /api/dev/reset`) passou a exigir o perfil de administrador | Revisão de segurança do código, antes dos testes |
| 1.1.0 (`v1.1.0-sistema-base`) | A consulta pelo cliente deixou de usar o número sequencial do agendamento e passou a exigir um código de acesso aleatório de 8 caracteres e o e-mail | Revisão de segurança do código, antes dos testes |
| 1.2.0 (`v1.2.0-sistema`) | Nova regra RF-09 (cancelamento com 2 horas de antecedência) e eliminação dos 3 alertas de bug do SonarQube | Ciclo de TDD e análise estática (seção 11) |

::: {custom-style="Destaque"}
**Ajustes de segurança feitos antes dos testes.** Na revisão do código da versão 1.0.0, foram encontrados dois problemas: qualquer pessoa podia apagar e recriar os dados pela rota de restauração, e um cliente podia consultar o agendamento de outro trocando o número na URL, porque os números eram sequenciais. Os dois foram corrigidos (versões 1.0.1 e 1.1.0) antes de os casos serem executados e, por isso, não foram registrados como defeitos de execução; estão descritos no Apêndice C como achados de revisão. Os casos CT-024 e CT-029 e o TNF-02 verificam que as correções continuam valendo.
:::

# 3 ESCOPO, REQUISITOS E RISCOS

## 3.1 Escopo

Ficaram no escopo os fluxos do cliente (cadastro, consulta de horários, agendamento, consulta e cancelamento) e do administrador (login, cadastro de barbeiros e serviços, agenda do dia), na interface web, na API REST e no banco H2, nos navegadores Chrome e Firefox. A regra de antecedência mínima para cancelamento foi reservada desde o início para ser criada por TDD e entrou no escopo como RF-09.

Tabela: Itens fora do escopo e motivo

{{FORA_ESCOPO}}

## 3.2 Requisitos

Foram definidos {{V:REQ_TOTAL}} requisitos verificáveis – {{V:NRF}} funcionais e {{V:NRNF}} não funcionais –, acima do mínimo do manual (6 funcionais e 2 não funcionais). Cada requisito tem identificador único, prioridade e um critério de aceitação observável, com os valores que tornam o resultado objetivo (códigos HTTP, mensagens e limites). A prioridade indica o efeito de uma falha: Alta quando impede o uso principal ou compromete dados, Média quando prejudica parte do uso mas há alternativa.

Tabela: Requisitos funcionais (modelo do Apêndice B do manual)

{{REQUISITOS_RF}}

Tabela: Requisitos não funcionais

{{REQUISITOS_RNF}}

## 3.3 Riscos e prioridades

Cada risco de produto foi classificado por probabilidade e impacto (Baixa, Média ou Alta). A prioridade combina os dois e define a ordem de execução: os riscos de prioridade Alta foram especificados e executados primeiro, foram automatizados em mais de um nível e entram em todas as regressões.

Tabela: Matriz de riscos do produto (modelo do Apêndice C do manual)

{{RISCOS}}

![Mapa de calor dos riscos: probabilidade × impacto](../14_APRESENTACAO_E_VIDEO_CONTINGENCIA/imagens/riscos.png){width=62%}

Três riscos ficaram com prioridade Alta, todos com impacto alto: R-01 (dois clientes no mesmo horário com o mesmo barbeiro), R-02 (agendamento fora do funcionamento ou fora dos intervalos) e R-03 (acesso à área administrativa ou a dados pessoais sem autenticação). Nenhum deles se concretizou nos testes: as regras de conflito e de funcionamento foram verificadas nos valores limite em três níveis (unidade, API e interface), e as 28 tentativas de acesso sem credencial do TNF-02 foram recusadas. O R-12 (cancelamento em cima da hora) foi tratado por meio de uma nova regra, criada por TDD.

# 4 PLANEJAMENTO DOS TESTES

Esta seção resume o plano de testes do projeto (produto P03), organizado nos campos do Apêndice D do manual. O documento completo está em `entrega/03_PLANO_DE_TESTES/`.

## 4.1 Identificação, objetivo e escopo

Tabela: Identificação e objetivo do plano de testes

| Campo | Definição |
|---|---|
| Sistema e versão | BarberAgenda 1.1.0 (tag `v1.1.0-sistema-base`); 1.2.0 após o TDD (tag `v1.2.0-sistema`) |
| Base de teste | Especificação do sistema (`docs/ESPECIFICACAO_SISTEMA.md`, v1.3) e P02 (requisitos e riscos) |
| Objetivo | Verificar, com evidências reproduzíveis, se o sistema atende aos requisitos RF-01 a RF-09 e RNF-01 a RNF-05, priorizando os riscos R-01, R-02 e R-03, e informar os defeitos, riscos residuais e oportunidades de melhoria |
| Escopo | Interface web, API REST e banco H2 (perfis `dev` e `test`), Chrome e Firefox, resoluções 1366×768 e 375×667 |
| Fora do escopo | Itens listados na seção 3.1; testes de carga, estresse e invasão; qualquer teste em produção |

## 4.2 Níveis, tipos e técnicas

A estratégia segue a pirâmide de testes: muitos testes rápidos onde ficam as regras (unidade), menos testes na API e poucos na interface, que são mais lentos e mais frágeis. Os casos foram derivados da especificação (caixa-preta), e não do código, para reduzir o viés de quem construiu o sistema; a aceitação foi planejada para uma pessoa externa ao grupo pelo mesmo motivo.

![Pirâmide de testes aplicada ao BarberAgenda (quantidades da versão 1.2.0)](../14_APRESENTACAO_E_VIDEO_CONTINGENCIA/imagens/piramide.png){width=62%}

Tabela: Níveis de teste: planejado e realizado

| Nível | Objeto | Ferramenta | Mínimo do manual | Realizado |
|---|---|---|---|---|
| Unidade | Regras na camada de serviço e validações de entrada | JUnit 5, AssertJ, Mockito | 6 testes | {{V:NUNIT}} execuções de teste (unidade + integração), 0 falhas |
| Integração/API | API REST com o banco | Postman/Newman; MockMvc | 5 requisições | {{V:NREQ_API}} requisições, {{V:NASSERT_API}} asserções, 0 falhas |
| Sistema (manual) | Aplicação completa | Execução dos casos do P04 | 24 casos | {{V:NCASOS}} casos: {{V:CT_APROV}} aprovados e {{V:CT_BLOQ}} bloqueado |
| Sistema (interface) | Fluxos completos no navegador | Selenium WebDriver 4.53 (Page Objects) | 4 testes | {{V:NE2E}} testes × 4 combinações = {{V:NE2E_TOTAL}} execuções, 0 falhas |
| Aceitação | Cenários do cliente e do dono | Roteiro Dado/Quando/Então | 4 cenários | 4 cenários prontos; aguardam pessoa externa |
| Não funcional | Desempenho, segurança, confiabilidade, compatibilidade, usabilidade | Scripts Python, Selenium, H2 Shell | 6 testes em 3 categorias | 8 testes em 5 categorias; 7 executados |

Os **tipos** de teste aplicados foram: funcional (RF-01 a RF-09, em todos os níveis), não funcional (RNF-01 a RNF-05), confirmação (reexecução após mudança de versão), regressão (suítes automatizadas completas a cada mudança e no pipeline) e, como complemento, teste estático (revisão de código e SonarQube).

Tabela: Técnicas de especificação e onde foram aplicadas

{{TECNICAS}}

## 4.3 Ambiente, ferramentas e dados

Tabela: Ambiente e ferramentas (versões registradas em `entrega/01_SISTEMA_ALVO/ambiente.md`)

| Recurso | Especificação usada |
|---|---|
| Equipamento | Computador do grupo com Windows 11 Pro 10.0.26200 (64 bits) |
| Aplicação | Local em `http://localhost:8080`; perfil `test` (H2 em memória) para os testes automatizados e `dev` (H2 em arquivo) para os testes manuais e de confiabilidade |
| Linguagem e build | Java 21.0.13 (Temurin), Maven 3.10.1 (wrapper), Spring Boot 3.5.16 |
| Testes de unidade | JUnit Jupiter 5.12.2, Mockito 5.17.0, AssertJ 3.27.7, JaCoCo 0.8.16 |
| API | Postman (coleção gerada por `scripts/gerar_colecao_postman.py`) e Newman 6.2.3 |
| Interface | Selenium WebDriver 4.53.0; Google Chrome 157 e Mozilla Firefox 160 (headless) |
| Não funcionais | Python 3.11.9 (`scripts/nf/`), H2 Shell |
| Análise estática | SonarQube Community Build 26.11 (instalação local) |
| CI/CD | GitHub Actions (runner Ubuntu, Java 21) |
| Defeitos | GitHub Issues com modelo de relatório (Apêndice G do manual) e etiquetas de severidade, prioridade e status |
| Controle e rastreabilidade | Planilha P05 (XLSX) gerada a partir de `dados/` por `scripts/gerar_artefatos.py` |

**Dados de teste.** Somente dados fictícios: nomes inventados, telefones fictícios, e-mails `@exemplo.com` e credencial de administrador fictícia (`admin` / `admin123`, apenas nos perfis de teste). A massa inicial tem 3 barbeiros (1 inativo), 5 serviços (1 inativo), 10 clientes e 5 agendamentos com datas relativas ao dia atual e códigos de acesso fixos (`SEMENTE2` a `SEMENTE6`). Antes de cada sessão manual e de cada suíte automatizada, os dados são restaurados por `scripts/reset-dados` (que chama `POST /api/dev/reset` como administrador). Dados criados pelos testes usam e-mails com sufixo único por execução, e os testes de unidade usam um relógio fixo em quarta-feira, 18/11/2026, 10:00.

## 4.4 Responsabilidades

O grupo tem dois integrantes; por isso, os papéis da seção 4.2 do manual foram acumulados, e os dois participaram de todas as etapas.

Tabela: Papéis e responsabilidades

{{RESPONSABILIDADES}}

O papel de **representante do usuário**, que executa a aceitação e a usabilidade, precisa ser de uma pessoa externa ao grupo e ainda está pendente (Apêndice H).

## 4.5 Critérios

Tabela: Critérios de entrada e de saída

| Critério | Definição adotada |
|---|---|
| Entrada | Versão identificada (tag ou commit) e compilando com `./mvnw -DskipTests package`; aplicação no ar no perfil previsto e `scripts/verificar-sistema.sh` sem falhas; dados restaurados; casos especificados e revisados pelo outro integrante; ferramentas instaladas, com versão registrada |
| Saída | 100% dos casos executados ou com justificativa registrada; todos os requisitos com ao menos um teste executado; nenhum defeito Crítico ou Alto aberto; todo defeito corrigido com reteste e regressão; suítes automatizadas aprovadas no pipeline na versão final; 8 métricas calculadas com dados reais |

Tabela: Critérios de suspensão e retomada

{{SUSPENSAO}}

## 4.6 Cronograma realizado

Cada marco terminou com uma tag no repositório, o que permite conferir o estado do projeto em cada etapa.

Tabela: Cronograma de marcos e datas de conclusão

| Marco | Entregas | Conclusão (tag) |
|---|---|---|
| 1 – Fundamentos | Ficha com duas opções de sistema (P01), níveis, tipos e estratégia; sistema base 1.0.0 → 1.1.0 | 18/11/2026 (`marco-1`) |
| 2 – Planejamento | Requisitos, escopo e riscos (P02); plano de testes (P03) | 18/11/2026 (`marco-2`) |
| 3 – Especificação | 36 casos (P04) e matriz de rastreabilidade em XLSX (P05) | 18/11/2026 (`marco-3`) |
| 5 – Automação de unidade | Testes de unidade, JaCoCo e 1ª análise do SonarQube (linha de base) | 18/11/2026 (`marco-5`) |
| 6 – Integração e sistema | Coleção Postman/Newman e testes Selenium | 18/11/2026 (`marco-6`) |
| 7 – Aceitação e não funcionais | Cenários de aceitação, roteiro de usabilidade e 7 testes não funcionais executados | 18/11/2026 (`marco-7`) |
| 4 – Execução e defeitos | Execução dos 35 casos da versão 1.1.0 com evidências (P06); processo de defeitos (P07) | 18/11/2026 (`marco-4`) |
| 9 – TDD, CI/CD e melhoria | Ciclo Red-Green-Refactor (RF-09), versão 1.2.0, pipeline, 2ª análise do SonarQube, plano de melhoria | 18/11/2026 (`marco-9`) |
| 8 – Métricas | 8 indicadores com gráficos e interpretação (P10), calculados com os dados finais | 18/11/2026 (`marco-8`) |
| Aprovação do sistema | Ficha P01 aprovada pelo professor | 19/11/2026 |
| Entrega final | Relatório (P12), apresentação (P13), diário (P14), cópia de segurança | `entrega-final`; relatório ampliado em 26/11/2026 |

A automação (marcos 5 e 6) foi feita antes da execução manual (marco 4) de propósito: a execução manual assistida reaproveitou a infraestrutura de Selenium e de chamadas à API, e os testes não funcionais (marco 7) foram executados antes, porque não dependiam do resultado dos casos manuais. O marco 8 foi fechado depois do 9 para que as métricas usassem os dados finais, inclusive a versão 1.2.0.

## 4.7 Riscos do processo de teste

Tabela: Riscos do processo de teste e respostas

{{RISCOS_PROCESSO}}

## 4.8 Gestão de defeitos

Tabela: Severidade, prioridade e ciclo de vida dos defeitos

{{GESTAO_DEFEITOS}}

## 4.9 Produtos, versionamento e comunicação

Código, scripts, dados e documentos ficam no repositório Git, com commits pequenos em português no padrão `tipo: descrição` e uma tag por marco e por versão do sistema; nenhum histórico foi reescrito. A pasta `entrega/` espelha as 17 pastas obrigatórias do Drive (00 a 16). Todos os artefatos derivados – catálogo de casos, registro de execução, planilha de rastreabilidade, gráficos de métricas e este relatório – são gerados por scripts a partir de uma única fonte de dados (`dados/`), o que evita números diferentes entre documentos. A comunicação com o professor segue os canais da disciplina; entre os integrantes, o andamento é registrado em `docs/PROGRESSO.md`.

## 4.10 Método de execução e uso de ferramentas de IA

::: {custom-style="Destaque"}
**Transparência sobre o método.** Os casos manuais foram executados em **execução assistida por script** (`scripts/execucao_assistida.py`), feita por Claude (IA) a pedido do grupo: o script segue os passos exatos de cada caso do P04, usando Selenium nos passos de tela e chamadas reais à API nos demais, compara o obtido com o esperado, grava a transcrição de cada verificação e captura a tela. Antes do registro oficial, um ensaio completo foi feito fora do registro para separar erros do próprio script de possíveis defeitos do sistema; as falhas do ensaio eram do script e foram corrigidas nele. Cada execução registra o executor, e qualquer caso pode ser reexecutado à mão seguindo os mesmos passos. Nenhum dado, defeito ou métrica foi fabricado.
:::

# 5 ESPECIFICAÇÃO DOS CASOS DE TESTE

Foram especificados {{V:NCASOS}} casos de teste manuais (CT-001 a CT-036; mínimo exigido: 24), no modelo do Apêndice E do manual. Cada caso está ligado a um requisito, a um risco e a uma regra, e tem pré-condições, dados, passos numerados, resultado esperado observável, prioridade e indicação de candidato à automação. O catálogo completo está no Apêndice A.

Tabela: Distribuição dos casos por técnica de projeto

{{CASOS_TECNICA}}

Tabela: Distribuição dos casos por classificação

{{CASOS_CLASSIFICACAO}}

Tabela: Casos e testes por requisito

{{CASOS_REQUISITO}}

## 5.1 Particionamento de equivalência e valores limite

Para cada regra com intervalo, foram identificadas as classes válidas e inválidas e escolhidos os valores exatamente nas fronteiras e imediatamente fora delas:

Tabela: Partições e valores limite por regra (P04, seção 2.1)

{{PARTICOES}}

**Exemplo detalhado – horário de funcionamento (CT-012).** A regra RN-04 aceita atendimentos que começam a partir de 09:00 e terminam até 19:00. Há duas fronteiras: a de início (abertura) e a de término (fechamento), que depende da duração do serviço. Os valores testados e o resultado obtido na execução EX-012 foram:

Tabela: Valores limite do CT-012 e resultado obtido (EX-012)

| Entrada | Classe | Esperado | Obtido (EX-012) |
|---|---|---|---|
| Corte de cabelo (30 min) às 08:30 | Inválida: começa antes da abertura | HTTP 400 com a mensagem da regra | HTTP 400 – aprovado |
| Corte e barba (60 min) às 18:30 | Inválida: terminaria às 19:30 | HTTP 400 com a mensagem da regra | HTTP 400 – aprovado |
| Corte e barba (60 min) às 18:00 | Válida: termina exatamente às 19:00 | HTTP 201, status AGENDADO | HTTP 201 – aprovado |

O limite inferior válido (09:00) e o último início possível de cada serviço foram cobertos pelo CT-011, e o teste de unidade `RegrasAgendamentoTest` repete os mesmos valores com um relógio fixo.

## 5.2 Transição de estados

O agendamento tem três estados. Os casos cobrem as transições válidas e as tentativas inválidas a partir dos estados finais:

Tabela: Transições de estado do agendamento (P04, seção 2.2)

{{TRANSICAO}}

## 5.3 Tabela de decisão

A consulta pelo cliente (RF-05) depende de duas condições, o código de acesso e o e-mail, e todas as combinações foram cobertas:

Tabela: Tabela de decisão da consulta pelo cliente (P04, seção 2.3)

{{DECISAO}}

## 5.4 Candidatos à automação

Foram marcados como candidatos à automação os casos repetitivos, de risco alto e com resultado objetivo, além dos testes não funcionais que podem ser medidos por script. Ao todo, {{V:AUTO_PLAN}} casos e testes foram planejados para automação e {{V:AUTO_FEITOS}} estão automatizados ({{V:AUTOMACAO}}%). Não foram automatizados os cenários de aceitação e o teste de usabilidade, que dependem de pessoas, e os casos de baixo valor de automação, com justificativa no catálogo. Cada teste automatizado indica no nome ou no `@DisplayName` o caso e o requisito que representa (Apêndice F).

# 6 EXECUÇÃO MANUAL E DEFEITOS

## 6.1 Procedimento

A execução seguiu os passos da seção 9.6 do manual: (1) confirmar os critérios de entrada; (2) restaurar os dados fictícios; (3) executar cada passo exatamente como especificado; (4) comparar o obtido com o esperado; (5) classificar o caso como Aprovado, Reprovado, Bloqueado ou Não executado; (6) guardar a evidência com o identificador da execução, do caso e a data; (7) registrar defeito quando houver falha; e (8) depois de uma correção ou mudança de versão, fazer o reteste e a regressão.

As evidências seguem o padrão `EX-NNN_CT-NNN_AAAA-MM-DD` – transcrição em `.txt` com cada requisição, resposta e verificação, e captura de tela em `.png` nos passos de interface – e estão em `entrega/05_EXECUCAO_MANUAL/evidencias/`, com {{V:NEVID05}} arquivos. O registro completo, com o resultado obtido em cada verificação, está no Apêndice B.

## 6.2 Resultado do ciclo principal

Os 35 casos da versão 1.1.0 (CT-001 a CT-035) foram executados em 18/11/2026, e todos foram aprovados na primeira execução. Depois da mudança para a versão 1.2.0 (TDD), os casos de cancelamento afetados pela nova regra (CT-022, CT-025 e CT-026) foram reexecutados e aprovados, e o caso criado para o RF-09 (CT-036) ficou bloqueado, como explicado na seção 6.3. O último resultado ficou em {{V:CT_APROV}} aprovados, {{V:CT_REPROV}} reprovados e {{V:CT_BLOQ}} bloqueado.

Tabela: Resultado de cada execução dos casos manuais (detalhes no Apêndice B)

{{EXECUCOES_CICLO}}

![Resultado atual dos casos e testes planejados](../11_METRICAS_E_QUALIDADE/metricas/01_resultado_dos_casos.png){width=70%}

As figuras a seguir mostram duas evidências da execução: a recusa de um nome abaixo do limite no cadastro e a recusa de uma consulta com o código de outra pessoa.

![EX-022 (CT-003): cadastro recusado com nome de 2 caracteres, abaixo do limite de 3](../05_EXECUCAO_MANUAL/evidencias/EX-022_CT-003_2026-11-18_a.png){width=80%}

![EX-034 (CT-024): consulta recusada quando o código SEMENTE2 é usado com o e-mail de outro cliente](../05_EXECUCAO_MANUAL/evidencias/EX-034_CT-024_2026-11-18_a.png){width=80%}

## 6.3 Caso bloqueado

O **CT-036** (RF-09: cancelar com menos de 2 horas de antecedência deve ser recusado com HTTP 422) exige criar um agendamento para daqui a menos de 2 horas, ainda dentro do horário de funcionamento. A execução EX-046 foi feita às 23h, quando não existe nenhum horário válido nas 2 horas seguintes; por isso, o caso foi classificado como **Bloqueado**, e não como reprovado. A regra está coberta pelos testes de unidade e de integração criados no TDD, que usam um relógio fixo e passam em qualquer horário (seção 11.1). A execução manual em horário comercial é a ação M-02 do plano de melhoria.

## 6.4 Defeitos registrados

**Nenhum defeito foi observado na execução dos casos** e, portanto, nenhum foi registrado no GitHub Issues. O processo de registro está pronto: o repositório tem o modelo de relatório do Apêndice G do manual, etiquetas de severidade, prioridade e status e um script que exporta as issues para a planilha (`scripts/exportar_defeitos.py`). Nenhum defeito foi inventado para "ter o que registrar" (manual, seção 9.7).

Esse resultado precisa ser lido com contexto. O sistema é pequeno, foi construído pelo próprio grupo com uma especificação pensada para os testes, e os problemas mais relevantes foram encontrados **antes** da execução dos casos, por técnicas estáticas:

Tabela: Problemas encontrados antes da execução dos casos (detalhes no Apêndice C)

| ID | Problema | Como foi encontrado | Correção |
|---|---|---|---|
| A-01 | Rota de restauração dos dados (`POST /api/dev/reset`) acessível sem autenticação | Revisão de segurança do código | Versão 1.0.1: exige perfil de administrador |
| A-02 | Consulta do agendamento pelo número sequencial: um cliente podia ver o agendamento de outro trocando o número | Revisão de segurança do código | Versão 1.1.0: código de acesso aleatório de 8 caracteres + e-mail |
| A-03 | 3 alertas de bug (regra `java:S8696`) na comparação do dia da semana | SonarQube, 1ª análise | Versão 1.2.0: comparação reescrita, comportamento inalterado |
| A-04 | Mesmo padrão da regra `java:S8696` no código de teste (`TesteE2EBase`) | SonarQube, análise intermediária | Ajustado no código de teste |
| A-05 | 2 vulnerabilidades: cookie `XSRF-TOKEN` sem `HttpOnly` (`java:S3330`) e proteção CSRF restrita (`java:S4502`) | SonarQube | Mantidas como decisão de projeto justificada; risco aceito e ação M-03 |

## 6.5 Reteste e regressão

Tabela: Reexecuções e regressão após a mudança para a versão 1.2.0

| Execução | O que foi verificado | Resultado |
|---|---|---|
| EX-043 (CT-022) | Cliente no limite de 3 ativos volta a poder agendar depois de cancelar, já com a regra das 2 horas | Aprovado |
| EX-044 (CT-025) | Cancelamento pela tela libera o horário, com antecedência maior que 2 horas | Aprovado |
| EX-045 (CT-026) | Cancelar agendamento já cancelado ou concluído continua sendo recusado | Aprovado |
| EX-046 (CT-036) | Cancelamento com menos de 2 horas recusado com HTTP 422 | Bloqueado (horário) |
| Regressão automatizada | Unidade + integração ({{V:NUNIT}}), Newman ({{V:NREQ_API}} requisições, {{V:NASSERT_API}} asserções) e Selenium ({{V:NE2E}} testes) na versão 1.2.0 | Todos aprovados (`entrega/12_TDD_CICD_MELHORIA/regressao_v1.2.0/`) |

## 6.6 Observações que não são defeitos

- **Falhas do script no ensaio.** No ensaio feito antes do registro oficial, algumas verificações falharam por erro do próprio script de execução assistida (por exemplo, comparação de texto com espaço especial e codificação de acentos na linha de comando). Essas falhas foram corrigidas no script e não são defeitos do sistema; por isso, o ensaio não entrou no registro oficial.

- **Falha proposital do pipeline.** A execução 44441895872 do GitHub Actions falhou de propósito, para demonstrar que o pipeline barra uma mudança que quebra um teste (seção 11.2). Também não é defeito do sistema.

- **Respostas 403 sem credencial.** Nas alterações administrativas sem credencial, o sistema responde 403 (e não 401), porque a proteção CSRF é verificada antes da autenticação. O comportamento atende ao RNF-02, que aceita 401 ou 403 sem dados no corpo.

# 7 AUTOMAÇÃO

## 7.1 Arquitetura dos testes

Os testes automatizados ficam no repositório, separados por nível, e usam a mesma massa fictícia dos testes manuais:

```text
barberagenda/
├── src/test/java/br/com/barberagenda/
│   ├── unit/          JUnit 5 + Mockito: regras e validações, relógio fixo (DadosTeste)
│   ├── integration/   Spring Boot Test + MockMvc: RF-09 de ponta a ponta na API
│   └── e2e/           Selenium (perfil Maven -Pe2e): testes e Page Objects (pages/)
├── postman/           coleção e ambiente do Postman (executados pelo Newman)
├── scripts/nf/        testes não funcionais em Python (desempenho, segurança, reinício)
├── dados/             fonte única: requisitos, riscos, casos, execuções e defeitos
└── .github/workflows/ci.yml   pipeline com 3 jobs
```

## 7.2 Testes de unidade (JUnit 5)

Os testes de unidade verificam as regras de negócio isoladamente, sem banco, rede ou interface: os repositórios são substituídos por *mocks* do Mockito e as validações usam o Bean Validation sem subir o Spring. O "agora" vem de um relógio fixo, de modo que os testes de data dão o mesmo resultado em qualquer dia. Cada teste tem uma única intenção, nome descritivo (`deveRejeitar...`, `deveAceitar...`) e `@DisplayName` com o caso e o requisito que representa; os valores limite usam testes parametrizados. A lista completa, método por método, está no Apêndice F.

Tabela: Testes de unidade e integração por classe (regressão da versão 1.2.0)

{{UNIDADE_CLASSES}}

**Cobertura de código (JaCoCo).** Na versão final, as suítes de unidade e integração cobrem 74,4% das linhas e 62,7% dos ramos do projeto; a classe de regras `RegrasAgendamento` tem 100% das linhas cobertas e `AgendamentoService`, mais de 90%. Na linha de base (só testes de unidade), a cobertura era de 36,4%: controllers, segurança e carga de dados só passaram a ser exercitados quando entraram os testes de integração com `@SpringBootTest`, criados no TDD.

## 7.3 Testes de integração/API (Postman + Newman)

A coleção do Postman verifica a cadeia interface → API → regras → banco. Ela restaura os dados, obtém os identificadores pelas consultas públicas e **encadeia** os dados entre as requisições (o cliente cadastrado é usado no agendamento; o código de acesso devolvido é usado na consulta e no cancelamento). As asserções conferem o status HTTP, o contrato da resposta (campos, tipos, cabeçalho `Location`, formato do código de acesso), as mensagens de erro sem detalhes internos e a ausência de efeito colateral (por exemplo, o serviço criado sem credencial não existe). Cada operação crítica tem um fluxo positivo e um negativo, e a coleção restaura os dados ao final.

Tabela: Coleção do Postman por pasta (lista completa no Apêndice F)

{{POSTMAN_RESUMO}}

Na regressão da versão 1.2.0, o Newman executou {{V:NREQ_API}} requisições com {{V:NASSERT_API}} asserções e {{V:NFALHA_API}} falhas (relatórios HTML e JUnit em `entrega/08_INTEGRACAO_API/relatorios/` e `entrega/12_TDD_CICD_MELHORIA/regressao_v1.2.0/`).

## 7.4 Testes de sistema/interface (Selenium)

Os testes de interface usam o padrão Page Object (uma classe por tela em `e2e/pages/`), localizadores estáveis (`id` e `data-testid`), esperas explícitas (`WebDriverWait`, sem esperas fixas), verificação do resultado na tela e captura automática de tela ao final de cada teste, com navegador, resolução e resultado no nome do arquivo. O navegador e o tamanho da janela são escolhidos na linha de comando (`-Dnavegador`, `-Djanela`), o que permitiu repetir a mesma suíte em 4 combinações.

Tabela: Testes de interface por classe (Chrome, 1366×768)

{{E2E_CLASSES}}

![Teste Selenium do agendamento completo (CT-010): mensagem de sucesso com o código de acesso gerado](../09_SISTEMA_INTERFACE/capturas/AgendamentoE2ETest_deveAgendarHorarioPelaTela_chrome_1366x768_OK.png){width=80%}

## 7.5 Como executar

```bash
# unidade + integração, com cobertura JaCoCo
./mvnw test
# API: em outro terminal, subir a aplicação no perfil test e rodar a coleção
./mvnw spring-boot:run -Dspring-boot.run.profiles=test
newman run postman/BarberAgenda.postman_collection.json \
       -e postman/BarberAgenda.postman_environment.json
# interface (trocar por firefox e/ou 375x667 para as outras combinações)
./mvnw test -Pe2e -Dnavegador=chrome -Djanela=1366x768
# um teste com o navegador visível
./mvnw test -Pe2e -Dtest=AgendamentoE2ETest -Dheadless=false
```

## 7.6 Limitações da automação

- A captura de tela automática em caso de falha do Selenium não chegou a ser exercitada por um erro real, porque nenhum teste de interface falhou fora da demonstração do pipeline.

- Os testes rodam em Chrome e Firefox; Edge, Safari e dispositivos iOS ficaram fora do escopo por não estarem disponíveis no ambiente do grupo.

- O CT-036 depende do horário atual na execução manual; na automação, o relógio fixo elimina essa dependência.

- Não há teste automatizado de concorrência real (dois pedidos simultâneos para o mesmo horário); o tratamento existe no código, mas fica como ação M-05.

# 8 TESTES DE INTEGRAÇÃO E DE SISTEMA

Os testes de integração verificaram a comunicação entre componentes sem depender da tela; os testes de sistema percorreram os fluxos completos como o usuário faz.

Tabela: Integrações validadas e resultado

| Comunicação validada | Evidência | Resultado |
|---|---|---|
| Interface → API: cadastro e validação | CT-001 a CT-006; Newman pasta 01; Selenium `CadastroClienteE2ETest` | Atende: 201 com dados válidos; 400 com a mensagem do campo; 409 para e-mail repetido |
| API → regras: horários disponíveis | CT-007 a CT-009; `RegrasAgendamentoTest`; Newman pasta 00 | Atende: só horários de 30 em 30 min, dentro do funcionamento e livres |
| API → regras → banco: agendamento | CT-010 a CT-022; Newman pastas 02 e 03; Selenium `AgendamentoE2ETest` | Atende: limites de horário, antecedência, conflito e limite de ativos respeitados |
| API → banco: consulta e cancelamento | CT-023 a CT-026; Newman pasta 04; Selenium `CancelamentoE2ETest` | Atende: horário liberado após cancelar; consulta alheia recusada com a mesma mensagem |
| Spring Security → área administrativa | CT-027 a CT-029; Newman pasta 05; TNF-02 | Atende: 28/28 acessos sem credencial recusados, sem dados no corpo |
| API administrativa → banco | CT-030 a CT-035; Newman pasta 06; Selenium `AdminServicoE2ETest` | Atende: limites de duração e preço; exclusão recusada com agendamentos; agenda sem códigos de acesso |
| API → regra de cancelamento (RF-09) | `CancelamentoAntecedenciaIntegracaoTest` (MockMvc); `AgendamentoServiceTest` | Atende na automação (422 com 1h30; 200 com 2h); caso manual bloqueado por horário |
| Aplicação → banco após reinício | TNF-05 | Atende: dados iguais depois de parar e subir a aplicação |

**Fluxos ponta a ponta executados:** cadastro até a mensagem de sucesso; cadastro inválido até a mensagem do campo; escolha de barbeiro, serviço, data e horário até a confirmação com o código de acesso; consulta pelo código até o cancelamento e a liberação do horário; login do administrador, cadastro de serviço e saída; agenda do dia até a conclusão do atendimento.

![Agenda do dia na área administrativa após marcar um atendimento como concluído (EX-040, CT-034)](../05_EXECUCAO_MANUAL/evidencias/EX-040_CT-034_2026-11-18_b.png){width=80%}

# 9 TESTES DE ACEITAÇÃO E NÃO FUNCIONAIS

## 9.1 Testes de aceitação

Os quatro cenários de aceitação foram escritos no formato Dado / Quando / Então, do ponto de vista do cliente e do dono da barbearia, para execução por uma **pessoa que não participou da construção dos testes** (manual, seção 9.11). O grupo prepara o ambiente e apenas observa. Os roteiros completos estão no Apêndice E.

Tabela: Cenários de aceitação e situação

| Cenário | Perfil | Tarefa | Situação |
|---|---|---|---|
| CA-01 | Cliente novo | Cadastrar-se e agendar o primeiro corte | Pronto; aguarda participante externo |
| CA-02 | Cliente | Consultar e cancelar o agendamento; ver o horário liberado | Pronto; aguarda participante externo |
| CA-03 | Dono | Confirmar que nenhum barbeiro recebe dois clientes ao mesmo tempo | Pronto; aguarda participante externo |
| CA-04 | Dono | Cadastrar um serviço, abrir a agenda do dia e concluir um atendimento | Pronto; aguarda participante externo |

A aceitação não pode ser simulada pelo grupo nem pela ferramenta de IA, porque seu objetivo é justamente a visão de quem não construiu o sistema. Os resultados serão registrados no P09 e em `dados/execucoes.csv` depois da sessão, e as métricas serão recalculadas pelos scripts.

## 9.2 Testes não funcionais

Foram planejados 8 testes não funcionais em 5 categorias (desempenho, segurança básica, confiabilidade, compatibilidade e usabilidade), acima do mínimo de 6 testes em 3 categorias. Sete foram executados; o de usabilidade depende de um participante externo. Nenhum teste foi destrutivo ou invasivo: todas as medições rodaram no ambiente local, sem carga, estresse ou invasão (manual, seção 15). Os registros completos, no modelo do Apêndice I do manual, estão no Apêndice E.

Tabela: Resultados dos testes não funcionais

{{NF_RESUMO}}

## 9.3 Desempenho (TNF-01)

O script `scripts/nf/desempenho.py` restaura os dados, faz 5 requisições de aquecimento e mede 30 requisições de cada operação principal do cliente: a consulta de horários disponíveis e a criação de agendamento (com 35 pedidos válidos em horários distintos). O critério do RNF-01 é o percentil 95 abaixo de 500 ms.

Tabela: Tempos de resposta medidos no TNF-01

{{TNF01}}

![Tempos de resposta das 60 medições do TNF-01 comparados com o critério](figuras/tnf01_tempos.png){width=88%}

As 60 medições ficaram entre 4 ms e 34 ms, com folga de mais de 14 vezes em relação ao critério. A ressalva é que o ambiente é local, com cliente e servidor na mesma máquina e sem latência de rede, e que o teste não mede carga concorrente.

## 9.4 Segurança básica (TNF-02 a TNF-04)

- **Controle de acesso (TNF-02):** 14 rotas restritas (`/api/admin/**`, listagem e detalhe de clientes e a rota de restauração) foram chamadas em 2 cenários – sem credencial e com senha errada –, num total de 28 requisições. Todas foram recusadas (401 nas consultas sem credencial e com senha errada; 403 nas alterações sem credencial, por causa do CSRF), com corpo contendo apenas `status`, `erro`, `mensagem` e `campos`, sem stack trace, nomes de classe ou SQL.

- **Armazenamento da senha (TNF-03):** com a aplicação parada, a consulta direta ao banco mostrou que a senha do administrador está guardada como hash BCrypt (prefixo `$2a$10$`, 60 caracteres) e que o texto da senha não aparece no banco.

- **HTML/script digitado pelo usuário (TNF-04):** um cliente cadastrado com o nome `<img src=x onerror=alert('xss')>` teve o nome exibido literalmente nas telas, sem criar elemento `<img>` nem abrir alerta, nos 2 navegadores e nas 2 resoluções.

## 9.5 Confiabilidade (TNF-05 e TNF-06)

- **Recuperação após reinício (TNF-05):** no perfil `dev`, com banco em arquivo, um cliente e um agendamento foram criados, a aplicação foi encerrada e iniciada de novo, e o agendamento foi encontrado pelo código de acesso com todos os dados iguais.

- **Entradas inválidas (TNF-06):** 16 entradas inválidas – JSON malformado, corpo vazio, tipo errado, data inexistente (30/02), textos de 10.000 caracteres, parâmetros ausentes, rota inexistente, método e tipo de conteúdo não suportados, entre outras – receberam respostas 400, 404, 405 ou 415, nenhuma 500 e nenhuma com detalhes internos.

## 9.6 Compatibilidade (TNF-07)

A suíte Selenium completa ({{V:NE2E}} testes) foi executada no Chrome 157 e no Firefox 160, nas janelas de 1366×768 (computador) e 375×667 (celular): {{V:NE2E_TOTAL}} execuções, todas aprovadas. Além dos fluxos, o teste `CompatibilidadeE2ETest` confere, em 5 páginas, que a largura do conteúdo não passa da largura visível, ou seja, que não há rolagem horizontal no celular.

![Agendamento concluído pelo Selenium na largura de celular (375×667): Chrome à esquerda e Firefox à direita](figuras/compat_celular.png){width=70%}

## 9.7 Usabilidade (TNF-08)

O critério do RNF-05 é que um participante externo, sem instruções além do objetivo da tarefa, conclua o cadastro e o agendamento em até 5 minutos, sem ajuda, e avalie a facilidade com nota maior ou igual a 4 em 5. O roteiro de observação e o questionário estão prontos (`P09_Roteiro_Usabilidade.md`), mas o teste ainda **não foi executado**, porque depende de uma pessoa externa ao grupo. Por isso, o RNF-05 aparece como requisito sem teste executado nas métricas.

# 10 MÉTRICAS E INDICADORES

As métricas foram calculadas por `scripts/metricas.py` com os dados reais de `dados/` e conferidas com a aba Métricas da planilha P05, onde as mesmas fórmulas estão escritas. Em todas, vale o **último resultado** de cada caso. Os denominadores incluem os {{V:PLANEJADOS}} casos e testes planejados: os 36 casos manuais, os 8 testes não funcionais e os 4 cenários de aceitação.

Tabela: Painel das 8 métricas obrigatórias (modelo do Apêndice K do manual)

{{METRICAS}}

![Indicadores percentuais](../11_METRICAS_E_QUALIDADE/metricas/02_indicadores_percentuais.png){width=72%}

**Interpretação.**

- **Percentual de execução ({{V:EXECUCAO}}%).** Dos {{V:PLANEJADOS}} casos e testes planejados, {{V:EXECUTADOS}} foram executados. Os 6 restantes são as 5 atividades que dependem de uma pessoa externa (4 cenários de aceitação e o teste de usabilidade) e o CT-036, bloqueado por horário. Tudo o que o grupo podia executar sozinho foi executado.

- **Taxa de aprovação ({{V:APROVACAO}}%) e de reprovação ({{V:REPROVACAO}}%).** Todos os casos executados obtiveram o resultado esperado. O número é alto e não significa ausência de defeitos: significa que, no escopo e com as técnicas aplicadas, nenhuma falha foi observada. Os problemas relevantes foram encontrados antes, por técnicas estáticas (seção 6.4).

- **Cobertura de requisitos ({{V:COBERTURA}}%).** {{V:REQ_EXEC}} dos {{V:REQ_TOTAL}} requisitos têm teste executado. Faltam o RNF-05 (usabilidade, depende do participante externo) e o RF-09, cujo caso manual ficou bloqueado. O RF-09 está coberto pelos testes automatizados do TDD; considerando também a automação, a cobertura seria de 13/14 = 92,9%. A métrica oficial usa apenas os casos do catálogo.

- **Taxa de automação ({{V:AUTOMACAO}}%).** Todos os candidatos à automação têm teste automatizado em todos os níveis planejados, e a regressão completa roda no pipeline a cada envio de código.

- **Defeitos por severidade e por status (0) e taxa de reabertura.** Sem defeitos registrados, não há itens abertos, e o critério de saída "nenhum defeito Crítico ou Alto aberto" está atendido. A taxa de reabertura é indefinida (0 reabertos / 0 retestados), e não 0%: a fórmula exige defeitos retestados.

![Resultado atual dos casos e testes por requisito](figuras/resultado_por_requisito.png){width=88%}

O gráfico por requisito mostra que as pendências estão concentradas em três lugares: a aceitação (que aparece em RF-01 a RF-08, porque cada cenário cobre vários requisitos), o RNF-05 (usabilidade) e o RF-09 (caso manual bloqueado). Os requisitos de prioridade Alta (RF-01 a RF-06 e RNF-02) tiveram todos os seus casos manuais aprovados.

## 10.1 Indicadores complementares de qualidade (SonarQube)

Tabela: Indicadores do SonarQube: linha de base e análise final

{{SONAR}}

![Bugs e cobertura no SonarQube: linha de base e análise final](../14_APRESENTACAO_E_VIDEO_CONTINGENCIA/imagens/sonar.png){width=80%}

## 10.2 Rastreabilidade

Tabela: Resumo da matriz de rastreabilidade por requisito (matriz completa no Apêndice D e na planilha P05)

{{RASTREABILIDADE}}

A coluna "Pend." soma os casos bloqueados e não executados. Os requisitos marcados como "Atendido no que foi executado" têm todos os casos executados aprovados, mas ainda têm cenário de aceitação ou caso pendente.

# 11 TDD, CI/CD E MELHORIA CONTÍNUA

## 11.1 Evolução por TDD (RF-09)

O comportamento escolhido foi uma regra nova, que não existia na versão 1.1.0 e foi reservada desde o planejamento para esta etapa: **o cliente só pode cancelar um agendamento com no mínimo 2 horas de antecedência**; caso contrário, a API responde HTTP 422 com mensagem explicativa. A regra trata o risco R-12 (cancelamento em cima da hora deixa o horário ocioso). O ciclo Red-Green-Refactor teve um commit em cada etapa:

Tabela: Ciclo Red-Green-Refactor (modelo do Apêndice J do manual)

{{TDD_COMMITS}}

![Ciclo de TDD aplicado ao RF-09](../14_APRESENTACAO_E_VIDEO_CONTINGENCIA/imagens/tdd.png){width=90%}

**RED.** Os testes foram escritos antes da implementação: na unidade (`AgendamentoServiceTest`: cancelar 1h59, 1h30 e 30 minutos antes deve ser recusado; exatamente 2 horas antes deve ser aceito) e na integração (`CancelamentoAntecedenciaIntegracaoTest`, com MockMvc e relógio fixo em 18/11/2026 às 09:00). A execução de `./mvnw test` falhou pelo motivo esperado: "Expecting code to raise a throwable" nos testes de unidade e "Status expected:<422> but was:<200>" no de integração. O teste de integração, como estava no commit RED:

{{CODIGO_RED}}

**GREEN.** A implementação mínima verificou o prazo em `AgendamentoService.cancelarPeloCliente` e criou a exceção `CancelamentoForaDoPrazoException`, traduzida para 422 pelo tratador de erros. Todos os testes passaram.

**REFACTOR.** A regra foi isolada na classe `PoliticaCancelamento`, com a antecedência mínima em uma constante e a mensagem em um único lugar, usando o relógio injetável; o comportamento não mudou e todos os testes continuaram aprovados:

{{CODIGO_POLITICA}}

**Aprendizado.** Escrever o teste antes obrigou a decidir o limite exato (2 horas é permitido; 1h59 não) e o código HTTP antes de programar. O relógio injetável permitiu testar uma regra dependente da hora atual a qualquer momento – ao contrário da execução manual do CT-036, que só é possível em horário comercial.

## 11.2 Pipeline de CI/CD

O pipeline está em `.github/workflows/ci.yml` e roda a cada `push` (em qualquer branch), a cada `pull_request` para a `main` e sob demanda. Ele tem três jobs; os de API e de interface dependem do primeiro e só rodam se os testes de unidade e integração passarem. Os relatórios de cada job são publicados como artefatos da execução.

![Etapas do pipeline de CI/CD](../14_APRESENTACAO_E_VIDEO_CONTINGENCIA/imagens/pipeline.png){width=90%}

Tabela: Jobs do pipeline

| Job | Etapas | Publicação |
|---|---|---|
| Unidade + integração + cobertura | Checkout → Java 21 com cache do Maven → `./mvnw -B verify` (testes e JaCoCo) | Relatórios Surefire e JaCoCo |
| API (Postman + Newman) | Checkout → Java 21 → aplicação no perfil `test` → Node.js e Newman → coleção completa | Relatórios do Newman (CLI, HTML e JUnit) |
| Interface (Selenium) | Checkout → Java 21 → `./mvnw test -Pe2e` com Chrome headless | Relatórios Surefire e capturas de tela |

Tabela: Execuções do pipeline documentadas

| Execução | Contexto | Resultado | Significado |
|---|---|---|---|
| 44441467718 | `push` na `main` | 3 jobs aprovados | Pipeline funcionando na versão 1.2.0 |
| 44441895872 | Branch `demo/falha-pipeline`: teste do CT-007 alterado de propósito para esperar 20 horários em vez de 19 | Job de unidade reprovado (`Expected size: 20 but was: 19`); API e interface pulados | Falha controlada: o pipeline barra uma mudança que quebra um teste |
| 44442093641 | Commit seguinte na mesma branch, desfazendo a alteração | 3 jobs aprovados | Correção confirmada pelo pipeline |

A falha da execução 44441895872 foi **proposital**, não é defeito do sistema e não foi registrada como defeito. A branch de demonstração não foi integrada à `main` e fica no repositório como evidência. Todas as execuções podem ser abertas em `github.com/ZangrandeG/barberagenda/actions`.

## 11.3 Análise estática (SonarQube)

A análise estática foi feita duas vezes no SonarQube Community Build 26.11 local: a linha de base logo após os testes de unidade (versão 1.1.0) e a análise final depois do TDD (versão 1.2.0). Os números estão na Tabela da seção 10.1.

- **3 bugs (`java:S8696`).** A comparação `getDayOfWeek() == DayOfWeek.SUNDAY` foi apontada como bug. Como `DayOfWeek` é um enum, o `==` já funcionava corretamente (falso positivo da regra), mas a comparação foi reescrita com `equals()` para eliminar o alerta, sem mudança de comportamento, confirmada pela regressão. Uma análise intermediária apontou o mesmo padrão no código de teste, que também foi ajustado.

- **Cobertura de 38,9% para 72,3%.** Subiu porque os testes de integração com `@SpringBootTest`, criados no TDD, passaram a exercitar controllers, segurança e carga de dados, que os testes de unidade não alcançam. O código novo teve 95,8% de cobertura, e o quality gate ficou aprovado.

- **2 vulnerabilidades mantidas.** O cookie `XSRF-TOKEN` sem `HttpOnly` (`java:S3330`) é necessário, porque o JavaScript precisa lê-lo para enviar o token CSRF; a proteção CSRF restrita (`java:S4502`) é exigida justamente nas alterações feitas com sessão, enquanto as rotas públicas não usam sessão e as chamadas HTTP Basic não usam cookie. São decisões de projeto documentadas e ficam como risco aceito, com a ação M-03 no plano de melhoria.

## 11.4 Plano de melhoria contínua

Tabela: Ações de melhoria priorizadas

{{MELHORIAS}}

# 12 DISCUSSÃO DOS RESULTADOS

## 12.1 Pontos fortes

- **Regras de agendamento sólidas.** Funcionamento, intervalos, antecedência, conflito entre agendamentos e limite de ativos se comportaram como especificado em todos os valores limite, nos três níveis de teste.

- **Controle de acesso e proteção de dados.** As 28 tentativas de acesso sem credencial foram recusadas sem expor dados; a senha está com hash BCrypt; a consulta pelo cliente exige código aleatório e e-mail; HTML digitado não é executado.

- **Robustez.** Nenhuma das 16 entradas inválidas provocou erro interno (HTTP 500), e os dados sobreviveram ao reinício da aplicação.

- **Desempenho com grande folga.** As operações principais responderam em menos de 35 ms no ambiente local.

- **Processo reproduzível.** Uma única fonte de dados gera a planilha, os documentos, os gráficos e este relatório; os testes de data usam relógio fixo; os dados são restaurados por script; a regressão completa roda no pipeline a cada envio de código.

## 12.2 Pontos frágeis

- **Viés de quem construiu o sistema.** O grupo construiu o sistema que testou, com apoio de IA, e a especificação já foi pensada para os testes. A taxa de aprovação de 100% e a ausência de defeitos devem ser lidas com essa ressalva; a aceitação e a usabilidade com pessoas externas são justamente a forma de reduzir esse viés.

- **Execução manual assistida por script.** Os casos foram executados por um script que segue os passos do catálogo, e não manualmente pelos integrantes. O método é reproduzível e transparente, mas não substitui a observação humana de detalhes de usabilidade.

- **Escala dos testes não funcionais.** O desempenho foi medido localmente, sem carga e sem latência de rede, e a concorrência real não foi testada.

- **Consulta sem limite de tentativas.** O código de acesso aleatório torna improvável adivinhar um agendamento, mas não há limite de tentativas por minuto (ação M-04).

## 12.3 Riscos residuais

Tabela: Situação dos riscos de produto após os testes

| Risco | Situação após os testes |
|---|---|
| R-01 Horários sobrepostos | Mitigado: sobreposição total, parcial e encostada verificadas em unidade, API e interface |
| R-02 Fora do funcionamento ou dos intervalos | Mitigado: limites de início, término, domingo e minutos verificados |
| R-03 Acesso indevido | Mitigado: 28/28 acessos recusados; rota de restauração protegida desde a versão 1.0.1 |
| R-04 Regras de data perto dos limites | Mitigado: D+30/D+31 e "agora" verificados com relógio fixo |
| R-05 Dados inválidos aceitos | Mitigado: limites de nome, telefone, e-mail, duração e preço verificados |
| R-06 Mais de 3 agendamentos ativos | Mitigado: 3º aceito, 4º recusado, vaga liberada após cancelar |
| R-07 Consultar ou cancelar agendamento de outra pessoa | Mitigado em parte: código aleatório + e-mail; sem limite de tentativas (M-04) |
| R-08 HTML/script executado | Mitigado: TNF-04 aprovado em 2 navegadores e 2 resoluções |
| R-09 Interface ruim no celular ou no Firefox | Mitigado: 44/44 execuções aprovadas; usabilidade ainda não avaliada por pessoa externa |
| R-10 Perda de dados após reinício | Mitigado: TNF-05 aprovado |
| R-11 Consulta de horários lenta | Mitigado no ambiente local: p95 de 26,2 ms |
| R-12 Cancelamento em cima da hora | Tratado pela regra RF-09 (TDD); verificado na automação; caso manual pendente (M-02) |

Permanecem como riscos aceitos as duas vulnerabilidades do SonarQube (M-03) e o perfil PostgreSQL, que não foi validado por falta de Docker no ambiente (M-07).

## 12.4 Limitações deste trabalho

- A aceitação (CA-01 a CA-04) e a usabilidade (TNF-08) ainda não foram executadas, porque dependem de uma pessoa externa ao grupo.

- O CT-036 precisa ser executado manualmente em horário comercial.

- Os testes de interface cobrem Chrome e Firefox; Edge, Safari e iOS não foram testados.

- A análise do SonarQube foi feita em uma instalação local e ainda não faz parte do pipeline (ação M-06).

## 12.5 Lições aprendidas

A principal lição foi que **técnicas estáticas e dinâmicas se complementam**: a revisão de código e o SonarQube encontraram mais problemas do que a execução dos casos, e os casos confirmaram que as correções continuaram valendo. A segunda foi o valor do **relógio injetável**: ele tornou reproduzíveis os testes de regras de data, que de outra forma dependeriam do dia e da hora da execução. A terceira foi a vantagem de manter **uma única fonte de dados**: requisitos, casos, execuções e métricas ficaram consistentes em todos os documentos, e qualquer nova execução atualiza a planilha, os gráficos e este relatório com um comando.

# 13 CONCLUSÃO

O projeto aplicou os nove tópicos da disciplina a um sistema real e executável: planejamento orientado a riscos, {{V:NCASOS}} casos especificados com quatro técnicas de projeto, execução com evidências de cada verificação, automação em três níveis com {{V:AUTOMACAO}}% dos candidatos automatizados, testes de integração, de sistema e não funcionais em cinco categorias, métricas interpretadas, um ciclo completo de TDD e um pipeline de CI/CD com falha e correção demonstradas, além da análise estática com SonarQube.

Tabela: Critérios de saída do plano de testes e situação final

| Critério de saída (P03, seção 13) | Situação |
|---|---|
| 100% dos casos executados ou com justificativa | Atendido: os não executados e o bloqueado têm justificativa registrada |
| Todos os requisitos com ao menos um teste executado | Parcial: {{V:REQ_EXEC}}/{{V:REQ_TOTAL}} ({{V:REQ_SEM}} pendentes) |
| Nenhum defeito Crítico ou Alto aberto | Atendido: nenhum defeito aberto |
| Defeitos corrigidos com reteste e regressão | Não se aplica: nenhum defeito registrado; regressão completa feita após a mudança de versão |
| Suítes automatizadas aprovadas no pipeline | Atendido: execução 44441467718 e regressão da versão 1.2.0 |
| Mínimos do manual e 8 métricas com dados reais | Atendido |

**Prontidão do sistema.** Dentro do escopo testado, o BarberAgenda 1.2.0 atende aos {{V:REQ_EXEC}} requisitos com teste executado, sem defeitos observados e com todas as suítes automatizadas aprovadas no pipeline. O sistema está **apto para uso em ambiente de demonstração**. Para uso real, o critério de saída ainda não está completo: faltam a aceitação e a usabilidade com pessoas externas e a execução do CT-036 em horário comercial.

**Recomendação.** Executar primeiro as ações M-01 (aceitação e usabilidade) e M-02 (CT-036); em seguida, M-04 (limite de tentativas na consulta) e M-03 (segurança do CSRF); depois, recalcular as métricas e rodar a regressão completa pelo pipeline. Com esses itens concluídos, o sistema atende a todos os critérios de saída do plano.

# REFERÊNCIAS

GITHUB. **GitHub Actions documentation**. Disponível em: https://docs.github.com/actions. Acesso em: 18 nov. 2026.

INTERNATIONAL SOFTWARE TESTING QUALIFICATIONS BOARD. **Certified Tester Foundation Level Syllabus**. Versão 4.0. ISTQB, 2023.

ISO/IEC. **ISO/IEC 25010**: systems and software engineering – product quality model. Geneva: ISO, 2023.

JACOCO. **JaCoCo Java Code Coverage Library documentation**. Disponível em: https://www.jacoco.org/jacoco/. Acesso em: 18 nov. 2026.

JUNIT. **JUnit 5 User Guide**. Disponível em: https://junit.org/junit5/docs/current/user-guide/. Acesso em: 18 nov. 2026.

POSTMAN. **Newman: command-line collection runner**. Disponível em: https://learning.postman.com/docs/collections/using-newman-cli/. Acesso em: 18 nov. 2026.

SELENIUM. **Selenium WebDriver documentation**. Disponível em: https://www.selenium.dev/documentation/webdriver/. Acesso em: 18 nov. 2026.

SILVA, E. G. da. **Projeto Integrado P2**: planejamento, execução e avaliação da qualidade de um sistema de software – manual completo de desenvolvimento e entrega. Bauru: UNISAGRADO, 2026. Material da disciplina Testes e Qualidade de Software.

SONARSOURCE. **SonarQube Community Build documentation**. Disponível em: https://docs.sonarsource.com/sonarqube-community-build/. Acesso em: 18 nov. 2026.

SPRING. **Spring Boot reference documentation** (versão 3.5). Disponível em: https://docs.spring.io/spring-boot/. Acesso em: 18 nov. 2026.

# APÊNDICE A – CATÁLOGO COMPLETO DOS CASOS DE TESTE

Cada caso segue o modelo do Apêndice E do manual. O campo "Último resultado" considera a execução mais recente do caso. Fonte: `dados/casos.json` (o mesmo conteúdo do P04).

{{CATALOGO}}

# APÊNDICE B – REGISTRO DE EXECUÇÃO

Registro de todas as {{V:EXEC_REG}} execuções, no modelo do Apêndice F do manual, na ordem em que foram feitas: EX-001 a EX-007 são os testes não funcionais; EX-008 a EX-042, o ciclo principal dos casos manuais na versão 1.1.0, em 18/11/2026; EX-043 a EX-046, as reexecuções na versão 1.2.0, no mesmo dia. O título de cada caso está no Apêndice A, e as evidências seguem o padrão `EX-NNN_CT-NNN_AAAA-MM-DD` (`.txt` com a transcrição e `.png` com as capturas de tela). A coluna "Resultado obtido" reproduz as linhas de verificação da transcrição de cada execução (✓ quando o obtido confere com o esperado); as requisições e respostas completas estão nos arquivos de evidência, na pasta `05_EXECUCAO_MANUAL/evidencias/` (casos manuais) ou `10_ACEITACAO_NAO_FUNCIONAIS/evidencias/` (não funcionais). Todas as execuções foram feitas por Claude (IA) a pedido do grupo – por script ou teste automatizado (EX-001 a EX-007) ou por execução assistida por script (EX-008 a EX-046).

Tabela: Registro de todas as execuções (modelo do Apêndice F do manual)

{{APENDICE_EXECUCOES}}

# APÊNDICE C – RELATÓRIOS DE DEFEITO E ACHADOS

## C.1 Defeitos da execução

Nenhum defeito foi observado na execução dos casos de teste; por isso, não há relatório de defeito no modelo do Apêndice G do manual. O repositório tem o modelo pronto (`.github/ISSUE_TEMPLATE/defeito.md`), com os campos: requisito, caso, execução, ambiente e versão, responsável, pré-condições, dados, passos para reproduzir, resultado esperado, resultado obtido, evidências, severidade, prioridade, reteste e conclusão; e as etiquetas `defeito`, `severidade:*`, `prioridade:*` e `status:*`.

## C.2 Achados antes da execução

Os problemas abaixo foram encontrados por técnicas estáticas, antes da execução dos casos, e corrigidos. Eles são registrados aqui para que o histórico de qualidade fique completo, mas não entram nas métricas de defeitos, que se referem à execução dos testes.

Quadro: A-01 – Rota de restauração dos dados sem autenticação

| Campo | Conteúdo |
|---|---|
| Versão afetada | 1.0.0 (tag `v1.0-sistema-base`) |
| Como foi encontrado | Revisão de segurança do código, antes do início dos testes |
| Descrição | A rota `POST /api/dev/reset`, que apaga e recria os dados fictícios, podia ser chamada sem autenticação |
| Impacto | Qualquer pessoa poderia apagar todos os agendamentos; severidade equivalente a Crítica |
| Correção | Versão 1.0.1 (tag `v1.0.1-sistema-base`): a rota exige o perfil de administrador |
| Verificação | TNF-02 (rota incluída nas 14 rotas restritas, recusada sem credencial e com senha errada) |

Quadro: A-02 – Consulta de agendamento pelo número sequencial

| Campo | Conteúdo |
|---|---|
| Versão afetada | 1.0.0 e 1.0.1 |
| Como foi encontrado | Revisão de segurança do código, antes do início dos testes |
| Descrição | A consulta pelo cliente usava o número do agendamento, que é sequencial; trocando o número, era possível tentar ver o agendamento de outra pessoa |
| Impacto | Exposição de dados pessoais (risco R-07); severidade equivalente a Alta |
| Correção | Versão 1.1.0 (tag `v1.1.0-sistema-base`): código de acesso aleatório de 8 caracteres, exigido junto com o e-mail |
| Verificação | CT-023 e CT-024 (inclusive com número sequencial no lugar do código); Newman, pasta 04 |

Quadro: A-03 e A-04 – Alertas de bug do SonarQube (`java:S8696`)

| Campo | Conteúdo |
|---|---|
| Versão afetada | 1.1.0 (código de produção) e código de teste (`TesteE2EBase`) |
| Como foi encontrado | SonarQube: 1ª análise (linha de base) e análise intermediária |
| Descrição | Comparação de `getDayOfWeek()` com `DayOfWeek.SUNDAY` usando `==` |
| Impacto | Nenhum na prática: como `DayOfWeek` é enum, o `==` funcionava (falso positivo da regra) |
| Correção | Comparação reescrita com `equals()` na versão 1.2.0 |
| Verificação | Regressão completa aprovada; análise final com 0 bugs |

Quadro: A-05 – Vulnerabilidades do SonarQube mantidas como decisão de projeto

| Campo | Conteúdo |
|---|---|
| Regras | `java:S3330` (cookie `XSRF-TOKEN` sem `HttpOnly`) e `java:S4502` (proteção CSRF restrita) |
| Situação | Mantidas, com justificativa: o JavaScript precisa ler o cookie para enviar o token CSRF, e a proteção é exigida nas alterações feitas com sessão |
| Ação | M-03: aplicar `SameSite=Strict` e verificação de origem, ou registrar a aceitação formal do risco na ferramenta |

# APÊNDICE D – MATRIZ DE RASTREABILIDADE

Matriz completa no modelo do Apêndice H do manual: requisito → riscos → caso → última execução → resultado → defeito. A mesma matriz, com fórmulas, está na aba Rastreabilidade da planilha P05.

Tabela: Matriz de rastreabilidade completa

{{MATRIZ}}

# APÊNDICE E – REGISTROS DOS TESTES DE ACEITAÇÃO E NÃO FUNCIONAIS

## E.1 Cenários de aceitação

Os campos de resultado e decisão serão preenchidos com a execução real pela pessoa externa ao grupo.

{{ACEITACAO_REGISTROS}}

## E.2 Testes não funcionais

{{NF_REGISTROS}}

# APÊNDICE F – TESTES AUTOMATIZADOS

## F.1 Testes de unidade e integração (JUnit 5)

Tabela: Lista dos testes JUnit (código em `src/test/java/br/com/barberagenda/unit` e `integration`)

{{TESTES_JUNIT}}

## F.2 Requisições da coleção do Postman

Tabela: Requisições e asserções da coleção do Postman

{{POSTMAN_LISTA}}

## F.3 Testes de interface (Selenium)

Tabela: Lista dos testes Selenium (código em `src/test/java/br/com/barberagenda/e2e`)

{{TESTES_SELENIUM}}

# APÊNDICE G – REGISTRO DE TDD E CI/CD

Registro no modelo do Apêndice J do manual. As saídas completas do `./mvnw test` em cada etapa estão em `entrega/12_TDD_CICD_MELHORIA/tdd/`, e o trecho do log da execução com falha, em `entrega/12_TDD_CICD_MELHORIA/cicd/`.

Tabela: Registro de TDD e CI/CD

{{REGISTRO_TDD}}

# APÊNDICE H – PENDÊNCIAS E COMO CONCLUÍ-LAS

Itens que dependem de pessoas ou de condições que não estavam disponíveis e que o grupo precisa concluir. Depois de cada um, as execuções são lançadas em `dados/execucoes.csv` e os scripts regeneram a planilha, as métricas e este relatório.

Tabela: Pendências

| Pendência | Por que não foi feita | Como concluir |
|---|---|---|
| Aceitação (CA-01 a CA-04) | Exige pessoa externa ao grupo | Aplicar os cenários do Apêndice E.1 com um colega de outro grupo ou um cliente de barbearia; registrar a decisão de cada cenário |
| Usabilidade (TNF-08) | Exige participante externo | Aplicar o roteiro e o questionário do P09; registrar tempo, ajuda necessária e nota |
| CT-036 | Exige horário comercial (agendamento para menos de 2 horas à frente) | Executar entre 09:00 e 16:30 e registrar como nova execução |
| Representante do usuário no plano (P03) | Depende da pessoa escolhida para a aceitação | Registrar o nome e o papel no P03, seção 10 |
| Vídeo de contingência | Gravação pelos integrantes | Gravar até 5 minutos seguindo o roteiro do P13 |
| Diário de participação (P14) | Deve refletir a participação real | Preencher responsável, colaboradores, tempo e evidência de cada atividade |
| Assinaturas | Ação dos integrantes | Assinar a declaração do Apêndice J e o comprovante de entrega |
| Acesso ao repositório | Decisão do grupo | Tornar o repositório público ou adicionar o professor como colaborador; testar os links em janela anônima |
| Pasta no Drive | Entrega oficial | Copiar `entrega/` para `P2_TQS_2026_A_GRUPO_GUILHERME_JOSEPAULO_BARBERAGENDA` e liberar visualização |

# APÊNDICE I – INVENTÁRIO DE EVIDÊNCIAS

Arquivos da pasta de entrega (`entrega/`), que espelha as pastas obrigatórias do Drive. Contagem feita pelo script no momento da geração deste relatório.

Tabela: Inventário de evidências por pasta

{{INVENTARIO}}

Também fazem parte da entrega: o código-fonte e os testes no repositório (tags `v1.2.0-sistema` e `entrega-final`), a coleção e o ambiente do Postman em JSON, a planilha `P05_Matriz_Rastreabilidade.xlsx` e os artefatos de cada execução do pipeline no GitHub Actions.

# APÊNDICE J – DECLARAÇÃO FINAL DO GRUPO

Declaramos que os arquivos entregues representam o trabalho efetivamente realizado pelo grupo, que as execuções e as métricas são reais, que os dados utilizados são fictícios e que respeitamos as autorizações, as licenças e as orientações da disciplina, inclusive quanto ao uso de inteligência artificial.

::: {custom-style="Assinatura"}
______________________________________  Data: ____/____/2026
:::

::: {custom-style="AssinaturaNome"}
Guilherme Ribeiro Zangrande (RA 23110757)
:::

::: {custom-style="Assinatura"}
______________________________________  Data: ____/____/2026
:::

::: {custom-style="AssinaturaNome"}
José Paulo Dassie Felippi (RA 24111563)
:::
