# Marco 1 — Fundamentos: níveis, tipos e estratégia de teste

**Projeto Integrado P2 — Testes e Qualidade de Software — UNISAGRADO 2026**
**Sistema:** BarberAgenda 1.1.0 (tag `v1.1.0-sistema-base`)
**Grupo:** Turma A — Guilherme Ribeiro Zangrande (RA 23110757) e José Paulo Dassie Felippi (RA 24111563)

| Versão | Data | Descrição |
|---|---|---|
| v1.0 | 2026-11-18 | Classificação preliminar dos níveis e tipos de teste e justificativa da estratégia |

> Documento preliminar do Marco 1. O detalhamento (cronograma, critérios de entrada e saída, responsabilidades) será feito no Plano de Testes (P03, Marco 2). A base de teste é a especificação em `docs/ESPECIFICACAO_SISTEMA.md`.

## 1. Entregas do Marco 1

| Entrega esperada (manual, seção 7) | Onde está | Situação |
|---|---|---|
| Grupo definido | P01, campo Integrantes | Concluído |
| Duas opções de sistema | P01: BarberAgenda (preferida) e Spring PetClinic | Concluído — aguardando decisão do professor |
| Classificação preliminar dos níveis de teste | Seções 3 e 4 deste documento | Concluído |
| Justificativa da escolha | P01 (Justificativa da escolha) e seção 6 deste documento | Concluído |

## 2. O sistema visto pelos testes

O BarberAgenda é dividido em camadas. Cada nível de teste mira uma parte dessa cadeia:

```
 Navegador (HTML/JS)  →  API REST (controller)  →  Regras (service)  →  Banco (repository/JPA + H2)
 └── Sistema / Aceitação ──────────────────────────────────────────────────────────────────────┘
                          └── Integração / API ──────────────────────────────────────────────┘
                                                    └ Unidade ┘
 Spring Security (login, CSRF) atravessa a interface e a API → Integração, Sistema e Não funcional (segurança)
```

## 3. Níveis de teste aplicados

| Nível | O que verifica no BarberAgenda | Objeto de teste | Ferramenta | Execução | Mínimo do manual |
|---|---|---|---|---|---|
| **Unidade** | Cada regra isolada, sem banco, rede ou interface: horário de funcionamento, intervalo de 30 min, antecedência de 30 dias, sobreposição de horários, limite de 3 agendamentos ativos, validações de cliente e serviço. | `RegrasAgendamento`, `AgendamentoService`, `ClienteService`, validações dos DTOs | JUnit 5, AssertJ, Mockito; `Clock` fixo para controlar "agora" | Automatizada (`./mvnw test`) | 6 testes |
| **Integração** | Comunicação entre componentes: requisição HTTP → controller → service → banco → resposta JSON; códigos de status, contrato dos campos, mensagens de erro, segurança (401/403) e encadeamento (cadastrar → agendar → consultar → cancelar). | API REST com banco H2 real | Postman + Newman; complemento com `@SpringBootTest` + MockMvc | Automatizada | 5 testes |
| **Sistema** | Fluxos completos do usuário pela interface, como caixa-preta, comparando o resultado obtido com o esperado: cadastro, agendamento completo, consulta/cancelamento, login do administrador e cadastro de serviço. | Aplicação inteira no navegador | Execução manual (casos do P04) e Selenium WebDriver (Page Object, esperas explícitas) | Manual e automatizada | 24 casos manuais e 4 testes de interface |
| **Aceitação** | Se o sistema atende ao cliente da barbearia e ao dono, do ponto de vista deles: conseguir agendar sem ajuda, entender os erros, administrar a agenda do dia. | Aplicação inteira, cenários Dado/Quando/Então | Roteiro de aceitação | Manual, por **pessoa externa ao grupo** | 4 cenários |

## 4. Tipos de teste aplicados

| Tipo | Significado | Como aparece no BarberAgenda | Níveis |
|---|---|---|---|
| **Funcional** | Verifica **o que** o sistema faz, contra os requisitos. | Regras RN-01 a RN-11 e os 6 fluxos selecionados, com casos positivos, negativos, de fronteira e de exceção. | Todos |
| **Não funcional** | Verifica **como** o sistema se comporta. | Desempenho básico (tempo de resposta de `GET /api/horarios-disponiveis` e `POST /api/agendamentos`), segurança básica (acesso sem login, senha com hash, entrada com HTML/script, erros sem stack trace), compatibilidade (Chrome/Firefox, desktop e 375×667), confiabilidade (dados preservados após reinício) e usabilidade (tarefas com usuário). | Integração, Sistema, Aceitação — mínimo de 6 testes em 3 categorias |
| **Confirmação (reteste)** | Repete o caso que falhou, depois da correção, para confirmar que o defeito foi resolvido. | Cada defeito registrado no GitHub Issues terá uma nova execução do caso que o revelou (novo EX-xxx). | O nível em que a falha apareceu |
| **Regressão** | Repete testes que já passaram para garantir que uma alteração não quebrou o que funcionava. | Suítes automatizadas (unidade, API e interface) executadas após cada correção, após o ciclo de TDD e a cada `push`/pull request no pipeline de CI. | Unidade, Integração, Sistema |

