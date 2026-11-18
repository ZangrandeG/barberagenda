#!/usr/bin/env bash
# Verificação rápida de disponibilidade das funções do BarberAgenda (seção 9.1, item 3 do manual).
# NÃO substitui os casos de teste formais (P04) nem a coleção Postman (P08): apenas confirma que a
# versão base sobe e responde nos fluxos selecionados.
#
# Uso: aplicação rodando no perfil dev ou test; depois:  bash scripts/verificar-sistema.sh [URL_BASE]
# Requisitos: bash, curl e python (para ler JSON).

set -u
BASE="${1:-http://localhost:8080}"
ADMIN="admin:admin123"   # credencial FICTÍCIA de desenvolvimento
FALHAS=0
TOTAL=0
CORPO="$(mktemp)"

verificar() { # descricao status_esperado status_obtido
    TOTAL=$((TOTAL + 1))
    if [ "$2" = "$3" ]; then
        printf 'OK      %-70s esperado=%s obtido=%s\n' "$1" "$2" "$3"
    else
        FALHAS=$((FALHAS + 1))
        printf 'FALHOU  %-70s esperado=%s obtido=%s\n' "$1" "$2" "$3"
        printf '        corpo: %s\n' "$(head -c 300 "$CORPO")"
    fi
}

ENVIO="$(mktemp)"

chamar() { # metodo caminho [corpo_json] [credencial]
    local args=(-s -o "$CORPO" -w '%{http_code}' -X "$1" "$BASE$2" -H 'Accept: application/json')
    if [ -n "${3:-}" ]; then
        # O corpo vai por arquivo para preservar acentos (UTF-8) no curl do Windows.
        printf '%s' "$3" > "$ENVIO"
        args+=(-H 'Content-Type: application/json; charset=utf-8' --data-binary "@$ENVIO")
    fi
    [ -n "${4:-}" ] && args+=(-u "$4")
    curl "${args[@]}"
}

json() { # expressão python sobre a variável d
    python -c "import json,sys; d=json.load(open(sys.argv[1], encoding='utf-8')); print($1)" "$CORPO"
}

proximo_dia_util() { # n-ésimo dia de segunda a sábado a partir de amanhã
    python -c "
import datetime as dt, sys
n=int(sys.argv[1]); d=dt.date.today()
while n>0:
    d+=dt.timedelta(days=1)
    if d.weekday()!=6: n-=1
print(d.isoformat())" "$1"
}

proximo_domingo() {
    python -c "
import datetime as dt
d=dt.date.today()+dt.timedelta(days=1)
while d.weekday()!=6: d+=dt.timedelta(days=1)
print(d.isoformat())"
}

echo "== BarberAgenda — verificação da versão base em $BASE =="
echo "== $(date '+%Y-%m-%d %H:%M:%S') =="

verificar "POST /api/dev/reset restaura a massa fictícia" 200 "$(chamar POST /api/dev/reset)"

verificar "GET /api/barbeiros lista barbeiros ativos" 200 "$(chamar GET /api/barbeiros)"
BARBEIRO=$(json "d[0]['id']")
verificar "GET /api/servicos lista serviços ativos" 200 "$(chamar GET /api/servicos)"
SERVICO=$(json "[s['id'] for s in d if s['duracaoMinutos']==30][0]")

SUFIXO=$(date +%s)
EMAIL1="verificacao.${SUFIXO}@exemplo.com"
EMAIL2="verificacao2.${SUFIXO}@exemplo.com"
verificar "POST /api/clientes com dados válidos" 201 \
    "$(chamar POST /api/clientes "{\"nome\":\"Cliente Verificação\",\"telefone\":\"14988887777\",\"email\":\"$EMAIL1\"}")"
verificar "POST /api/clientes com e-mail repetido (RN-03)" 409 \
    "$(chamar POST /api/clientes "{\"nome\":\"Outro Nome\",\"telefone\":\"14988887777\",\"email\":\"$EMAIL1\"}")"
