"""
Gera a coleção e o ambiente do Postman (formato v2.1) usados nos testes de integração/API (P08, Marco 6):

  postman/BarberAgenda.postman_collection.json
  postman/BarberAgenda.postman_environment.json

Uso: python scripts/gerar_colecao_postman.py   (depois importe os dois arquivos no Postman, se quiser editá-los lá)
Execução: newman run postman/BarberAgenda.postman_collection.json -e postman/BarberAgenda.postman_environment.json
"""
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PASTA = RAIZ / "postman"

ADMIN = {"type": "basic", "basic": [{"key": "username", "value": "{{adminUsuario}}", "type": "string"},
                                    {"key": "password", "value": "{{adminSenha}}", "type": "string"}]}
SEM_AUTH = {"type": "noauth"}

# Funções JavaScript reaproveitadas nos scripts (cada script do Postman é isolado).
JS_DATAS = """
function doisDigitos(n) { return String(n).padStart(2, '0'); }
function formatarData(d) { return d.getFullYear() + '-' + doisDigitos(d.getMonth() + 1) + '-' + doisDigitos(d.getDate()); }
function formatarDataHora(d) { return formatarData(d) + 'T' + doisDigitos(d.getHours()) + ':' + doisDigitos(d.getMinutes()) + ':00'; }
function somarMinutos(isoLocal, minutos) { const d = new Date(isoLocal); d.setMinutes(d.getMinutes() + minutos); return formatarDataHora(d); }
"""

JS_CONTRATO_ERRO = """
function verificarContratoDeErro(json, status) {
    pm.expect(json).to.have.all.keys('status', 'erro', 'mensagem', 'campos');
    pm.expect(json.status).to.eql(status);
    pm.expect(json.mensagem).to.be.a('string').and.not.empty;
    pm.expect(json.campos).to.be.an('object');
    pm.expect(JSON.stringify(json)).to.not.match(/Exception|at br\\.com|\\.java/);
}
"""


def req(nome, metodo, url, testes, corpo=None, auth=None, pre=None):
    item = {"name": nome, "event": [{"listen": "test", "script": {"type": "text/javascript", "exec": testes.strip("\n").split("\n")}}],
            "request": {"method": metodo, "header": [], "url": url, "auth": auth or SEM_AUTH}}
    if pre:
        item["event"].insert(0, {"listen": "prerequest", "script": {"type": "text/javascript", "exec": pre.strip("\n").split("\n")}})
    if corpo is not None:
        item["request"]["header"].append({"key": "Content-Type", "value": "application/json"})
        bruto = json.dumps(corpo, ensure_ascii=False, indent=2)
        bruto = re.sub(r'"(\{\{\w+Id\}\})"', r"\1", bruto)  # ids vão como número, não como texto
        item["request"]["body"] = {"mode": "raw", "raw": bruto, "options": {"raw": {"language": "json"}}}
    return item


def pasta(nome, descricao, itens):
    return {"name": nome, "description": descricao, "item": itens}


