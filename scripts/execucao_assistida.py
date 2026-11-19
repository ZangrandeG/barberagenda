"""
Execução assistida dos casos manuais do P04 (Marco 4), feita por Claude (IA) a pedido do grupo.

Cada caso é executado pelos mesmos passos do P04 — pela tela (Selenium, Chrome) ou pela API — com os dados
restaurados antes de cada caso. O resultado obtido é comparado com o esperado; a evidência (captura de tela e
transcrição das verificações/requisições) é salva em entrega/05_EXECUCAO_MANUAL/evidencias/ e uma linha é
acrescentada a dados/execucoes.csv. Nenhum resultado é escrito sem a verificação correspondente ter sido feita.

Uso (aplicação no ar em http://localhost:8080, perfil test ou dev):
  python scripts/execucao_assistida.py [CT-001 CT-002 ...]     (sem argumentos: todos os casos, em ordem de prioridade)
"""
import csv
import datetime as dt
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

sys.path.insert(0, str(Path(__file__).parent / "nf"))
import comum  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
BASE = "http://localhost:8080"
EVID = RAIZ / "entrega" / "05_EXECUCAO_MANUAL" / "evidencias"
CSV = RAIZ / "dados" / "execucoes.csv"
if os.environ.get("ENSAIO_DIR"):  # ensaio do próprio script: grava fora do projeto, sem registrar execuções oficiais
    EVID = Path(os.environ["ENSAIO_DIR"])
    CSV = EVID / "execucoes_ensaio.csv"
    EVID.mkdir(parents=True, exist_ok=True)
    if not CSV.exists():
        CSV.write_text("execucao,caso,data,versao,executor,resultado,evidencia,defeito,observacoes\n", encoding="utf-8")
EXECUTOR = "Claude (IA) — execução assistida por script, a pedido do grupo"
HOJE = dt.date.today()
DF1, DF2, DF3 = comum.dias_de_funcionamento(1, 3)
ONTEM = HOJE - dt.timedelta(days=1)
DOM = HOJE + dt.timedelta(days=(6 - HOJE.weekday()) or 7)
D30, D31 = HOJE + dt.timedelta(days=30), HOJE + dt.timedelta(days=31)
SUF = HOJE.strftime("%Y%m%d")
BR = lambda d: d.strftime("%d/%m/%Y")  # noqa: E731
MSG_NAO_ENCONTRADO = "Agendamento não encontrado para o código de acesso e o e-mail informados."
MSG_FUNC = "O atendimento deve ocorrer entre 09:00 e 19:00 e o serviço precisa terminar até 19:00."


