# Roteiro de fala – Apresentação da P2 (BarberAgenda)

**Guilherme Ribeiro Zangrande (G)** e **José Paulo Dassie Felippi (J)** · Turma A · 13 slides (`P13_Apresentacao.pptx`) · 12 a 15 minutos + até 5 minutos de perguntas.

O manual (seção 13.2) pede que **os dois falem e respondam perguntas** e que a apresentação **não seja leitura dos slides**. Use o texto abaixo para ensaiar e depois fale com as suas palavras: o que importa são os números e a ordem das ideias. As partes marcadas como **Na tela** são o que fazer no computador enquanto fala.

## Divisão e tempo

| Slide | Assunto (item do manual, seção 13.1) | Quem fala | Início | Duração |
|-----|------------------------------|-----------|------|-------|
| 1 | Abertura (item 1) | Guilherme | 0:00 | 0:45 |
| 2 | O sistema (item 1) | Guilherme | 0:45 | 0:45 |
| 3 | Como foi construído (item 1) | Guilherme | 1:30 | 0:45 |
| 4 | Riscos (item 2) | José Paulo | 2:15 | 1:00 |
| 5 | Estratégia: pirâmide de testes (item 2) | José Paulo | 3:15 | 0:45 |
| 6 | Caso manual, evidência e defeito (item 3) | José Paulo | 4:00 | 1:30 |
| 7 | Automação + **demonstração ao vivo** (item 4) | Guilherme | 5:30 | 3:00 |
| 8 | Não funcionais e aceitação (item 5) | José Paulo | 8:30 | 1:00 |
| 9 | Métricas (item 5) | José Paulo | 9:30 | 1:00 |
| 10 | TDD + **demonstração** (item 6) | Guilherme | 10:30 | 1:00 |
| 11 | Pipeline CI/CD + **demonstração** (item 6) | Guilherme | 11:30 | 1:00 |
| 12 | Qualidade do código – SonarQube (item 7) | José Paulo | 12:30 | 0:45 |
| 13 | Conclusão e melhorias (item 7) | José Paulo | 13:15 | 1:00 |

Cada um fala cerca de 7 minutos. Quem não está falando cuida do computador: passa os slides e prepara a próxima demonstração.

## Antes de começar (10 minutos antes)

::: acao
**Na tela – preparar tudo antes de ser chamado:**

1. Abrir o PowerShell na pasta do projeto e garantir o Java 21: `$env:JAVA_HOME = 'C:\Program Files\Eclipse Adoptium\jdk-21.0.13.9-hotspot'` (no computador da faculdade, usar o caminho do Java 21 instalado ou a pasta `java21` do pendrive).
2. **Terminal 1** (deixar rodando): `java -jar target\barberagenda-1.2.0.jar --spring.profiles.active=test`
3. **Terminal 2**: vazio, na pasta do projeto, para as demonstrações.
4. Navegador com as abas: `http://localhost:8080` · GitHub Actions do repositório · `entrega/05_EXECUCAO_MANUAL/evidencias/EX-012_CT-012_2026-11-18.txt` · `entrega/12_TDD_CICD_MELHORIA/tdd/01_RED_mvnw_test.log`.
5. Slides abertos no PowerPoint, no modo de apresentação.
6. Vídeo de contingência e PDF dos slides no pendrive, caso algo falhe.
:::

## Slide 1 – Abertura · Guilherme · 0:00

::: {.fala .g}
**Guilherme:** Bom dia, professor e turma. Eu sou o Guilherme, este é o José Paulo, e somos da turma A. O nosso projeto foi planejar, executar e avaliar os testes do BarberAgenda, um sistema web de agendamento de barbearia que nós mesmos construímos para a disciplina e que o senhor aprovou em 19 de novembro. Vamos mostrar como decidimos o que testar, como executamos, o que automatizamos e o que os números dizem sobre a qualidade do sistema. Eu começo pelo sistema, e depois a gente vai alternando.
:::

## Slide 2 – O sistema · Guilherme · 0:45