preparacao = pasta("00 Preparação", "Restaura a massa fictícia e obtém ids e datas usados nas próximas requisições.", [
    req("Restaurar dados fictícios (administrador)", "POST", "{{baseUrl}}/api/dev/reset", JS_DATAS + """
pm.test('HTTP 200', () => pm.response.to.have.status(200));
pm.test('massa restaurada: 3 barbeiros, 5 serviços, 10 clientes, 5 agendamentos', () => {
    pm.expect(pm.response.json()).to.eql({ barbeiros: 3, servicos: 5, clientes: 10, agendamentos: 5 });
});
// Data dos novos agendamentos: 7 dias à frente (pulando domingo), longe dos agendamentos da massa.
const d = new Date(); d.setDate(d.getDate() + 7); if (d.getDay() === 0) { d.setDate(d.getDate() + 1); }
pm.collectionVariables.set('dataAgendamento', formatarData(d));
pm.collectionVariables.set('sufixo', String(Date.now()));
""", auth=ADMIN),
    req("Listar barbeiros ativos", "GET", "{{baseUrl}}/api/barbeiros", """
pm.test('HTTP 200', () => pm.response.to.have.status(200));
const lista = pm.response.json();
pm.test('contrato: lista de {id: número, nome: texto, ativo: verdadeiro}', () => {
    pm.expect(lista).to.be.an('array').that.is.not.empty;
    lista.forEach(b => { pm.expect(b.id).to.be.a('number'); pm.expect(b.nome).to.be.a('string'); pm.expect(b.ativo).to.eql(true); });
});
pm.test('RN-10: barbeiro inativo (Diego Máquina) não é listado', () => pm.expect(lista.map(b => b.nome)).to.not.include('Diego Máquina'));
pm.collectionVariables.set('carlosId', lista.find(b => b.nome === 'Carlos Navalha').id);
pm.collectionVariables.set('rafaelId', lista.find(b => b.nome === 'Rafael Tesoura').id);
"""),
    req("Listar serviços ativos", "GET", "{{baseUrl}}/api/servicos", """
pm.test('HTTP 200', () => pm.response.to.have.status(200));
const lista = pm.response.json();
pm.test('contrato: duracaoMinutos e preco numéricos', () => lista.forEach(s => {
    pm.expect(s.duracaoMinutos).to.be.a('number'); pm.expect(s.preco).to.be.a('number');
}));
pm.test('RN-10: serviço inativo (Relaxamento capilar) não é listado', () => pm.expect(lista.map(s => s.nome)).to.not.include('Relaxamento capilar'));
pm.collectionVariables.set('corteId', lista.find(s => s.nome === 'Corte de cabelo').id);
"""),
])

clientes = pasta("01 Clientes — POST /api/clientes", "Operação crítica de cadastro: fluxo positivo e negativos.", [
    req("CT-001 / RF-01 — cadastrar cliente válido", "POST", "{{baseUrl}}/api/clientes", """
pm.test('HTTP 201 Created', () => pm.response.to.have.status(201));
const c = pm.response.json();
pm.test('contrato: id, nome, telefone, email, dataCadastro', () => {
    pm.expect(c).to.have.all.keys('id', 'nome', 'telefone', 'email', 'dataCadastro');
    pm.expect(c.id).to.be.a('number');
    pm.expect(c.dataCadastro).to.match(/^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}/);
});
pm.test('nome sem espaços nas pontas e e-mail em minúsculas', () => {
    pm.expect(c.nome).to.eql('Cliente Postman');
    pm.expect(c.email).to.eql(('postman.' + pm.collectionVariables.get('sufixo') + '@exemplo.com'));
});
pm.test('cabeçalho Location aponta para o cliente criado', () => pm.expect(pm.response.headers.get('Location')).to.match(new RegExp('/api/clientes/' + c.id + '$')));
pm.collectionVariables.set('clienteEmail', c.email);
""", corpo={"nome": "  Cliente Postman ", "telefone": "14988887777", "email": "Postman.{{sufixo}}@Exemplo.com"}),
    req("CT-005 / RF-01 — e-mail em formato inválido", "POST", "{{baseUrl}}/api/clientes", JS_CONTRATO_ERRO + """
pm.test('HTTP 400', () => pm.response.to.have.status(400));
const e = pm.response.json();
pm.test('contrato de erro padronizado, sem detalhes internos', () => verificarContratoDeErro(e, 400));
pm.test('mensagem do campo email', () => pm.expect(e.campos.email).to.eql('O e-mail informado é inválido.'));
""", corpo={"nome": "Paula Teste", "telefone": "14988776655", "email": "paula@exemplo"}),
    req("CT-006 / RF-01 — e-mail já cadastrado (em maiúsculas)", "POST", "{{baseUrl}}/api/clientes", JS_CONTRATO_ERRO + """
pm.test('HTTP 409 Conflict', () => pm.response.to.have.status(409));
const e = pm.response.json();
pm.test('contrato de erro padronizado', () => verificarContratoDeErro(e, 409));
pm.test('mensagem de e-mail repetido', () => pm.expect(e.mensagem).to.eql('Já existe um cliente cadastrado com este e-mail.'));
""", corpo={"nome": "Ana Repetida", "telefone": "14988776655", "email": "ANA.ROCHA@EXEMPLO.COM"}),
])

