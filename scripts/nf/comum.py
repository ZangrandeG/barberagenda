"""Funções comuns aos scripts de testes não funcionais (P09). Somente biblioteca padrão do Python."""
import base64
import datetime as dt
import json
import time
import urllib.error
import urllib.request

ADMIN = ("admin", "admin123")  # credencial FICTÍCIA de desenvolvimento/teste


class Resposta:
    def __init__(self, status, cabecalhos, texto, ms):
        self.status, self.cabecalhos, self.texto, self.ms = status, cabecalhos, texto, ms

    def json(self):
        return json.loads(self.texto) if self.texto else None


def chamar(base, metodo, caminho, corpo=None, credencial=None, corpo_bruto=None, cabecalhos=None):
    """Faz a requisição e devolve status, cabeçalhos, corpo e tempo em milissegundos (inclui a leitura do corpo)."""
    dados = corpo_bruto if corpo_bruto is not None else (json.dumps(corpo).encode() if corpo is not None else None)
    req = urllib.request.Request(base + caminho, data=dados, method=metodo)
    req.add_header("Accept", "application/json")
    if dados is not None:
        req.add_header("Content-Type", "application/json; charset=utf-8")
    for k, v in (cabecalhos or {}).items():
        req.add_header(k, v)
    if credencial:
        req.add_header("Authorization", "Basic " + base64.b64encode(f"{credencial[0]}:{credencial[1]}".encode()).decode())
    inicio = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            texto = r.read().decode("utf-8")
            return Resposta(r.status, dict(r.headers), texto, (time.perf_counter() - inicio) * 1000)
    except urllib.error.HTTPError as e:
        texto = e.read().decode("utf-8", errors="replace")
        return Resposta(e.code, dict(e.headers), texto, (time.perf_counter() - inicio) * 1000)


def aguardar(base, segundos=90):
    limite = time.time() + segundos
    while time.time() < limite:
        try:
            if chamar(base, "GET", "/api/barbeiros").status == 200:
                return True
        except OSError:
            pass
        time.sleep(1)
    return False


def restaurar(base):
    r = chamar(base, "POST", "/api/dev/reset", credencial=ADMIN)
    assert r.status == 200, f"restauração falhou: {r.status} {r.texto[:200]}"


def ids(base):
    barbeiros = {b["nome"]: b["id"] for b in chamar(base, "GET", "/api/admin/barbeiros", credencial=ADMIN).json()}
    servicos = {s["nome"]: s["id"] for s in chamar(base, "GET", "/api/admin/servicos", credencial=ADMIN).json()}
    return barbeiros, servicos


def dias_de_funcionamento(a_partir, quantidade):
    """Lista de datas (segunda a sábado) começando em hoje + a_partir dias."""
    datas, d = [], dt.date.today() + dt.timedelta(days=a_partir)
    while len(datas) < quantidade:
        if d.weekday() != 6:
            datas.append(d)
        d += dt.timedelta(days=1)
    return datas


def contem_detalhe_interno(texto):
    marcas = ("Exception", "at br.com", ".java:", "\"trace\"", "org.springframework", "org.hibernate", "SQL")
    return any(m in texto for m in marcas)


def agora():
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
