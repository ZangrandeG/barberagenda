# Execuções do pipeline (GitHub Actions)

| Run | Branch / evento | Resultado | Jobs |
|---|---|---|---|
| [44441467718](https://github.com/ZangrandeG/barberagenda/actions/runs/44441467718) | `main` / push (inclusão do workflow) | Sucesso | testes ✓, api ✓, interface ✓ |
| [44441895872](https://github.com/ZangrandeG/barberagenda/actions/runs/44441895872) | `demo/falha-pipeline` / push (quebra proposital do teste do CT-007) | **Falha** (demonstração controlada) | testes ✗ (`Expected size: 20 but was: 19`), api e interface pulados |
| [44442093641](https://github.com/ZangrandeG/barberagenda/actions/runs/44442093641) | `demo/falha-pipeline` / push (correção) | Sucesso | testes ✓, api ✓, interface ✓ |

A quebra proposital é uma demonstração do pipeline exigida pelo manual (seção 9.15) e **não** é defeito do sistema.