class Execucao:
    def __init__(self, caso, ex, driver):
        self.caso, self.ex, self.d, self.linhas, self.ok = caso, ex, driver, [], True
        self.w = WebDriverWait(driver, 10)
        self.capturas = []

    # ---- registro
    def log(self, texto):
        self.linhas.append(texto)

    def verificar(self, descricao, condicao, obtido=""):
        self.ok &= bool(condicao)
        self.log(f"[{'OK' if condicao else 'FALHOU'}] {descricao}" + (f" — obtido: {obtido}" if obtido != "" else ""))

    # ---- API
    def api(self, metodo, caminho, corpo=None, cred=None):
        r = comum.chamar(BASE, metodo, caminho, corpo, credencial=cred)
        self.log(f"> {metodo} {caminho}" + (f"  {json.dumps(corpo, ensure_ascii=False)}" if corpo is not None else "")
                 + (" (admin)" if cred else ""))
        self.log(f"< HTTP {r.status}  {r.texto[:400]}")
        return r

    # ---- tela
    def abrir(self, caminho):
        self.d.get(BASE + caminho)

    def el(self, id_):
        return self.w.until(EC.visibility_of_element_located((By.ID, id_)))

    def digitar(self, id_, texto):
        e = self.el(id_)
        e.clear()
        e.send_keys(texto)

    def clicar(self, id_=None, css=None):
        alvo = (By.ID, id_) if id_ else (By.CSS_SELECTOR, css)
        self.w.until(EC.element_to_be_clickable(alvo)).click()

    def texto(self, id_, esperar=True):
        e = self.d.find_element(By.ID, id_)
        if esperar:
            self.w.until(lambda _: e.text.strip() != "")
        return e.text.strip()

    def visivel(self, id_):
        es = self.d.find_elements(By.ID, id_)
        return bool(es) and es[0].is_displayed()

    def selecionar(self, id_, prefixo):
        xp = f"//select[@id='{id_}']/option[starts-with(normalize-space(.), '{prefixo}')]"
        opcao = self.w.until(EC.presence_of_element_located((By.XPATH, xp)))
        Select(self.el(id_)).select_by_visible_text(opcao.text)

    def opcoes(self, id_):
        self.w.until(lambda d: len(d.find_elements(By.CSS_SELECTOR, f"#{id_} option")) > 1)
        return [o.text for o in self.d.find_elements(By.CSS_SELECTOR, f"#{id_} option")]

    def data(self, id_, valor):
        self.d.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('change'));",
                              self.el(id_), valor.isoformat())

    def capturar(self, sufixo=""):
        nome = f"{self.ex}_{self.caso}_{HOJE}{sufixo}.png"
        self.d.save_screenshot(str(EVID / nome))
        self.capturas.append(nome)

    # ---- fluxos de tela reaproveitados
    def cadastrar(self, nome, telefone, email):
        self.abrir("/cadastro.html")
        self.digitar("campo-nome-cliente", nome)
        self.digitar("campo-telefone-cliente", telefone)
        self.digitar("campo-email-cliente", email)
        self.clicar("botao-cadastrar-cliente")
        return self.texto("mensagem-cadastro")

    def horarios(self, barbeiro, servico, data, email=None):
        self.abrir("/agendar.html")
        if email:
            self.digitar("campo-email-agendamento", email)
        self.selecionar("campo-barbeiro", barbeiro)
        self.selecionar("campo-servico", servico)
        self.data("campo-data", data)
        self.clicar("botao-buscar-horarios")
        self.w.until(lambda d: d.find_elements(By.CSS_SELECTOR, "#lista-horarios button") or self.texto("mensagem-horarios", False))
        return [b.text for b in self.d.find_elements(By.CSS_SELECTOR, "#lista-horarios button")]

    def confirmar(self, horario):
        self.clicar(css=f"[data-testid='horario-{horario}']")
        self.clicar("botao-confirmar-agendamento")
        return self.texto("mensagem-agendamento")

    def consultar(self, codigo, email):
        self.abrir("/consulta.html")
        self.digitar("campo-codigo-acesso", codigo)
        self.digitar("campo-email-consulta", email)
        self.clicar("botao-consultar")
        try:
            self.w.until(lambda d: self.visivel("detalhes-agendamento") or self.texto("mensagem-consulta", False))
        except TimeoutException:
            pass

    def login(self, usuario="admin", senha="admin123"):
        self.abrir("/admin/login.html")
        self.digitar("campo-usuario", usuario)
        self.digitar("campo-senha", senha)
        self.clicar("botao-entrar")


def ids():
    return comum.ids(BASE)


def agendar_api(x, email, barbeiro, servico, inicio):
    b, s = ids()
    return x.api("POST", "/api/agendamentos", {"emailCliente": email, "barbeiroId": b[barbeiro], "servicoId": s[servico],
                                              "dataHoraInicio": inicio})


# =============================================================== casos
def ct_001(x):
    msg = x.cadastrar("Marina Lopes Teixeira", "14988776655", f"marina.{SUF}@exemplo.com")
    x.verificar("mensagem de sucesso com código do cliente", re.fullmatch(r"Cadastro realizado com sucesso! Código do cliente: \d+\.", msg), msg)
    x.verificar("botão 'Agendar um horário' visível", x.visivel("link-agendar-apos-cadastro"))
    x.capturar()


def ct_002(x):
    for suf, nome, tel, email in (("_a", "Léa", "1432221100", f"lea.{SUF}@exemplo.com"),
                                  ("_b", "Maria Eduarda Fernandes Albuquerque Cavalcanti Souza Ribeiro", "14999990000", f"maria.eduarda.{SUF}@exemplo.com")):
        msg = x.cadastrar(nome, tel, email)
        x.verificar(f"({suf[1]}) nome com {len(nome)} caracteres e telefone com {len(tel)} dígitos aceitos",
                    msg.startswith("Cadastro realizado com sucesso!"), msg)
        x.capturar(suf)


