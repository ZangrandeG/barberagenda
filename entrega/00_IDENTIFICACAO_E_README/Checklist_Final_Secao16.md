# Checklist final do grupo (seção 16 do manual) — situação em 2026-11-18

Legenda: **OK** = pronto e verificado · **Parcial** = pronto com pendência indicada · **Grupo** = depende de ação dos integrantes, do professor ou de pessoa externa.

| # | Item da seção 16 | Situação | Evidência / o que falta |
|---|---|---|---|
| 1 | O sistema aprovado está executável e corresponde à versão informada | **Parcial** | BarberAgenda 1.2.0 (tag `v1.2.0-sistema`) compila, sobe e passa em todas as suítes; **falta a aprovação do professor** (P01) |
| 2 | O README permite instalar, configurar, executar e testar o projeto | **OK** | `README.md` (ordem da seção 11.4); cópia nesta pasta; clone limpo testado em 2026-11-18 |
| 3 | O escopo, requisitos e riscos estão identificados e rastreáveis | **OK** | P02 v1.1 (14 requisitos, 12 riscos); P05 abas Requisitos/Riscos/Rastreabilidade |
| 4 | O plano de testes está completo e atualizado | **Parcial** | P03 v1.1; **falta**: datas-limite do cronograma (data da P2) e confirmar papéis |
| 5 | Os casos manuais atendem às quantidades e às técnicas exigidas | **OK** | P04: 36 casos (mín. 24) com partições, limites, transição de estados e tabela de decisão |
| 6 | As execuções possuem resultados e evidências | **OK** | P06: 46 execuções com transcrição e capturas; CT-036 bloqueado (repetir em horário comercial) |
| 7 | Todos os defeitos encontrados estão registrados e vinculados | **OK** | Nenhum defeito observado na execução; processo e exportação prontos (P07) |
| 8 | Os testes unitários, integração/API e sistema/interface podem ser executados | **OK** | `./mvnw test`, Newman, `./mvnw test -Pe2e`; também no pipeline |
| 9 | As coleções, ambientes, dependências e configurações foram exportados | **OK** | `entrega/08_INTEGRACAO_API/*.json`, `pom.xml`, `.github/workflows/ci.yml` |
| 10 | Os testes de aceitação e não funcionais estão documentados | **Parcial** | P09: 7 não funcionais executados; **aceitação (4) e usabilidade dependem de pessoa externa** |
| 11 | As métricas foram calculadas com dados reais e interpretadas | **OK** | P10 + aba Métricas do P05 + gráficos |
| 12 | O ciclo de TDD possui evidências Red, Green e Refactor | **OK** | Commits `35ce2a2`, `c9c6e4c`, `78b44e3` e logs em `12_TDD_CICD_MELHORIA/tdd/` |
| 13 | O pipeline CI/CD possui execução documentada | **OK** | Runs 44441467718 (verde), 44441895872 (falha proposital), 44442093641 (correção) |
| 14 | A análise de qualidade possui linha de base e comparação final | **OK** | `sonar_baseline/`, `sonar_final/` e P11 seção 2 |
| 15 | O relatório final está em DOCX e PDF e corresponde aos arquivos técnicos | **Parcial** | `13_RELATORIO_FINAL/P12_Relatorio_Final.docx` e `.pdf` (PDF gerado do DOCX); **falta** número do grupo e assinaturas |
| 16 | A apresentação e o vídeo de contingência estão na pasta correta | **Parcial** | PPTX + PDF e roteiros em `14_APRESENTACAO_E_VIDEO_CONTINGENCIA/`; **falta gravar o vídeo** |
| 17 | O Diário de Participação está atualizado e coerente | **Grupo** | Linhas sugeridas em P14; **revisar e preencher responsáveis, colaboradores e tempo** |
| 18 | O Drive possui a estrutura obrigatória e todos os links funcionam | **Grupo** | `entrega/` tem as 17 pastas; **copiar para o Drive** na pasta `P2_TQS_2026_A_GRUPOXX_BARBERAGENDA` |
| 19 | As permissões foram testadas sem solicitar acesso | **Grupo** | O repositório está **privado**: tornar público ou dar acesso ao professor e testar em janela anônima |
| 20 | A entrega foi concluída antes do horário limite da P2 | **Grupo** | Data da P2 não informada |