::: {.fala .g}
**Guilherme:** O cliente não precisa de login. Ele se cadastra, escolhe barbeiro, serviço, data e um horário livre – o sistema só mostra os horários que realmente estão livres – e no final recebe um código de acesso de 8 caracteres. Com esse código e o e-mail, ele consulta ou cancela o agendamento. O dono da barbearia entra numa área administrativa com usuário e senha, onde cadastra barbeiros e serviços e vê a agenda do dia. As regras que mais importam para os testes são: funcionamento de segunda a sábado, das 9 às 19; horários de 30 em 30 minutos; até 30 dias de antecedência; nenhum barbeiro com dois clientes ao mesmo tempo; e no máximo 3 agendamentos ativos por cliente.
:::

::: acao
**Na tela (opcional, 15 segundos):** mostrar `http://localhost:8080` e clicar em "Agendar horário".
:::

## Slide 3 – Como foi construído · Guilherme · 1:30

::: {.fala .g}
**Guilherme:** O sistema é em Java 21 com Spring Boot. A tela, em HTML e JavaScript, chama uma API REST que troca dados em JSON. Dentro da API há três camadas: os controllers recebem a requisição, os services aplicam as regras de negócio e os repositories gravam no banco H2. Um detalhe que pesou muito nos testes: toda regra que depende de data e hora recebe o "agora" de um relógio que a gente consegue fixar. Assim, um teste sobre "até 30 dias" dá o mesmo resultado em qualquer dia. E todo erro volta no mesmo formato, sem mostrar detalhes internos do sistema. Agora o José Paulo explica como decidimos o que testar.
:::

## Slide 4 – Riscos · José Paulo · 2:15

::: {.fala .j}
**José Paulo:** Antes de escrever qualquer teste, listamos 12 riscos do produto e classificamos cada um por probabilidade e impacto. No mapa, quanto mais para cima e para a direita, mais urgente. Três ficaram com prioridade alta: dois clientes no mesmo horário com o mesmo barbeiro; um agendamento aceito fora do expediente ou fora dos intervalos de 30 minutos; e alguém acessando a área administrativa ou os dados dos clientes sem login. Esses três foram testados primeiro, em mais de um nível, e entram em todas as regressões. Nenhum deles se confirmou nos testes.
:::

## Slide 5 – Estratégia: pirâmide de testes · José Paulo · 3:15

::: {.fala .j}
**José Paulo:** A estratégia segue a pirâmide de testes. Na base ficam muitos testes de unidade, rápidos, em cima das regras de negócio: são 58. No meio, os testes de API com Postman e Newman: 26 requisições com 63 verificações. No topo, poucos testes de interface com Selenium, que são mais lentos: 11. Além deles, temos os 36 casos de teste manuais. Duas decisões ajudaram muito: o relógio fixo nos testes de data, e os dados fictícios, que restauramos com um comando antes de cada rodada, para todo teste começar do mesmo ponto.
:::

## Slide 6 – Caso manual, evidência e defeito · José Paulo · 4:00

::: {.fala .j}
**José Paulo:** Especificamos 36 casos de teste, cada um ligado a um requisito e a um risco, usando particionamento de equivalência, valor limite, transição de estados e tabela de decisão. Um exemplo é o CT-012, do horário de funcionamento: o sistema abre às 9 e o serviço tem que terminar até as 19. Então testamos exatamente nas fronteiras. Um corte às 8h30 tem que ser recusado. Um serviço de uma hora às 18h30 também, porque terminaria às 19h30. E às 18h00 tem que ser aceito, porque termina às 19 em ponto. Os três deram o resultado esperado, e a evidência é este arquivo, com cada requisição, a resposta e a verificação.
:::

::: acao
**Na tela:** abrir `EX-012_CT-012_2026-11-18.txt` e apontar as três linhas `[OK]` (400, 400 e 201).
:::