def ct_003(x):
    for suf, nome in (("_a", "Al"), ("_b", "Maria Eduarda Fernandes Albuquerque Cavalcanti Souza Ribeiros")):
        msg = x.cadastrar(nome, "14988776655", f"nome.limite.{SUF}@exemplo.com")
        erro = x.texto("erro-nome-cliente")
        x.verificar(f"({suf[1]}) nome com {len(nome)} caracteres: erro no campo", erro == "O nome deve ter entre 3 e 60 caracteres.", erro)
        x.verificar(f"({suf[1]}) mensagem geral e nenhum código", msg == "Existem campos inválidos." and not x.visivel("link-agendar-apos-cadastro"), msg)
        x.capturar(suf)


def ct_004(x):
    esperado = "O telefone deve conter somente dígitos, com 10 ou 11 dígitos (incluindo DDD)."
    for suf, tel in (("_a", "149887766"), ("_b", "149887766551"), ("_c", "14-98877-6655")):
        x.cadastrar("Rodrigo Teste", tel, f"rodrigo.{SUF}@exemplo.com")
        erro = x.texto("erro-telefone-cliente")
        x.verificar(f"({suf[1]}) telefone '{tel}' recusado", erro == esperado, erro)
        x.capturar(suf)


def ct_005(x):
    for suf, email in (("_a", "paula.exemplo.com"), ("_b", "paula@exemplo")):
        x.cadastrar("Paula Teste", "14988776655", email)
        erro = x.texto("erro-email-cliente")
        x.verificar(f"({suf[1]}) e-mail '{email}' recusado", erro == "O e-mail informado é inválido.", erro)
        x.capturar(suf)


def ct_006(x):
    msg = x.cadastrar("Ana Repetida", "14988776655", "ANA.ROCHA@EXEMPLO.COM")
    x.verificar("e-mail repetido recusado", msg == "Já existe um cliente cadastrado com este e-mail.", msg)
    x.capturar()


def ct_007(x):
    h = x.horarios("Carlos Navalha", "Corte e barba", DF3)
    esperado = [f"{9 + i // 2:02d}:{30 * (i % 2):02d}" for i in range(19)]
    x.verificar(f"19 horários de 09:00 a 18:00 em {DF3}", h == esperado, f"{len(h)} horários: {h[0] if h else '-'} … {h[-1] if h else '-'}")
    x.capturar()


def ct_008(x):
    h = x.horarios("Rafael Tesoura", "Corte de cabelo", DF1)
    x.verificar("14:00 e 14:30 ausentes", "14:00" not in h and "14:30" not in h)
    x.verificar("13:30 e 15:00 presentes", "13:30" in h and "15:00" in h)
    x.verificar("18 horários", len(h) == 18, len(h))
    x.capturar()


def ct_009(x):
    b, s = ids()
    for rotulo, data in (("DOM", DOM), ("D+31", D31), ("ONTEM", ONTEM)):
        r = x.api("GET", f"/api/horarios-disponiveis?barbeiroId={b['Carlos Navalha']}&servicoId={s['Corte de cabelo']}&data={data}")
        x.verificar(f"{rotulo} ({data}): HTTP 200 e lista vazia", r.status == 200 and r.json()["horarios"] == [], r.status)


def ct_010(x):
    x.horarios("Carlos Navalha", "Barba", DF3, email="camila.prado@exemplo.com")
    msg = x.confirmar("11:00")
    codigo = x.texto("codigo-acesso")
    x.verificar("mensagem com código de acesso", msg == f"Agendamento realizado com sucesso! Código de acesso: {codigo}.", msg)
    x.verificar("código com 8 caracteres", re.fullmatch(r"[A-HJKMNP-Z2-9]{8}", codigo), codigo)
    x.verificar("resumo: Carlos Navalha, Barba, data 11:00, AGENDADO",
                (x.texto("resumo-barbeiro"), x.texto("resumo-servico"), x.texto("resumo-data-hora"), x.texto("resumo-status"))
                == ("Carlos Navalha", "Barba", f"{BR(DF3)} 11:00", "AGENDADO"))
    x.capturar()


def ct_011(x):
    for suf, hora in (("_a", "09:00"), ("_b", "18:30")):
        x.horarios("Carlos Navalha", "Corte de cabelo", DF3, email="felipe.nunes@exemplo.com")
        msg = x.confirmar(hora)
        x.verificar(f"({suf[1]}) agendamento às {hora} confirmado", msg.startswith("Agendamento realizado com sucesso!"), msg)
        x.verificar(f"({suf[1]}) status AGENDADO", x.texto("resumo-status") == "AGENDADO")
        x.capturar(suf)


