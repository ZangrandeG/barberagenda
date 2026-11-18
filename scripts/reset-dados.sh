#!/usr/bin/env bash
# Restaura a massa de dados fictícios (somente perfis dev e test; exige administrador).
# Uso: bash scripts/reset-dados.sh [URL_BASE]
# Credencial: variáveis ADMIN_LOGIN e ADMIN_SENHA (padrão fictício admin/admin123).
set -euo pipefail
BASE="${1:-http://localhost:8080}"
curl -sS -f -u "${ADMIN_LOGIN:-admin}:${ADMIN_SENHA:-admin123}" -X POST "$BASE/api/dev/reset"
echo