::: {.fala .j}
**José Paulo:** Dos 36 casos, 35 foram aprovados e 1 ficou bloqueado, o CT-036, porque ele precisa de horário comercial e foi executado às 23 horas. Defeito na execução: nenhum, e a gente não inventou defeito para ter o que mostrar. O problema mais relevante foi encontrado antes, revisando o código: na primeira versão, a consulta usava o número do agendamento, que é sequencial, então dava para trocar o número e tentar ver o agendamento de outra pessoa. Corrigimos com o código aleatório de 8 caracteres junto com o e-mail, e o CT-024 confirma que isso continua funcionando. Agora o Guilherme mostra a automação rodando.
:::

## Slide 7 – Automação e demonstração ao vivo · Guilherme · 5:30

::: {.fala .g}
**Guilherme:** Toda essa automação roda com um comando. Vou mostrar ao vivo.
:::

::: acao
**Na tela – terminal 2:** `.\mvnw.cmd test` (cerca de 30 segundos). Falar enquanto roda.
:::

::: {.fala .g}
**Guilherme:** Aqui rodam os testes de unidade, com JUnit e Mockito, e os de integração. Cada teste tem no nome o caso e o requisito que cobre, então dá para ir do teste até o requisito. Os testes de valor limite são parametrizados: o mesmo teste roda com 8h30, 9h00 e assim por diante. … Pronto: 58 testes, nenhuma falha. Agora a API.
:::

::: acao
**Na tela – terminal 2:** `newman run postman\BarberAgenda.postman_collection.json -e postman\BarberAgenda.postman_environment.json`
:::

::: {.fala .g}
**Guilherme:** A coleção do Postman faz um fluxo encadeado: cadastra um cliente, agenda para ele e usa o código que voltou para consultar e cancelar. O dado de uma requisição passa para a próxima. Cada operação importante tem um caso que deve funcionar e um que deve ser recusado, e no final os dados são restaurados. Resultado: 26 requisições, 63 verificações, zero falhas.
:::

::: acao
**Se houver tempo (1 minuto):** `.\mvnw.cmd test -Pe2e -Dtest=AgendamentoE2ETest -Dheadless=false`. O navegador abre e agenda sozinho. **Se algo falhar:** mostrar os relatórios já gerados em `entrega/07_AUTOMACAO_UNITARIA/surefire/` e `entrega/08_INTEGRACAO_API/relatorios/newman_2026-11-18.html`.
:::

::: {.fala .g}
**Guilherme:** O Selenium abre o navegador e faz o agendamento sozinho. Cada tela tem uma classe, que é o padrão Page Object, e o teste espera os elementos aparecerem em vez de usar tempos fixos. Agora o José Paulo mostra os testes não funcionais e as métricas.
:::

## Slide 8 – Não funcionais e aceitação · José Paulo · 8:30

::: {.fala .j}
**José Paulo:** Fizemos 8 testes não funcionais em 5 categorias. Desempenho: medimos 30 vezes cada operação principal, e o percentil 95 ficou em 34 milissegundos, contra um critério de 500. Segurança: chamamos 14 rotas restritas sem login e com senha errada, 28 tentativas, todas recusadas sem devolver dados. A senha do administrador fica guardada só como hash, e um código HTML digitado no nome aparece como texto, sem ser executado. Confiabilidade: os dados continuam lá depois de reiniciar o sistema, e 16 tipos de entrada inválida nunca derrubaram o servidor. Compatibilidade: a suíte do Selenium passou no Chrome e no Firefox, em tela de computador e de celular, 44 de 44 execuções – são essas duas telas.
:::

::: {.fala .j}
**José Paulo:** A aceitação e o teste de usabilidade precisam de uma pessoa de fora do grupo. **[AJUSTAR ANTES DA AULA – se já foram feitos:]** "Fizemos com [nome], que conseguiu agendar sozinho em [tempo] e deu nota [nota]; os quatro cenários foram aceitos." **[Se ainda não:]** "Os cenários e o questionário estão prontos, e essa é a primeira ação do nosso plano de melhoria."
:::