encadeado = pasta("02 Agendamento encadeado", "Cadastrar → agendar → consultar → cancelar, reaproveitando e-mail e código de acesso.", [
    req("CT-010 / RF-03 — agendar para o cliente recém-cadastrado", "POST", "{{baseUrl}}/api/agendamentos", JS_DATAS + """
pm.test('HTTP 201 Created', () => pm.response.to.have.status(201));
const a = pm.response.json();
const inicio = pm.collectionVariables.get('dataAgendamento') + 'T10:00:00';
pm.test('código de acesso com 8 caracteres do alfabeto sem ambíguos', () => pm.expect(a.codigoAcesso).to.match(/^[A-HJKMNP-Z2-9]{8}$/));
pm.test('status AGENDADO, término = início + 30 min', () => {
    pm.expect(a.status).to.eql('AGENDADO');
    pm.expect(a.dataHoraInicio).to.eql(inicio);
    pm.expect(a.dataHoraFim).to.eql(somarMinutos(inicio, 30));
});
pm.test('dados encadeados: cliente, barbeiro e serviço corretos', () => {
    pm.expect(a.clienteEmail).to.eql(pm.collectionVariables.get('clienteEmail'));
    pm.expect(a.barbeiroId).to.eql(Number(pm.collectionVariables.get('carlosId')));
    pm.expect(a.servicoNome).to.eql('Corte de cabelo');
});
pm.test('Location aponta para o código de acesso', () => pm.expect(pm.response.headers.get('Location')).to.match(new RegExp('/api/agendamentos/' + a.codigoAcesso + '$')));
pm.collectionVariables.set('codigoAcesso', a.codigoAcesso);
""", corpo={"emailCliente": "{{clienteEmail}}", "barbeiroId": "{{carlosId}}", "servicoId": "{{corteId}}",
            "dataHoraInicio": "{{dataAgendamento}}T10:00:00"}),
    req("CT-023 / RF-05 — consultar pelo código de acesso e e-mail", "GET",
        "{{baseUrl}}/api/agendamentos/{{codigoAcesso}}?email={{clienteEmail}}", """
pm.test('HTTP 200', () => pm.response.to.have.status(200));
const a = pm.response.json();
pm.test('é o agendamento criado, ainda AGENDADO', () => {
    pm.expect(a.codigoAcesso).to.eql(pm.collectionVariables.get('codigoAcesso'));
    pm.expect(a.status).to.eql('AGENDADO');
});
"""),
    req("CT-025 / RF-05 — cancelar o agendamento", "PATCH", "{{baseUrl}}/api/agendamentos/{{codigoAcesso}}/cancelar", """
pm.test('HTTP 200', () => pm.response.to.have.status(200));
pm.test('status CANCELADO', () => pm.expect(pm.response.json().status).to.eql('CANCELADO'));
""", corpo={"email": "{{clienteEmail}}"}),
    req("CT-026 / RF-05 — cancelar de novo é recusado", "PATCH", "{{baseUrl}}/api/agendamentos/{{codigoAcesso}}/cancelar", JS_CONTRATO_ERRO + """
pm.test('HTTP 409', () => pm.response.to.have.status(409));
const e = pm.response.json();
pm.test('contrato de erro padronizado', () => verificarContratoDeErro(e, 409));
pm.test('mensagem de transição inválida', () => pm.expect(e.mensagem).to.eql('Somente agendamentos com status AGENDADO podem ser cancelados.'));
""", corpo={"email": "{{clienteEmail}}"}),
])