def ct_012(x):
    for rotulo, servico, hora, status in (("(a)", "Corte de cabelo", "08:30", 400), ("(b)", "Corte e barba", "18:30", 400),
                                          ("(c)", "Corte e barba", "18:00", 201)):
        r = agendar_api(x, "gabriela.teixeira@exemplo.com", "Carlos Navalha", servico, f"{DF3}T{hora}:00")
        ok = r.status == status and (status == 201 or r.json()["mensagem"] == MSG_FUNC)
        x.verificar(f"{rotulo} {servico} às {hora}: HTTP {status}", ok, r.status)


def ct_013(x):
    for hora in ("10:15", "10:01"):
        r = agendar_api(x, "gabriela.teixeira@exemplo.com", "Carlos Navalha", "Corte de cabelo", f"{DF3}T{hora}:00")
        msg = "Os agendamentos devem começar em intervalos de 30 minutos (ex.: 09:00, 09:30)."
        x.verificar(f"{hora}: HTTP 400, mensagem e campo dataHoraInicio",
                    r.status == 400 and r.json()["mensagem"] == msg and "dataHoraInicio" in r.json()["campos"], r.status)


def ct_014(x):
    r = agendar_api(x, "gabriela.teixeira@exemplo.com", "Carlos Navalha", "Corte de cabelo", f"{DOM}T10:00:00")
    x.verificar(f"domingo {DOM}: HTTP 400 'A barbearia não abre aos domingos.'",
                r.status == 400 and r.json()["mensagem"] == "A barbearia não abre aos domingos.", r.status)


def ct_015(x):
    if D30.weekday() == 6:
        raise BloqueadoErro(f"D+30 ({D30}) cai em domingo")
    r = agendar_api(x, "heitor.moreira@exemplo.com", "Carlos Navalha", "Corte de cabelo", f"{D30}T10:00:00")
    x.verificar(f"D+30 ({D30}): HTTP 201 AGENDADO", r.status == 201 and r.json()["status"] == "AGENDADO", r.status)
    r = agendar_api(x, "heitor.moreira@exemplo.com", "Carlos Navalha", "Corte de cabelo", f"{D31}T10:00:00")
    x.verificar(f"D+31 ({D31}): HTTP 400 antecedência máxima",
                r.status == 400 and r.json()["mensagem"] == "A antecedência máxima para agendamento é de 30 dias.", r.status)


def ct_016(x):
    msg = "Não é permitido agendar em data ou horário que já passou."
    r = agendar_api(x, "heitor.moreira@exemplo.com", "Carlos Navalha", "Corte de cabelo", f"{ONTEM}T10:00:00")
    x.verificar(f"(a) ontem {ONTEM} 10:00: HTTP 400", r.status == 400 and r.json()["mensagem"] == msg, r.status)
    if dt.datetime.now().time() < dt.time(9, 30) or HOJE.weekday() == 6:
        x.log("(b) não aplicável neste horário/dia (pré-condição: segunda a sábado após 09:30)")
    else:
        r = agendar_api(x, "heitor.moreira@exemplo.com", "Carlos Navalha", "Corte de cabelo", f"{HOJE}T09:00:00")
        x.verificar(f"(b) hoje {HOJE} 09:00: HTTP 400", r.status == 400 and r.json()["mensagem"] == msg, r.status)


def ct_017(x):
    x.abrir("/agendar.html")
    barbeiros, servicos = x.opcoes("campo-barbeiro"), x.opcoes("campo-servico")
    x.verificar("Diego Máquina e Relaxamento capilar não aparecem na tela",
                not any("Diego" in o for o in barbeiros) and not any("Relaxamento" in o for o in servicos))
    x.capturar()
    r = agendar_api(x, "gabriela.teixeira@exemplo.com", "Diego Máquina", "Corte de cabelo", f"{DF3}T10:00:00")
    x.verificar("(a) barbeiro inativo: HTTP 400", r.status == 400 and r.json()["mensagem"] == "O barbeiro selecionado está inativo.", r.status)
    r = agendar_api(x, "gabriela.teixeira@exemplo.com", "Carlos Navalha", "Relaxamento capilar", f"{DF3}T10:00:00")
    x.verificar("(b) serviço inativo: HTTP 400", r.status == 400 and r.json()["mensagem"] == "O serviço selecionado está inativo.", r.status)


def ct_018(x):
    x.horarios("Carlos Navalha", "Barba", DF3, email="nao.cadastrado@exemplo.com")
    msg = x.confirmar("15:00")
    x.verificar("mensagem de cliente não encontrado",
                msg == "Cliente não encontrado para o e-mail informado. Faça o cadastro antes de agendar.", msg)
    x.verificar("nenhum resumo/código exibido", not x.visivel("resumo-agendamento"))
    x.capturar()


