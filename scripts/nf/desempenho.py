"""
TNF-01 (RNF-01) — Desempenho básico: tempo de resposta de GET /api/horarios-disponiveis e POST /api/agendamentos.
5 requisições de aquecimento + 30 medidas por operação; critério: p95 < 500 ms.
Uso (aplicação no ar, perfil test):  python scripts/nf/desempenho.py <pasta_evidencias> [--url http://localhost:8080]
"""
import argparse
import csv
import json
import math
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import comum  # noqa: E402

AQUECIMENTO, MEDIDAS, LIMITE_P95_MS = 5, 30, 500


def p95(valores):
    ordenados = sorted(valores)
    return ordenados[math.ceil(0.95 * len(ordenados)) - 1]  # método do posto mais próximo


def resumo(nome, tempos):
    return {"operacao": nome, "amostras": len(tempos), "media_ms": round(statistics.mean(tempos), 1),
            "mediana_ms": round(statistics.median(tempos), 1), "p95_ms": round(p95(tempos), 1),
            "min_ms": round(min(tempos), 1), "max_ms": round(max(tempos), 1),
            "criterio": f"p95 < {LIMITE_P95_MS} ms", "atende": p95(tempos) < LIMITE_P95_MS}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser()
    p.add_argument("destino")
    p.add_argument("--url", default="http://localhost:8080")
    a = p.parse_args()
    base, destino = a.url, Path(a.destino)
    destino.mkdir(parents=True, exist_ok=True)
    inicio = comum.agora()

    comum.restaurar(base)
    barbeiros, servicos = comum.ids(base)
    carlos, rafael, corte = barbeiros["Carlos Navalha"], barbeiros["Rafael Tesoura"], servicos["Corte de cabelo"]
    data = comum.dias_de_funcionamento(7, 1)[0]

    # 1) GET /api/horarios-disponiveis
    url = f"/api/horarios-disponiveis?barbeiroId={carlos}&servicoId={corte}&data={data}"
    tempos_get = []
    for i in range(AQUECIMENTO + MEDIDAS):
        r = comum.chamar(base, "GET", url)
        assert r.status == 200, r.texto
        if i >= AQUECIMENTO:
            tempos_get.append(r.ms)

    # 2) POST /api/agendamentos — cada pedido usa horário livre diferente; até 3 por cliente (RN-08)
    total = AQUECIMENTO + MEDIDAS
    emails = []
    for n in range(math.ceil(total / 3)):
        email = f"desempenho.{n}.{abs(hash(inicio)) % 100000}@exemplo.com"
        r = comum.chamar(base, "POST", "/api/clientes", {"nome": f"Cliente Desempenho {n}", "telefone": "14900000000", "email": email})
        assert r.status == 201, r.texto
        emails.append(email)
    vagas = [(b, d, f"{h:02d}:{m:02d}") for d in comum.dias_de_funcionamento(8, 3) for b in (carlos, rafael)
             for h in range(9, 19) for m in (0, 30)]
    tempos_post = []
    for i in range(total):
        barbeiro, dia, hora = vagas[i]
        corpo = {"emailCliente": emails[i // 3], "barbeiroId": barbeiro, "servicoId": corte, "dataHoraInicio": f"{dia}T{hora}:00"}
        r = comum.chamar(base, "POST", "/api/agendamentos", corpo)
        assert r.status == 201, r.texto
        if i >= AQUECIMENTO:
            tempos_post.append(r.ms)
    comum.restaurar(base)

    resultados = [resumo("GET /api/horarios-disponiveis", tempos_get), resumo("POST /api/agendamentos", tempos_post)]
    with open(destino / "TNF-01_desempenho_amostras.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["operacao", "amostra", "tempo_ms"])
        for nome, tempos in (("GET /api/horarios-disponiveis", tempos_get), ("POST /api/agendamentos", tempos_post)):
            w.writerows((nome, k + 1, round(t, 2)) for k, t in enumerate(tempos))
    (destino / "TNF-01_desempenho_resultado.json").write_text(
        json.dumps({"inicio": inicio, "fim": comum.agora(), "url": base, "resultados": resultados}, ensure_ascii=False, indent=2),
        encoding="utf-8")
    for r in resultados:
        print(f"{r['operacao']:<32} média {r['media_ms']:>6} ms | p95 {r['p95_ms']:>6} ms | máx {r['max_ms']:>6} ms | "
              f"{'ATENDE' if r['atende'] else 'NÃO ATENDE'}")


if __name__ == "__main__":
    main()