regras = pasta("03 Regras de agendamento — POST /api/agendamentos", "Negativos e fronteiras da operação crítica de agendamento.", [
    req("Obter SEMENTE3 (base dos testes de conflito)", "GET", "{{baseUrl}}/api/agendamentos/SEMENTE3?email=bruno.lima@exemplo.com", JS_DATAS + """
pm.test('HTTP 200', () => pm.response.to.have.status(200));
const a = pm.response.json();
pm.test('SEMENTE3 é do Rafael Tesoura, 60 min, AGENDADO', () => {
    pm.expect(a.barbeiroId).to.eql(Number(pm.collectionVariables.get('rafaelId')));
    pm.expect(a.duracaoMinutos).to.eql(60);
    pm.expect(a.status).to.eql('AGENDADO');
});
pm.collectionVariables.set('dataSemente3', a.dataHoraInicio.substring(0, 10));
pm.collectionVariables.set('horarioConflito', somarMinutos(a.dataHoraInicio, 30));
pm.collectionVariables.set('horarioEncostado', a.dataHoraFim);
"""),
    req("CT-019 / RF-04 — sobreposição com agendamento do mesmo barbeiro", "POST", "{{baseUrl}}/api/agendamentos", JS_CONTRATO_ERRO + """
pm.test('HTTP 409', () => pm.response.to.have.status(409));
const e = pm.response.json();
pm.test('contrato de erro padronizado', () => verificarContratoDeErro(e, 409));
pm.test('mensagem de horário ocupado', () => pm.expect(e.mensagem).to.eql('O barbeiro já possui agendamento nesse horário.'));
""", corpo={"emailCliente": "joao.mendes@exemplo.com", "barbeiroId": "{{rafaelId}}", "servicoId": "{{corteId}}",
            "dataHoraInicio": "{{horarioConflito}}"}),
    req("CT-020 / RF-04 — horário encostado no término é aceito", "POST", "{{baseUrl}}/api/agendamentos", """
pm.test('HTTP 201', () => pm.response.to.have.status(201));
pm.test('começa exatamente quando o outro termina', () => pm.expect(pm.response.json().dataHoraInicio).to.eql(pm.collectionVariables.get('horarioEncostado')));
""", corpo={"emailCliente": "joao.mendes@exemplo.com", "barbeiroId": "{{rafaelId}}", "servicoId": "{{corteId}}",
            "dataHoraInicio": "{{horarioEncostado}}"}),
    req("CT-012 / RF-03 — início às 08:30 é recusado", "POST", "{{baseUrl}}/api/agendamentos", JS_CONTRATO_ERRO + """
pm.test('HTTP 400', () => pm.response.to.have.status(400));
const e = pm.response.json();
pm.test('contrato de erro padronizado', () => verificarContratoDeErro(e, 400));
pm.test('erro no campo dataHoraInicio', () => pm.expect(e.campos.dataHoraInicio).to.eql('O atendimento deve ocorrer entre 09:00 e 19:00 e o serviço precisa terminar até 19:00.'));
""", corpo={"emailCliente": "joao.mendes@exemplo.com", "barbeiroId": "{{carlosId}}", "servicoId": "{{corteId}}",
            "dataHoraInicio": "{{dataAgendamento}}T08:30:00"}),
    req("CT-018 / RF-03 — e-mail não cadastrado", "POST", "{{baseUrl}}/api/agendamentos", JS_CONTRATO_ERRO + """
pm.test('HTTP 404', () => pm.response.to.have.status(404));
const e = pm.response.json();
pm.test('contrato de erro padronizado', () => verificarContratoDeErro(e, 404));
pm.test('mensagem orienta o cadastro', () => pm.expect(e.mensagem).to.eql('Cliente não encontrado para o e-mail informado. Faça o cadastro antes de agendar.'));
""", corpo={"emailCliente": "nao.cadastrado.{{sufixo}}@exemplo.com", "barbeiroId": "{{carlosId}}", "servicoId": "{{corteId}}",
            "dataHoraInicio": "{{dataAgendamento}}T15:00:00"}),
])