## Slide 9 – Métricas · José Paulo · 9:30

::: {.fala .j}
**José Paulo:** As 8 métricas do manual foram calculadas com os dados reais. Executamos 87,5% do que foi planejado, 42 de 48; o que falta são as 5 atividades com pessoa externa e o CT-036. A taxa de aprovação foi de 100%. Isso não quer dizer que o sistema não tem defeitos: quer dizer que, com as técnicas que aplicamos, nenhuma falha apareceu, e os problemas mais sérios foram encontrados antes, por revisão de código e análise estática. A cobertura de requisitos é de 85,7%, 12 de 14 requisitos com teste executado, e 100% do que planejamos automatizar está automatizado. Agora o Guilherme mostra o TDD e o pipeline.
:::

## Slide 10 – TDD · Guilherme · 10:30

::: {.fala .g}
**Guilherme:** Para o TDD, criamos uma regra que não existia: o cliente só pode cancelar com pelo menos 2 horas de antecedência; com menos, o sistema responde 422 com uma mensagem explicativa. Primeiro escrevemos os testes – 1h59 antes tem que ser recusado, exatamente 2 horas tem que ser aceito – e rodamos. Eles falharam pelo motivo certo, porque a regra ainda não existia: o teste esperava 422 e recebeu 200.
:::

::: acao
**Na tela:** abrir `01_RED_mvnw_test.log` e mostrar `Status expected:<422> but was:<200>`. No terminal 2: `git log --oneline -3 78b44e3` (mostra os três commits: RED `35ce2a2`, GREEN `c9c6e4c`, REFACTOR `78b44e3`).
:::

::: {.fala .g}
**Guilherme:** Depois escrevemos o código mínimo para o teste passar, que é o GREEN. Por fim, organizamos a regra numa classe própria, a PoliticaCancelamento, e todos os testes continuaram verdes, que é o REFACTOR. São três commits separados no GitHub, um para cada etapa.
:::

## Slide 11 – Pipeline CI/CD · Guilherme · 11:30

::: acao
**Na tela:** aba do GitHub Actions; abrir as execuções 44441467718, 44441895872 e 44442093641.
:::

::: {.fala .g}
**Guilherme:** O pipeline do GitHub Actions roda tudo a cada envio de código, em três etapas: primeiro os testes de unidade com a cobertura, depois a API e a interface. Esta execução está verde. Nesta outra, criamos de propósito uma branch com um teste alterado, esperando 20 horários em vez de 19: o pipeline falhou, e as etapas seguintes nem rodaram. É isso que impede uma mudança quebrada de entrar no projeto. Desfizemos a alteração e o pipeline voltou a ficar verde. Para fechar, o José Paulo.
:::

## Slide 12 – Qualidade do código · José Paulo · 12:30

::: {.fala .j}
**José Paulo:** Também analisamos o código com o SonarQube, duas vezes: antes e depois das correções. Os bugs foram de 3 para 0 e a cobertura subiu de 38,9% para 72,3%, porque os testes de integração passaram a exercitar partes que a unidade não alcança. Ficaram 2 alertas de segurança ligados à proteção CSRF, que são decisões de projeto justificadas e estão no plano de melhoria.
:::

## Slide 13 – Conclusão · José Paulo · 13:15

::: {.fala .j}
**José Paulo:** Concluindo: dentro do escopo, o BarberAgenda está pronto para demonstração. Todos os testes executados passaram e o pipeline está verde. Para uso real ainda faltam a aceitação com usuários de verdade, executar o CT-036 em horário comercial e duas melhorias de segurança: limitar as tentativas na consulta pelo código e reforçar a proteção CSRF. A principal lição foi que o teste estático e o dinâmico se completam: a revisão de código e o SonarQube encontraram problemas que a execução dos casos não encontraria. Obrigado. Ficamos à disposição para perguntas.
:::

## Perguntas prováveis – quem responde

Respondam com calma e com as suas palavras. Se a pergunta for do outro, passem a palavra: "O Guilherme fez essa parte, ele explica melhor."

