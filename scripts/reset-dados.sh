#!/usr/bin/env bash
# Restaura a massa de dados fictícios (somente perfis dev e test).
# Uso: bash scripts/reset-dados.sh [URL_BASE]
set -euo pipefail
BASE="${1:-http://localhost:8080}"
curl -sS -f -X POST "$BASE/api/dev/reset"
echo