MSG_NAO_ENCONTRADO = "Agendamento não encontrado para o código de acesso e o e-mail informados."
consulta = pasta("04 Consulta — GET /api/agendamentos/{codigo}", "Negativos da consulta pelo cliente (tabela de decisão do P04).", [
    req("CT-024 / RF-05 — código certo, e-mail de outro cliente", "GET", "{{baseUrl}}/api/agendamentos/SEMENTE2?email=bruno.lima@exemplo.com", JS_CONTRATO_ERRO + f"""
pm.test('HTTP 404', () => pm.response.to.have.status(404));
pm.test('contrato e mensagem sem revelar o agendamento', () => {{
    verificarContratoDeErro(pm.response.json(), 404);
    pm.expect(pm.response.json().mensagem).to.eql('{MSG_NAO_ENCONTRADO}');
    pm.expect(pm.response.text()).to.not.include('Ana Beatriz');
}});
"""),
    req("CT-024 / RF-05 — número sequencial no lugar do código", "GET", "{{baseUrl}}/api/agendamentos/1?email=ana.rocha@exemplo.com", f"""
pm.test('HTTP 404', () => pm.response.to.have.status(404));
pm.test('mesma mensagem', () => pm.expect(pm.response.json().mensagem).to.eql('{MSG_NAO_ENCONTRADO}'));
"""),
])

seguranca = pasta("05 Segurança — sem credenciais (CT-029)", "Área administrativa e dados pessoais não podem ser acessados sem login (RN-11, RNF-02).", [
    req("CT-029 / RF-06 — listar barbeiros (admin) sem credenciais", "GET", "{{baseUrl}}/api/admin/barbeiros", JS_CONTRATO_ERRO + """
pm.test('HTTP 401', () => pm.response.to.have.status(401));
const e = pm.response.json();
pm.test('corpo é só o erro padronizado, sem dados', () => { verificarContratoDeErro(e, 401); pm.expect(e.mensagem).to.eql('Autenticação necessária.'); });
"""),
    req("CT-029 / RF-06 — listar clientes sem credenciais", "GET", "{{baseUrl}}/api/clientes", """
pm.test('HTTP 401', () => pm.response.to.have.status(401));
pm.test('nenhum e-mail de cliente no corpo', () => pm.expect(pm.response.text()).to.not.include('@exemplo.com'));
"""),
    req("CT-029 / RF-06 — cadastrar serviço sem credenciais", "POST", "{{baseUrl}}/api/admin/servicos", """
pm.test('HTTP 403 (token CSRF verificado antes da autenticação)', () => pm.response.to.have.status(403));
""", corpo={"nome": "Serviço Invasor", "duracaoMinutos": 30, "preco": 10.00}),
    req("CT-029 / RF-06 — serviço invasor não foi criado", "GET", "{{baseUrl}}/api/servicos", """
pm.test('HTTP 200', () => pm.response.to.have.status(200));
pm.test('"Serviço Invasor" não existe', () => pm.expect(pm.response.json().map(s => s.nome)).to.not.include('Serviço Invasor'));
"""),
])