| Pergunta | Quem | Resposta curta |
|----------------|-----|------------------------------|
| Como foi a implementação da API e quais linguagens vocês usaram? | G | Java 21 com Spring Boot. A API é REST e troca JSON; a tela é HTML, CSS e JavaScript; o banco é o H2; o build é com Maven. Três camadas: controller, service e repository. |
| Por que nenhum defeito e 100% de aprovação? | J | O sistema é pequeno e os problemas sérios foram achados antes, na revisão de código e no SonarQube, e corrigidos. Não inventamos defeito; 100% significa que, com as técnicas aplicadas, nenhuma falha apareceu, e por isso a aceitação com pessoa externa é importante. |
| Vocês executaram os casos manuais à mão? | J | A execução foi assistida por um script, feito com IA a pedido do grupo e registrado como tal: ele segue exatamente os passos do catálogo, guarda cada resposta e tira as capturas. Qualquer caso pode ser repetido à mão agora, se o senhor quiser. |
| Qual a diferença entre partição de equivalência e valor limite? | J | Partição divide as entradas em grupos que o sistema trata do mesmo jeito (nome válido de 3 a 60, inválido abaixo ou acima). Valor limite testa as bordas desses grupos: 2, 3, 60 e 61 caracteres. |
| Por que o CT-036 está bloqueado e não reprovado? | J | Ele precisa criar um agendamento para daqui a menos de 2 horas, dentro do expediente. Às 23h isso é impossível, então o caso não pôde rodar, e o sistema não falhou. A regra está coberta pelos testes automáticos com relógio fixo. |
| Por que 422 e não 400 no cancelamento? | G | 400 é um pedido mal formado. 422 é um pedido válido que a regra de negócio recusa naquele momento: o cancelamento está certo, só está fora do prazo. |
| Para que serve o relógio fixo? | G | Para os testes de data darem o mesmo resultado em qualquer dia e hora. Sem ele, um teste de "30 dias" ou "2 horas" mudaria de resultado conforme o dia. |
| O que é Page Object e espera explícita? | G | Page Object é uma classe por tela, com os campos e ações dela, para o teste não repetir localizadores. Espera explícita é aguardar o elemento aparecer, em vez de esperar um tempo fixo. |
| O que mostra a falha do pipeline? | G | Foi proposital: mudamos um teste numa branch separada e o pipeline barrou. Mostra que uma mudança que quebra um teste não passa. Não é defeito do sistema. |
| Como os testes começam sempre do mesmo ponto? | J | Os dados são fictícios e restaurados por um comando (`reset-dados`) antes de cada rodada; os testes que criam dados usam e-mails únicos. |
| Por que as 2 vulnerabilidades do SonarQube ficaram? | J | O cookie do CSRF precisa ser lido pelo JavaScript para enviar o token, e a proteção é exigida onde há sessão. Está justificado e é a melhoria M-03. |
| Como foi o uso de IA? | G e J | Usamos o Claude Code com autorização do senhor, para construir o sistema, os scripts, os documentos e a execução assistida, tudo declarado no relatório. Todos os resultados são de execuções reais, e nós entendemos e explicamos cada parte. |

## Se algo der errado (plano B)

| Problema | O que fazer |
|-----------|----------------------|
| Sem internet | Usar o PDF dos slides e os arquivos locais: logs em `entrega/12_TDD_CICD_MELHORIA/` e `cicd/execucoes_pipeline.md`. |
| O sistema não sobe | Mostrar as capturas em `entrega/09_SISTEMA_INTERFACE/capturas/` e `entrega/01_SISTEMA_ALVO/`. |
| Um teste demora ou trava | Interromper (`Ctrl+C`) e mostrar o relatório já gerado em `entrega/07_AUTOMACAO_UNITARIA/surefire/` ou `entrega/08_INTEGRACAO_API/relatorios/`. |
| O computador da sala não funciona | Rodar o vídeo de contingência a partir do pendrive. |