def ct_019(x):
    for rotulo, servico, hora in (("(a)", "Corte de cabelo", "14:30"), ("(b)", "Corte e barba", "13:30")):
        r = agendar_api(x, "joao.mendes@exemplo.com", "Rafael Tesoura", servico, f"{DF1}T{hora}:00")
        x.verificar(f"{rotulo} {hora}: HTTP 409 horário ocupado",
                    r.status == 409 and r.json()["mensagem"] == "O barbeiro já possui agendamento nesse horário.", r.status)


def ct_020(x):
    for rotulo, barbeiro, hora in (("(a)", "Rafael Tesoura", "13:30"), ("(b)", "Rafael Tesoura", "15:00"), ("(c)", "Carlos Navalha", "14:00")):
        r = agendar_api(x, "isabela.pires@exemplo.com", barbeiro, "Corte de cabelo", f"{DF1}T{hora}:00")
        x.verificar(f"{rotulo} {barbeiro} {hora}: HTTP 201", r.status == 201 and r.json()["status"] == "AGENDADO", r.status)


def preparar_tres(x, email, telefone):
    x.api("POST", "/api/clientes", {"nome": "Cliente Limite", "telefone": telefone, "email": email})
    return [agendar_api(x, email, "Carlos Navalha", "Corte de cabelo", f"{DF3}T{h}:00") for h in ("09:00", "09:30", "10:00")]


def ct_021(x):
    rs = preparar_tres(x, f"ct021.{SUF}@exemplo.com", "14977770021")
    x.verificar("1º, 2º e 3º agendamentos: HTTP 201", [r.status for r in rs] == [201, 201, 201], [r.status for r in rs])
    r = agendar_api(x, f"ct021.{SUF}@exemplo.com", "Carlos Navalha", "Corte de cabelo", f"{DF3}T10:30:00")
    x.verificar("4º agendamento: HTTP 409 limite",
                r.status == 409 and r.json()["mensagem"] == "O cliente já possui 3 agendamentos ativos, que é o limite permitido.", r.status)


def ct_022(x):
    email = f"ct022.{SUF}@exemplo.com"
    codigo = preparar_tres(x, email, "14977770022")[0].json()["codigoAcesso"]
    x.consultar(codigo, email)
    x.clicar("botao-cancelar-agendamento")
    x.clicar("botao-confirmar-cancelamento")
    x.w.until(lambda _: x.texto("detalhe-status") == "CANCELADO")
    x.verificar("agendamento das 09:00 cancelado pela tela", x.texto("detalhe-status") == "CANCELADO")
    x.capturar()
    r = agendar_api(x, email, "Carlos Navalha", "Corte de cabelo", f"{DF3}T10:30:00")
    x.verificar("novo agendamento após cancelar: HTTP 201", r.status == 201, r.status)


def ct_023(x):
    x.consultar("semente2", "ana.rocha@exemplo.com")
    valores = {k: x.texto("detalhe-" + k).replace(" ", " ")
               for k in ("codigo", "cliente", "barbeiro", "servico", "data-hora", "preco", "status")}
    esperado = {"codigo": "SEMENTE2", "cliente": "Ana Beatriz Rocha", "barbeiro": "Carlos Navalha",
                "servico": "Corte de cabelo (30 min)", "data-hora": f"{BR(DF1)} 10:00", "preco": "R$ 45,00", "status": "AGENDADO"}
    x.verificar("detalhes exibidos conforme o esperado", valores == esperado, valores)
    x.verificar("botão 'Cancelar agendamento' visível", x.visivel("botao-cancelar-agendamento"))
    x.capturar()


def ct_024(x):
    for suf, codigo, email in (("_a", "SEMENTE2", "bruno.lima@exemplo.com"), ("_b", "ZZZZ9999", "ana.rocha@exemplo.com"),
                               ("_c", "1", "ana.rocha@exemplo.com")):
        x.consultar(codigo, email)
        msg = x.texto("mensagem-consulta")
        x.verificar(f"({suf[1]}) {codigo} + {email}: não encontrado, sem dados", msg == MSG_NAO_ENCONTRADO and not x.visivel("detalhes-agendamento"), msg)
        x.capturar(suf)


