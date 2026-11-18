"""
Apoio à execução manual (P06): calcula as datas relativas usadas no P04 e mostra os ids
de barbeiros e serviços da aplicação em execução (os ids mudam a cada restauração dos dados).

Uso:  python scripts/datas_teste.py [--url http://localhost:8080] [--data AAAA-MM-DD]
"""
import argparse
import base64
import datetime as dt
import json
import sys
import urllib.request

DIAS = ["segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"]


def dia_funcionamento(base, n):
    data, passo, restantes = base, (1 if n >= 0 else -1), abs(n)
    while restantes:
        data += dt.timedelta(days=passo)
        if data.weekday() != 6:
            restantes -= 1
    return data


def obter(url, credencial=None):
    pedido = urllib.request.Request(url, headers={"Accept": "application/json"})
    if credencial:
        pedido.add_header("Authorization", "Basic " + base64.b64encode(credencial.encode()).decode())
    with urllib.request.urlopen(pedido, timeout=10) as resposta:
        return json.load(resposta)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser()
    p.add_argument("--url", default="http://localhost:8080")
    p.add_argument("--data", help="data da execução (padrão: hoje)")
    p.add_argument("--admin", default="admin:admin123", help="credencial fictícia do administrador")
    args = p.parse_args()

    d = dt.date.fromisoformat(args.data) if args.data else dt.date.today()
    domingo = d + dt.timedelta(days=(6 - d.weekday()) or 7)
    datas = [
        ("D", d), ("DF1", dia_funcionamento(d, 1)), ("DF2", dia_funcionamento(d, 2)), ("DF3", dia_funcionamento(d, 3)),
        ("ONTEM", d - dt.timedelta(days=1)), ("DOM", domingo),
        ("D+30", d + dt.timedelta(days=30)), ("D+31", d + dt.timedelta(days=31)),
        ("Dia de funcionamento anterior (SEMENTE5)", dia_funcionamento(d, -1)),
    ]
    print("Datas relativas do P04")
    for nome, valor in datas:
        print(f"  {nome:<42} {valor.isoformat()}  ({DIAS[valor.weekday()]})")
    print(f"  {'<AAAAMMDD> (e-mails únicos)':<42} {d.strftime('%Y%m%d')}")
    if (d + dt.timedelta(days=30)).weekday() == 6:
        print("\n  ATENÇÃO: D+30 cai em domingo — CT-015 deve ser registrado como Bloqueado e executado em outro dia.")

    print(f"\nIds na aplicação ({args.url})")
    try:
        barbeiros = obter(args.url + "/api/admin/barbeiros", args.admin)
        servicos = obter(args.url + "/api/admin/servicos", args.admin)
    except Exception as erro:  # aplicação parada ou credencial diferente
        print(f"  Não foi possível consultar a aplicação: {erro}")
        return
    for b in barbeiros:
        print(f"  barbeiro {b['id']:>4}  {b['nome']:<22} {'ativo' if b['ativo'] else 'INATIVO'}")
    for s in servicos:
        print(f"  serviço  {s['id']:>4}  {s['nome']:<22} {s['duracaoMinutos']:>3} min  R$ {s['preco']:>7}  "
              f"{'ativo' if s['ativo'] else 'INATIVO'}")


if __name__ == "__main__":
    main()