admin = pasta("06 Administração — HTTP Basic", "Cadastro de serviço e agenda do dia com credencial (fictícia) de administrador.", [
    req("RF-07 — cadastrar serviço válido", "POST", "{{baseUrl}}/api/admin/servicos", """
pm.test('HTTP 201', () => pm.response.to.have.status(201));
const s = pm.response.json();
pm.test('contrato do serviço', () => {
    pm.expect(s).to.have.all.keys('id', 'nome', 'duracaoMinutos', 'preco', 'ativo');
    pm.expect(s.preco).to.eql(55.9);
    pm.expect(s.ativo).to.eql(true);
});
pm.collectionVariables.set('servicoTemporarioId', s.id);
""", corpo={"nome": "Hidratação Postman", "duracaoMinutos": 45, "preco": 55.90}, auth=ADMIN),
    req("CT-031 / RF-07 — duração não múltipla de 15", "POST", "{{baseUrl}}/api/admin/servicos", JS_CONTRATO_ERRO + """
pm.test('HTTP 400', () => pm.response.to.have.status(400));
const e = pm.response.json();
pm.test('erro no campo duracaoMinutos', () => { verificarContratoDeErro(e, 400); pm.expect(e.campos.duracaoMinutos).to.eql('A duração deve ser múltipla de 15 minutos.'); });
""", corpo={"nome": "Serviço Limite", "duracaoMinutos": 20, "preco": 10.00}, auth=ADMIN),
    req("RF-07 — excluir serviço sem agendamentos", "DELETE", "{{baseUrl}}/api/admin/servicos/{{servicoTemporarioId}}", """
pm.test('HTTP 204 No Content', () => pm.response.to.have.status(204));
""", auth=ADMIN),
    req("RF-08 — agenda do dia não expõe códigos de acesso", "GET",
        "{{baseUrl}}/api/admin/agenda?barbeiroId={{rafaelId}}&data={{dataSemente3}}", """
pm.test('HTTP 200', () => pm.response.to.have.status(200));
const agenda = pm.response.json();
pm.test('lista os agendamentos do dia em ordem de horário', () => {
    pm.expect(agenda.length).to.be.at.least(2);
    const inicios = agenda.map(a => a.dataHoraInicio);
    pm.expect(inicios).to.eql([...inicios].sort());
});
pm.test('nenhum agendamento traz codigoAcesso', () => agenda.forEach(a => pm.expect(a).to.not.have.property('codigoAcesso')));
""", auth=ADMIN),
])

limpeza = pasta("07 Limpeza", "Deixa o ambiente como estava.", [
    req("Restaurar dados fictícios ao final", "POST", "{{baseUrl}}/api/dev/reset", """
pm.test('HTTP 200', () => pm.response.to.have.status(200));
""", auth=ADMIN),
])

colecao = {
    "info": {
        "name": "BarberAgenda — testes de integração/API",
        "description": "Projeto Integrado P2 (Testes e Qualidade de Software). Cada requisição indica o caso de teste (CT) "
                       "e o requisito (RF) que representa. Dados fictícios; credencial de administrador fictícia no ambiente. "
                       "Gerada por scripts/gerar_colecao_postman.py.",
        "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
    },
    "auth": SEM_AUTH,
    "item": [preparacao, clientes, encadeado, regras, consulta, seguranca, admin, limpeza],
    "variable": [{"key": k, "value": ""} for k in (
        "dataAgendamento", "sufixo", "carlosId", "rafaelId", "corteId", "clienteEmail", "codigoAcesso",
        "dataSemente3", "horarioConflito", "horarioEncostado", "servicoTemporarioId")],
}

ambiente = {
    "name": "BarberAgenda — local",
    "values": [
        {"key": "baseUrl", "value": "http://localhost:8080", "type": "default", "enabled": True},
        {"key": "adminUsuario", "value": "admin", "type": "default", "enabled": True},
        {"key": "adminSenha", "value": "admin123", "type": "secret", "enabled": True},
    ],
    "_postman_variable_scope": "environment",
}

sys.stdout.reconfigure(encoding="utf-8")
PASTA.mkdir(exist_ok=True)
(PASTA / "BarberAgenda.postman_collection.json").write_text(json.dumps(colecao, ensure_ascii=False, indent=2), encoding="utf-8")
(PASTA / "BarberAgenda.postman_environment.json").write_text(json.dumps(ambiente, ensure_ascii=False, indent=2), encoding="utf-8")
total = sum(len(p["item"]) for p in colecao["item"])
print(f"Coleção gerada: {total} requisições em {len(colecao['item'])} pastas")
