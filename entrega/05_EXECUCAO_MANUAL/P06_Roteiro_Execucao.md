# P06 — Roteiro de execução manual

**Projeto Integrado P2 — BarberAgenda** — Turma A — Guilherme Ribeiro Zangrande e José Paulo Dassie Felippi

| Versão | Data | Descrição |
|---|---|---|
| v1.0 | 2026-11-18 | Roteiro para a execução manual dos 35 casos do P04 pelo grupo |

> **Quem executa:** os integrantes do grupo. O nome de quem executou cada caso vai no registro (coluna Executor). Registre somente o que foi realmente observado; se um caso não puder ser executado, registre "Bloqueado" ou "Não executado" com o motivo (manual, seções 9.6 e 15).

## 1. Antes de começar (critérios de entrada — P03, seção 12)

1. Atualizar o repositório e anotar a versão sob teste:
   ```bash
   git pull
   git describe --tags          # ex.: marco-3 ou v1.1.0-sistema-base-3-g446b5ce
   ```
2. Gerar o pacote e subir a aplicação no perfil `dev` (terminal separado, deixar aberto):
   ```bash
   ./mvnw -DskipTests package
   java -jar target/barberagenda-1.2.0.jar
   ```
3. Em outro terminal, confirmar que o sistema responde:
   ```bash
   bash scripts/verificar-sistema.sh     # deve terminar com "46/46 verificações OK"
   ```
4. Calcular as datas do dia e ver os ids de barbeiros e serviços:
   ```bash
   python scripts/datas_teste.py
   ```
   Anote DF1, DF2, DF3, ONTEM, DOM, D+30, D+31 e `<AAAAMMDD>`. Se o script avisar que D+30 cai em domingo, o CT-015 fica "Bloqueado" nesse dia.
5. Abrir o checklist `P06_Checklist_Execucao.md` (ordem: casos de prioridade Alta primeiro).

## 2. Executar cada caso

Para cada linha do checklist:

1. **Restaurar os dados** (obrigatório antes de cada caso):
   ```bash
   bash scripts/reset-dados.sh
   ```
   Se o caso usa ids da API, rode `python scripts/datas_teste.py` de novo (os ids mudam a cada restauração).
2. **Ler o caso no P04** (`entrega/04_CASOS_E_RASTREABILIDADE/P04_Catalogo_Casos_de_Teste.md`): pré-condições, dados, passos e resultado esperado.
3. **Executar os passos exatamente como escritos**, substituindo DF1, D+30 etc. pelas datas do dia.
4. **Comparar o obtido com o esperado** e classificar:

   | Resultado | Quando usar |
   |---|---|
   | Aprovado | Tudo o que está em "Resultado esperado" aconteceu |
   | Reprovado | Algo diferente do esperado aconteceu (mesmo que pequeno) → registrar defeito (seção 4) |
   | Bloqueado | Não foi possível executar por um impedimento externo ao caso (ex.: D+30 em domingo, aplicação fora do ar) — escrever o motivo |
   | Não executado | O caso não foi executado nesta rodada — escrever o motivo |

5. **Salvar a evidência** em `entrega/05_EXECUCAO_MANUAL/evidencias/` com o nome `EX-NNN_CT-NNN_AAAA-MM-DD.ext`:
   - **Tela:** captura da tela mostrando o resultado (mensagem, tabela ou status). Se o caso tem várias partes — (a), (b) etc. —, use um sufixo: `EX-003_CT-003_2026-11-20_a.png`.
   - **API:** salvar requisição e resposta em `.txt` (ver seção 3).

## 3. Casos executados pela API

Use o **Postman** (montando as requisições do P04) ou o **curl** do Git Bash. No Windows, envie o corpo JSON **por arquivo** (o curl do Git Bash corrompe acentos passados direto no comando).

Exemplo — CT-014 (domingo), com a data e os ids do dia:

```bash
cat > corpo.json <<'EOF'
{"emailCliente":"gabriela.teixeira@exemplo.com","barbeiroId":7,"servicoId":12,"dataHoraInicio":"2026-11-22T10:00:00"}
EOF
curl -i -s -H "Content-Type: application/json" --data-binary @corpo.json \
     http://localhost:8080/api/agendamentos | tee entrega/05_EXECUCAO_MANUAL/evidencias/EX-014_CT-014_2026-11-20.txt
```

Para rotas administrativas acrescente `-u admin:admin123` (credencial fictícia). Para consultas use `curl -i -s "http://localhost:8080/api/..."`. A opção `-i` grava o código HTTP (ex.: `HTTP/1.1 400`) junto com o corpo, o que serve de evidência.

## 4. Quando um caso falha (Reprovado)

1. **Confirmar que é defeito do sistema** (e não engano na execução): repetir os passos uma vez com cuidado.
2. **Registrar o defeito no GitHub Issues** com o modelo **Defeito** (https://github.com/ZangrandeG/barberagenda/issues/new/choose). Preencher todos os campos do Apêndice G: requisito, caso, execução, ambiente/versão, pré-condições, dados, passos, esperado × obtido, evidência anexada, responsável.
3. **Etiquetas:** uma de cada grupo — `severidade:baixa|media|alta|critica`, `prioridade:baixa|media|alta` e `status:novo`. Severidade e prioridade seguem o P03, seção 17.
4. Na linha da execução, coluna Defeito: `#N` (número da issue).
5. **Acompanhar o status** trocando a etiqueta: `status:novo` → `status:em-analise` → `status:em-correcao` → `status:pronto-para-reteste` → `status:encerrado` (fechar a issue). Se o reteste falhar: `status:reaberto` **e** a etiqueta permanente `historico:reaberto` (é ela que alimenta a taxa de reabertura).
6. **Depois da correção:**
   - **Reteste (confirmação):** executar de novo o mesmo caso e registrar como **nova execução** (novo EX-NNN, mesmo CT).
   - **Regressão:** reexecutar os outros casos do mesmo requisito com prioridade Alta (P04, seção 4.1) e registrar cada um como nova execução.
7. **Nunca** crie defeito sem falha real observada, nem altere evidências (manual, seção 9.7).

## 5. Registrar os resultados

Ao fim de cada sessão, acrescentar uma linha por execução em `dados/execucoes.csv`, na ordem em que aconteceram:

```csv
execucao,caso,data,versao,executor,resultado,evidencia,defeito,observacoes
EX-001,CT-007,2026-11-20,v1.1.0-sistema-base-3-g446b5ce,Nome do integrante,Aprovado,EX-001_CT-007_2026-11-20.png,,DF3=2026-11-24
```

Depois, regerar os documentos e exportar os defeitos:

```bash
python scripts/exportar_defeitos.py     # se houver defeitos: atualiza dados/defeitos.csv e entrega/06_DEFEITOS
python scripts/gerar_artefatos.py       # atualiza P06_Registro_Execucao.md, o checklist e a planilha P05
```

E registrar no Diário de Participação (P14) quem executou o quê, quanto tempo levou e a evidência.

## 6. Fim da rodada (critérios de saída do Marco 4)

- [ ] Todos os 35 casos com resultado registrado (ou justificativa de Bloqueado/Não executado).
- [ ] Toda reprovação com issue aberta e etiquetada.
- [ ] Defeitos corrigidos com reteste e regressão registrados como novas execuções.
- [ ] Evidências salvas com o nome padrão, uma por execução.
- [ ] `exportar_defeitos.py` e `gerar_artefatos.py` executados; P05 e P06 atualizados.
- [ ] Commit das evidências e dos CSV e tag `marco-4`.