def ct_025(x):
    x.consultar("SEMENTE6", "eduarda.costa@exemplo.com")
    x.clicar("botao-cancelar-agendamento")
    x.clicar("botao-confirmar-cancelamento")
    x.w.until(lambda _: x.texto("detalhe-status") == "CANCELADO")
    x.verificar("mensagem e status CANCELADO", x.texto("mensagem-consulta") == "Agendamento cancelado com sucesso.")
    x.verificar("botão de cancelar oculto", not x.visivel("botao-cancelar-agendamento"))
    x.capturar("_a")
    h = x.horarios("Carlos Navalha", "Sobrancelha", DF2)
    x.verificar(f"16:00 volta a ser oferecido em {DF2}", "16:00" in h)
    x.capturar("_b")


def ct_026(x):
    x.consultar("SEMENTE4", "camila.prado@exemplo.com")
    x.verificar("SEMENTE4 exibido como CANCELADO, sem botão de cancelar",
                x.texto("detalhe-status") == "CANCELADO" and not x.visivel("botao-cancelar-agendamento"))
    x.capturar()
    for codigo, email in (("SEMENTE4", "camila.prado@exemplo.com"), ("SEMENTE5", "daniel.alves@exemplo.com")):
        r = x.api("PATCH", f"/api/agendamentos/{codigo}/cancelar", {"email": email})
        x.verificar(f"cancelar {codigo}: HTTP 409",
                    r.status == 409 and r.json()["mensagem"] == "Somente agendamentos com status AGENDADO podem ser cancelados.", r.status)


def ct_027(x):
    x.abrir("/admin/")
    x.verificar("passo 1: tela de login", x.d.current_url.endswith("/admin/login.html"), x.d.current_url)
    x.login()
    x.w.until(EC.url_contains("/admin/index.html"))
    x.verificar("passo 2: painel com 'Usuário: admin'", x.texto("usuario-logado") == "Usuário: admin")
    x.capturar("_a")
    x.clicar("botao-sair")
    x.w.until(EC.url_contains("/admin/login.html"))
    x.verificar("passo 3: mensagem de saída", x.texto("mensagem-login") == "Você saiu da área administrativa.")
    x.abrir("/admin/index.html")
    x.verificar("passo 4: volta a exigir login", x.d.current_url.endswith("/admin/login.html"), x.d.current_url)
    x.capturar("_b")


def ct_028(x):
    x.login(senha="senhaerrada")
    msg = x.texto("mensagem-login")
    x.verificar("mensagem de credencial inválida e permanência no login",
                msg == "Usuário ou senha inválidos." and x.d.current_url.endswith("/admin/login.html"), msg)
    x.capturar()


def ct_029(x):
    x.abrir("/admin/agenda.html")
    x.verificar("página administrativa redireciona ao login", x.d.current_url.endswith("/admin/login.html"), x.d.current_url)
    x.capturar()
    for rota in ("/api/admin/barbeiros", "/api/clientes"):
        r = x.api("GET", rota)
        x.verificar(f"GET {rota}: HTTP 401 sem dados", r.status == 401 and r.json()["mensagem"] == "Autenticação necessária.", r.status)
    r = x.api("POST", "/api/admin/servicos", {"nome": "Serviço Invasor", "duracaoMinutos": 30, "preco": 10.00})
    x.verificar("POST sem credenciais: HTTP 403", r.status == 403, r.status)
    r = x.api("GET", "/api/servicos")
    x.verificar("'Serviço Invasor' não existe", "Serviço Invasor" not in r.texto)


def ct_030(x):
    x.login()
    x.w.until(EC.url_contains("/admin/index.html"))
    x.abrir("/admin/servicos.html")
    for suf, nome, dur, preco, trecho in (("_a", "Acabamento", "15", "1.00", "15 min R$ 1,00"),
                                         ("_b", "Tratamento completo", "180", "1000.00", "180 min R$ 1.000,00")):
        x.digitar("campo-nome-servico", nome)
        x.digitar("campo-duracao-servico", dur)
        x.digitar("campo-preco-servico", preco)
        x.clicar("botao-salvar-servico")
        msg = x.texto("mensagem-servico")
        linha = x.w.until(EC.visibility_of_element_located((By.XPATH, f"//table[@id='tabela-servicos']//tr[td[normalize-space(.)='{nome}']]"))).text
        x.verificar(f"({suf[1]}) '{nome}' cadastrado e na tabela",
                    re.fullmatch(r"Serviço cadastrado \(código \d+\)\.", msg) and trecho in linha.replace(" ", " ") and "Ativo" in linha, linha)
        x.capturar(suf)