**Teste estático (complemento).** Além dos testes dinâmicos acima, o código passa por análise estática com SonarQube (linha de base e análise final). Um exemplo real do valor dessa prática já ocorreu: em 2026-11-18, antes do início dos testes, uma revisão automatizada de segurança do código apontou dois problemas — a rota de restauração de dados sem autenticação e a consulta de agendamento por número sequencial — corrigidos nas versões 1.0.1 e 1.1.0 (ver `docs/PROGRESSO.md`).

## 5. Técnicas previstas (detalhadas no Marco 3)

| Técnica | Onde se aplica | Exemplo |
|---|---|---|
| Particionamento de equivalência | Toda regra com faixa ou formato | Telefone: só dígitos com 10–11 dígitos (válida); com letras; com 9 ou 12 dígitos (inválidas) |
| Análise de valor limite | Tamanhos, quantidades, horários e datas | Nome com 2/3/60/61 caracteres; início 08:30/09:00 e serviço terminando 19:00/19:30; antecedência de 30 e 31 dias; 3º e 4º agendamento ativo; duração 14/15/180/195 |
| Transição de estados | Status do agendamento | `AGENDADO` → `CANCELADO` / `CONCLUIDO`; tentar cancelar ou concluir de novo (409) |
| Teste baseado em experiência | Interface e segurança | Campos com espaços, acentos, HTML; uso em tela de celular |

## 6. Justificativa da estratégia

1. **Priorização por risco.** As regras de agendamento (RN-04 a RN-08) e o controle de acesso (RN-11) são os pontos em que uma falha causa mais prejuízo: dois clientes no mesmo horário, agendamento fora do expediente, dados pessoais expostos. Esses casos serão especificados e executados primeiro e repetidos após correções.
2. **Pirâmide de testes.** As regras ficam concentradas na camada de serviço, onde testes de unidade são rápidos, baratos e não dependem de banco. Por isso a base terá mais testes de unidade, menos testes de API e poucos testes de interface (Selenium só nos fluxos críticos, que são os mais lentos e frágeis de automatizar).
3. **Sistema com API REST própria.** Permite testar a integração com Postman/Newman de forma independente da interface, inclusive cenários negativos difíceis de produzir pela tela (corpo inválido, requisição sem login).
4. **Regras que dependem de data e hora.** O "agora" é obtido de um `Clock` injetável, que os testes de unidade fixam em uma data conhecida; a massa de dados usa datas relativas ao dia atual. Isso evita testes que passam hoje e falham amanhã.
5. **Repetibilidade.** Dados exclusivamente fictícios e a rota `POST /api/dev/reset` (perfis dev e test) restauram o ambiente entre execuções manuais e automatizadas.
6. **Visão do usuário.** Como o próprio grupo construiu o sistema, existe o risco de testar "o que foi feito" em vez de "o que deveria ser". Para reduzir esse viés, os casos serão derivados da especificação (caixa-preta), e a aceitação será executada por uma pessoa externa ao grupo.

## 7. Distribuição preliminar das regras por nível

| Regra | Unidade | Integração/API | Sistema (manual/Selenium) | Aceitação | Não funcional |
|---|:---:|:---:|:---:|:---:|:---:|
| RN-01 Nome do cliente | X | X | X | X | |
| RN-02 Telefone | X | X | X | | |
| RN-03 E-mail válido e único | X | X | X | | |
| RN-04 Horário de funcionamento | X | X | X | X | |
| RN-05 Intervalos de 30 min | X | X | X | | |
| RN-06 Passado e 30 dias | X | X | X | | |
| RN-07 Sem sobreposição | X | X | X | X | |
| RN-08 Limite de 3 ativos | X | X | X | | |
| RN-09 Duração e preço do serviço | X | X | X | | |
| RN-10 Somente ativos | X | X | X | | |
| RN-11 Área restrita | | X | X | X | X (segurança) |

A matriz definitiva, ligada a riscos, casos, execuções e defeitos, será a Matriz de Rastreabilidade (P05).

## 8. Limitações conhecidas desta estratégia

- O sistema foi construído pelo próprio grupo, com apoio de IA; espera-se um número pequeno de defeitos. Serão registrados apenas os defeitos reais encontrados (manual, seção 9.7).
- Os testes de desempenho são básicos (tempo de resposta em ambiente local, com repetições), sem teste de carga, conforme a seção 15 do manual.
- Os testes de segurança se limitam a validações, controle de acesso e exposição indevida, sem ataques.
- A aceitação depende da disponibilidade de uma pessoa externa: [PREENCHER PELO GRUPO — nome/papel do participante].
