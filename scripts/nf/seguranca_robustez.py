"""
TNF-02 (RNF-02) — Segurança básica: nenhuma rota administrativa ou de dados pessoais responde dados sem credencial
                 válida, e nenhuma resposta de erro expõe detalhes internos (stack trace, classes, SQL).
TNF-06 (RNF-04) — Confiabilidade: entradas inválidas nunca produzem HTTP 500 (sempre 4xx com erro padronizado).
Uso (aplicação no ar, perfil test):  python scripts/nf/seguranca_robustez.py <pasta_evidencias> [--url ...]
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import comum  # noqa: E402

ROTAS_RESTRITAS = [
    ("GET", "/api/admin/barbeiros"), ("GET", "/api/admin/servicos"), ("GET", "/api/admin/sessao"),
    ("GET", "/api/admin/agenda?barbeiroId=1&data=2030-01-07"), ("GET", "/api/clientes"), ("GET", "/api/clientes/1"),
    ("POST", "/api/admin/barbeiros"), ("PUT", "/api/admin/barbeiros/1"), ("DELETE", "/api/admin/barbeiros/1"),
    ("POST", "/api/admin/servicos"), ("PUT", "/api/admin/servicos/1"), ("DELETE", "/api/admin/servicos/1"),
    ("PATCH", "/api/admin/agendamentos/1/concluir"), ("POST", "/api/dev/reset"),
]
CORPO = {"nome": "Teste Segurança", "ativo": True, "duracaoMinutos": 30, "preco": 10}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser()
    p.add_argument("destino")
    p.add_argument("--url", default="http://localhost:8080")
    a = p.parse_args()
    base, destino = a.url, Path(a.destino)
    destino.mkdir(parents=True, exist_ok=True)
    comum.restaurar(base)

    # ---- TNF-02: controle de acesso
    acesso = []
    for metodo, rota in ROTAS_RESTRITAS:
        for cenario, cred in (("sem credencial", None), ("senha errada", ("admin", "senha-errada"))):
            corpo = CORPO if metodo in ("POST", "PUT") else None
            r = comum.chamar(base, metodo, rota, corpo, credencial=cred)
            dados = r.json() if r.texto.startswith("{") else None
            sem_dados = isinstance(dados, dict) and set(dados) == {"status", "erro", "mensagem", "campos"}
            ok = r.status in (401, 403) and sem_dados and not comum.contem_detalhe_interno(r.texto)
            acesso.append({"metodo": metodo, "rota": rota, "cenario": cenario, "status": r.status,
                           "corpo_somente_erro": sem_dados, "ok": ok})
    comum.restaurar(base)  # garante que nada foi alterado

    # ---- TNF-06: entradas inválidas
    barbeiros, servicos = comum.ids(base)
    b, s = barbeiros["Carlos Navalha"], servicos["Corte de cabelo"]
    longa = "x" * 10000
    invalidas = [
        ("JSON malformado", "POST", "/api/clientes", None, b'{"nome": "Ana", '),
        ("corpo vazio", "POST", "/api/agendamentos", None, b""),
        ("tipo errado em barbeiroId", "POST", "/api/agendamentos", {"emailCliente": "ana.rocha@exemplo.com", "barbeiroId": "abc", "servicoId": s, "dataHoraInicio": "2030-01-07T10:00:00"}, None),
        ("data em formato inválido", "POST", "/api/agendamentos", {"emailCliente": "ana.rocha@exemplo.com", "barbeiroId": b, "servicoId": s, "dataHoraInicio": "07/01/2030 10:00"}, None),
        ("campos nulos", "POST", "/api/agendamentos", {"emailCliente": None, "barbeiroId": None, "servicoId": None, "dataHoraInicio": None}, None),
        ("número gigante", "POST", "/api/agendamentos", {"emailCliente": "ana.rocha@exemplo.com", "barbeiroId": 99999999999999999999, "servicoId": s, "dataHoraInicio": "2030-01-07T10:00:00"}, None),
        ("texto de 10.000 caracteres", "POST", "/api/clientes", {"nome": longa, "telefone": longa, "email": longa}, None),
        ("parâmetro ausente", "GET", f"/api/horarios-disponiveis?barbeiroId={b}", None, None),
        ("parâmetro de tipo errado", "GET", f"/api/horarios-disponiveis?barbeiroId=abc&servicoId={s}&data=2030-01-07", None, None),
        ("data inexistente", "GET", f"/api/horarios-disponiveis?barbeiroId={b}&servicoId={s}&data=2030-02-30", None, None),
        ("barbeiro inexistente", "GET", f"/api/horarios-disponiveis?barbeiroId=999999&servicoId={s}&data=2030-01-07", None, None),
        ("código com caracteres especiais", "GET", "/api/agendamentos/%3Cscript%3E?email=ana.rocha@exemplo.com", None, None),
        ("rota inexistente", "GET", "/api/nao-existe", None, None),
        ("método não suportado", "DELETE", "/api/barbeiros", None, None),
        ("tipo de conteúdo não suportado", "POST", "/api/clientes", None, "nome=Ana".encode()),
        ("cancelamento sem e-mail", "PATCH", "/api/agendamentos/SEMENTE2/cancelar", {}, None),
    ]
    robustez = []
    for nome, metodo, rota, corpo, bruto in invalidas:
        cab = {"Content-Type": "text/plain"} if nome == "tipo de conteúdo não suportado" else None
        r = comum.chamar(base, metodo, rota, corpo, corpo_bruto=bruto, cabecalhos=cab)
        ok = 400 <= r.status < 500 and not comum.contem_detalhe_interno(r.texto)
        robustez.append({"entrada": nome, "metodo": metodo, "rota": rota, "status": r.status,
                         "detalhe_interno_exposto": comum.contem_detalhe_interno(r.texto), "ok": ok})
    comum.restaurar(base)

    (destino / "TNF-02_seguranca_acesso.json").write_text(json.dumps(acesso, ensure_ascii=False, indent=2), encoding="utf-8")
    (destino / "TNF-06_entradas_invalidas.json").write_text(json.dumps(robustez, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"TNF-02 acesso restrito: {sum(x['ok'] for x in acesso)}/{len(acesso)} verificações OK")
    for x in acesso:
        if not x["ok"]:
            print("  FALHOU:", x)
    print(f"TNF-06 entradas inválidas: {sum(x['ok'] for x in robustez)}/{len(robustez)} sem HTTP 500 nem detalhe interno")
    for x in robustez:
        print(f"  {'OK    ' if x['ok'] else 'FALHOU'} {x['status']}  {x['entrada']}")


if __name__ == "__main__":
    main()