def ct_031(x):
    x.login()
    x.w.until(EC.url_contains("/admin/index.html"))
    x.abrir("/admin/servicos.html")
    casos = (("_a", "14", "10", "erro-duracao-servico", ("A duração deve ser de no mínimo 15 minutos.", "A duração deve ser múltipla de 15 minutos."))
             , ("_b", "20", "10", "erro-duracao-servico", ("A duração deve ser múltipla de 15 minutos.",)),
             ("_c", "195", "10", "erro-duracao-servico", ("A duração deve ser de no máximo 180 minutos.",)),
             ("_d", "30", "0.99", "erro-preco-servico", ("O preço deve ser de no mínimo R$ 1,00.",)),
             ("_e", "30", "1000.01", "erro-preco-servico", ("O preço deve ser de no máximo R$ 1.000,00.",)))
    for suf, dur, preco, campo, aceitas in casos:
        x.digitar("campo-nome-servico", "Serviço Limite")
        x.digitar("campo-duracao-servico", dur)
        x.digitar("campo-preco-servico", preco)
        x.clicar("botao-salvar-servico")
        erro = x.texto(campo)
        x.verificar(f"({suf[1]}) duração {dur}, preço {preco}: mensagem esperada", erro in aceitas, erro)
        x.capturar(suf)
    r = x.api("GET", "/api/admin/servicos", cred=comum.ADMIN)
    x.verificar("nenhum 'Serviço Limite' cadastrado", "Serviço Limite" not in r.texto)


def ct_032(x):
    rafael = ids()[0]["Rafael Tesoura"]
    x.login()
    x.w.until(EC.url_contains("/admin/index.html"))
    x.abrir("/admin/barbeiros.html")
    x.clicar(css=f"[data-testid='editar-barbeiro-{rafael}']")
    caixa = x.el("campo-ativo-barbeiro")
    if caixa.is_selected():
        caixa.click()
    x.clicar("botao-salvar-barbeiro")
    msg = x.texto("mensagem-barbeiro")
    linha = x.d.find_element(By.CSS_SELECTOR, f"[data-testid='linha-barbeiro-{rafael}']").text
    x.verificar("Rafael atualizado como Inativo", msg == "Barbeiro atualizado." and "Inativo" in linha, f"{msg} | {linha}")
    x.capturar("_a")
    x.abrir("/agendar.html")
    x.verificar("Rafael Tesoura não aparece para o cliente", not any("Rafael" in o for o in x.opcoes("campo-barbeiro")))
    x.capturar("_b")


def ct_033(x):
    carlos = ids()[0]["Carlos Navalha"]
    x.login()
    x.w.until(EC.url_contains("/admin/index.html"))
    x.abrir("/admin/barbeiros.html")
    for _ in range(2):
        x.clicar(css=f"[data-testid='excluir-barbeiro-{carlos}']")
    msg = x.texto("mensagem-barbeiro")
    x.verificar("Carlos não pode ser excluído", msg == "O barbeiro possui agendamentos e não pode ser excluído. Desative-o em vez de excluir.", msg)
    x.capturar("_a")
    x.digitar("campo-nome-barbeiro", "Barbeiro Temporário")
    x.clicar("botao-salvar-barbeiro")
    x.texto("mensagem-barbeiro")
    temp = ids()[0]["Barbeiro Temporário"]
    x.w.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"[data-testid='excluir-barbeiro-{temp}']")))
    for _ in range(2):
        x.clicar(css=f"[data-testid='excluir-barbeiro-{temp}']")
    x.w.until(lambda _: x.texto("mensagem-barbeiro") == "Barbeiro excluído.")
    x.verificar("Barbeiro Temporário excluído e removido da tabela",
                not x.d.find_elements(By.CSS_SELECTOR, f"[data-testid='linha-barbeiro-{temp}']"))
    x.capturar("_b")