verificar "POST /api/clientes com nome de 2 caracteres (RN-01)" 400 \
    "$(chamar POST /api/clientes "{\"nome\":\"Al\",\"telefone\":\"14988887777\",\"email\":\"x.$EMAIL1\"}")"
verificar "  resposta 400 traz o campo 'nome' em 'campos'" "True" "$(json "'nome' in d['campos']")"
verificar "POST /api/clientes com telefone de 9 dígitos (RN-02)" 400 \
    "$(chamar POST /api/clientes "{\"nome\":\"Cliente Teste\",\"telefone\":\"149888877\",\"email\":\"y.$EMAIL1\"}")"
chamar POST /api/clientes "{\"nome\":\"Cliente Verificação Dois\",\"telefone\":\"1432221111\",\"email\":\"$EMAIL2\"}" >/dev/null

verificar "GET /api/clientes sem autenticação (dados pessoais)" 401 "$(chamar GET /api/clientes)"
verificar "GET /api/clientes como administrador (HTTP Basic)" 200 "$(chamar GET /api/clientes '' "$ADMIN")"

DIA=$(proximo_dia_util 2)
verificar "GET /api/horarios-disponiveis em $DIA" 200 \
    "$(chamar GET "/api/horarios-disponiveis?barbeiroId=$BARBEIRO&servicoId=$SERVICO&data=$DIA")"
verificar "  primeiro horário livre é 09:00" "09:00" "$(json "d['horarios'][0]")"

verificar "POST /api/agendamentos válido ($DIA 18:30, serviço de 30 min)" 201 \
    "$(chamar POST /api/agendamentos "{\"emailCliente\":\"$EMAIL1\",\"barbeiroId\":$BARBEIRO,\"servicoId\":$SERVICO,\"dataHoraInicio\":\"${DIA}T18:30:00\"}")"
AGENDAMENTO=$(json "d['id']")
verificar "  status do novo agendamento" "AGENDADO" "$(json "d['status']")"
verificar "POST /api/agendamentos no mesmo horário/barbeiro (RN-07)" 409 \
    "$(chamar POST /api/agendamentos "{\"emailCliente\":\"$EMAIL2\",\"barbeiroId\":$BARBEIRO,\"servicoId\":$SERVICO,\"dataHoraInicio\":\"${DIA}T18:30:00\"}")"
verificar "POST /api/agendamentos às 08:30 (RN-04)" 400 \
    "$(chamar POST /api/agendamentos "{\"emailCliente\":\"$EMAIL2\",\"barbeiroId\":$BARBEIRO,\"servicoId\":$SERVICO,\"dataHoraInicio\":\"${DIA}T08:30:00\"}")"
verificar "POST /api/agendamentos às 10:15 (RN-05)" 400 \
    "$(chamar POST /api/agendamentos "{\"emailCliente\":\"$EMAIL2\",\"barbeiroId\":$BARBEIRO,\"servicoId\":$SERVICO,\"dataHoraInicio\":\"${DIA}T10:15:00\"}")"
DOMINGO=$(proximo_domingo)
verificar "POST /api/agendamentos no domingo $DOMINGO (RN-04)" 400 \
    "$(chamar POST /api/agendamentos "{\"emailCliente\":\"$EMAIL2\",\"barbeiroId\":$BARBEIRO,\"servicoId\":$SERVICO,\"dataHoraInicio\":\"${DOMINGO}T10:00:00\"}")"
LONGE=$(python -c "import datetime as dt; print((dt.date.today()+dt.timedelta(days=45)).isoformat())")
verificar "POST /api/agendamentos para daqui a 45 dias (RN-06)" 400 \
    "$(chamar POST /api/agendamentos "{\"emailCliente\":\"$EMAIL2\",\"barbeiroId\":$BARBEIRO,\"servicoId\":$SERVICO,\"dataHoraInicio\":\"${LONGE}T10:00:00\"}")"
verificar "POST /api/agendamentos com e-mail não cadastrado" 404 \
    "$(chamar POST /api/agendamentos "{\"emailCliente\":\"ninguem.${SUFIXO}@exemplo.com\",\"barbeiroId\":$BARBEIRO,\"servicoId\":$SERVICO,\"dataHoraInicio\":\"${DIA}T11:00:00\"}")"

verificar "GET /api/agendamentos/{id} com o e-mail correto" 200 "$(chamar GET "/api/agendamentos/$AGENDAMENTO?email=$EMAIL1")"
verificar "GET /api/agendamentos/{id} com outro e-mail" 404 "$(chamar GET "/api/agendamentos/$AGENDAMENTO?email=$EMAIL2")"
verificar "PATCH /api/agendamentos/{id}/cancelar" 200 \
    "$(chamar PATCH "/api/agendamentos/$AGENDAMENTO/cancelar" "{\"email\":\"$EMAIL1\"}")"
verificar "  status após cancelamento" "CANCELADO" "$(json "d['status']")"
verificar "PATCH cancelar novamente (já cancelado)" 409 \
    "$(chamar PATCH "/api/agendamentos/$AGENDAMENTO/cancelar" "{\"email\":\"$EMAIL1\"}")"

verificar "GET /api/admin/barbeiros sem credenciais (RN-11)" 401 "$(chamar GET /api/admin/barbeiros)"
verificar "  resposta 401 não contém stack trace" "False" "$(json "'trace' in d or 'exception' in str(d).lower()")"
verificar "GET /api/admin/barbeiros com senha errada" 401 "$(chamar GET /api/admin/barbeiros '' 'admin:errada')"
verificar "GET /api/admin/barbeiros como administrador" 200 "$(chamar GET /api/admin/barbeiros '' "$ADMIN")"
verificar "POST /api/admin/servicos com duração 20 (RN-09)" 400 \
    "$(chamar POST /api/admin/servicos '{"nome":"Teste duração","duracaoMinutos":20,"preco":10.00}' "$ADMIN")"
verificar "POST /api/admin/servicos com preço 1000.01 (RN-09)" 400 \
    "$(chamar POST /api/admin/servicos '{"nome":"Teste preço","duracaoMinutos":30,"preco":1000.01}' "$ADMIN")"
verificar "POST /api/admin/servicos válido" 201 \
    "$(chamar POST /api/admin/servicos '{"nome":"Hidratação","duracaoMinutos":45,"preco":55.90}' "$ADMIN")"
NOVO_SERVICO=$(json "d['id']")
verificar "DELETE /api/admin/servicos/{id} sem agendamentos" 204 \
    "$(chamar DELETE "/api/admin/servicos/$NOVO_SERVICO" '' "$ADMIN")"
verificar "DELETE /api/admin/barbeiros/{id} com agendamentos" 409 \
    "$(chamar DELETE "/api/admin/barbeiros/$BARBEIRO" '' "$ADMIN")"

AMANHA=$(proximo_dia_util 1)
verificar "GET /api/admin/agenda do barbeiro em $AMANHA" 200 \
    "$(chamar GET "/api/admin/agenda?barbeiroId=$BARBEIRO&data=$AMANHA" '' "$ADMIN")"
PARA_CONCLUIR=$(json "[a['id'] for a in d if a['status']=='AGENDADO'][0]")
verificar "PATCH /api/admin/agendamentos/{id}/concluir" 200 \
    "$(chamar PATCH "/api/admin/agendamentos/$PARA_CONCLUIR/concluir" '' "$ADMIN")"
verificar "  status após conclusão" "CONCLUIDO" "$(json "d['status']")"

verificar "GET /admin/index.html sem login redireciona ao login" 302 \
    "$(curl -s -o /dev/null -w '%{http_code}' "$BASE/admin/index.html")"
verificar "GET /index.html (página pública)" 200 "$(curl -s -o /dev/null -w '%{http_code}' "$BASE/index.html")"

verificar "POST /api/dev/reset restaura a massa fictícia ao final" 200 "$(chamar POST /api/dev/reset)"

rm -f "$CORPO" "$ENVIO"
echo "== Resultado: $((TOTAL - FALHAS))/$TOTAL verificações OK =="
[ "$FALHAS" -eq 0 ]