def ct_034(x):
    x.login()
    x.w.until(EC.url_contains("/admin/index.html"))
    x.abrir("/admin/agenda.html")
    x.selecionar("campo-barbeiro-agenda", "Rafael Tesoura")
    x.data("campo-data-agenda", DF1)
    x.clicar("botao-carregar-agenda")
    linha = x.w.until(EC.visibility_of_element_located((By.XPATH, "//table[@id='tabela-agenda']//tr[td[contains(., '14:00')]]")))
    texto = linha.text
    x.verificar("linha 14:00 – 15:00, Bruno Henrique Lima, Corte e barba, AGENDADO, sem código de acesso",
                all(t in texto for t in ("14:00", "15:00", "Bruno Henrique Lima", "Corte e barba", "AGENDADO")) and "SEMENTE" not in x.d.page_source, texto)
    x.capturar("_a")
    linha.find_element(By.TAG_NAME, "button").click()
    msg = x.texto("mensagem-agenda")
    x.w.until(lambda d: "CONCLUIDO" in d.find_element(By.ID, "tabela-agenda").text)
    x.verificar("atendimento concluído", re.fullmatch(r"Atendimento #\d+ marcado como concluído\.", msg), msg)
    x.capturar("_b")


def ct_035(x):
    carlos = ids()[0]["Carlos Navalha"]
    r = x.api("GET", f"/api/admin/agenda?barbeiroId={carlos}&data={DF2}", cred=comum.ADMIN)
    alvo = next(a for a in r.json() if a["dataHoraInicio"].endswith("09:30:00"))
    x.verificar("agendamento das 09:30 está CANCELADO", alvo["status"] == "CANCELADO", alvo["status"])
    r = x.api("PATCH", f"/api/admin/agendamentos/{alvo['id']}/concluir", cred=comum.ADMIN)
    x.verificar("concluir: HTTP 409", r.status == 409 and r.json()["mensagem"] == "Somente agendamentos com status AGENDADO podem ser concluídos.", r.status)


class BloqueadoErro(Exception):
    pass


# =============================================================== execução
def proximo_ex():
    with open(CSV, encoding="utf-8") as f:
        nums = [int(l["execucao"][3:]) for l in csv.DictReader(f) if l["execucao"]]
    return max(nums, default=0) + 1


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    casos = json.load(open(RAIZ / "dados" / "casos.json", encoding="utf-8"))
    ordem = {"Alta": 0, "Média": 1, "Baixa": 2}
    selecionados = [c["id"] for c in sorted(casos, key=lambda c: (ordem[c["prioridade"]], c["id"]))]
    if len(sys.argv) > 1:
        selecionados = [c for c in selecionados if c in sys.argv[1:]]
    versao = subprocess.run(["git", "describe", "--tags"], capture_output=True, text=True, cwd=RAIZ).stdout.strip()
    EVID.mkdir(parents=True, exist_ok=True)
    opcoes = webdriver.ChromeOptions()
    opcoes.add_argument("--headless=new")
    opcoes.add_argument("--window-size=1366,900")
    driver = webdriver.Chrome(options=opcoes)
    datas = f"D={HOJE} DF1={DF1} DF2={DF2} DF3={DF3} ONTEM={ONTEM} DOM={DOM} D+30={D30} D+31={D31}"
    try:
        for caso in selecionados:
            comum.restaurar(BASE)
            driver.delete_all_cookies()
            ex = f"EX-{proximo_ex():03d}"
            x = Execucao(caso, ex, driver)
            x.log(f"{ex} — {caso} — {comum.agora()} — BarberAgenda 1.1.0 ({versao}) — {EXECUTOR}")
            x.log(datas)
            try:
                globals()["ct_" + caso[3:]](x)
                resultado = "Aprovado" if x.ok else "Reprovado"
            except BloqueadoErro as e:
                resultado = "Bloqueado"
                x.log(f"[BLOQUEADO] {e}")
            except Exception as e:  # falha na execução: registrada como Reprovado para análise, com o erro
                resultado = "Reprovado"
                x.log(f"[ERRO NA EXECUÇÃO] {type(e).__name__}: {e}")
                try:
                    x.capturar("_erro")
                except Exception:
                    pass
            transcricao = f"{ex}_{caso}_{HOJE}.txt"
            (EVID / transcricao).write_text("\n".join(x.linhas) + f"\nRESULTADO: {resultado}\n", encoding="utf-8")
            evidencias = " ".join([transcricao] + x.capturas)
            with open(CSV, "a", encoding="utf-8", newline="") as f:
                csv.writer(f).writerow([ex, caso, HOJE.isoformat(), f"1.1.0 ({versao})", EXECUTOR, resultado, evidencias, "", ""])
            print(f"{ex} {caso}: {resultado}" + ("" if resultado == "Aprovado" else "  <-- ver " + transcricao))
    finally:
        driver.quit()
        comum.restaurar(BASE)


if __name__ == "__main__":
    main()
