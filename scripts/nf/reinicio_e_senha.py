"""
TNF-05 (RNF-04) — Confiabilidade: dados criados antes de uma parada da aplicação continuam disponíveis após reiniciar.
TNF-03 (RNF-02) — Segurança: a senha do administrador está gravada no banco somente como hash BCrypt.

O script sobe a aplicação (perfil dev) com um banco H2 em arquivo temporário e porta 8099, cria dados, encerra o
processo, consulta o arquivo do banco com o H2 Shell, sobe de novo e confere os dados.
Uso:  python scripts/nf/reinicio_e_senha.py <pasta_evidencias>   (requer target/barberagenda-*.jar e JAVA_HOME)
"""
import glob
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import comum  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
PORTA = 8099
BASE = f"http://localhost:{PORTA}"


def java():
    home = os.environ.get("JAVA_HOME")
    return str(Path(home) / "bin" / "java") if home else "java"


def subir(arquivo_banco, log):
    jar = sorted(glob.glob(str(RAIZ / "target" / "barberagenda-*.jar")))[-1]
    proc = subprocess.Popen([java(), "-jar", jar, "--spring.profiles.active=dev", f"--server.port={PORTA}",
                             f"--spring.datasource.url=jdbc:h2:file:{arquivo_banco}"], stdout=log, stderr=subprocess.STDOUT)
    assert comum.aguardar(BASE), "aplicação não subiu"
    return proc


def parar(proc):
    proc.terminate()
    proc.wait(timeout=60)


def consultar_banco(arquivo_banco, sql):
    jar_h2 = glob.glob(str(Path.home() / ".m2/repository/com/h2database/h2/*/h2-*.jar"))[-1]
    saida = subprocess.run([java(), "-cp", jar_h2, "org.h2.tools.Shell", "-url", f"jdbc:h2:file:{arquivo_banco}",
                            "-user", "sa", "-password", "", "-sql", sql], capture_output=True, text=True, timeout=60)
    return saida.stdout


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    destino = Path(sys.argv[1])
    destino.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as pasta, open(destino / "TNF-05_aplicacao.log", "w", encoding="utf-8") as log:
        banco = Path(pasta, "barberagenda").as_posix()
        registro = {"inicio": comum.agora(), "porta": PORTA, "perfil": "dev", "banco": "H2 em arquivo temporário"}

        proc = subir(banco, log)
        barbeiros, servicos = comum.ids(BASE)
        email = f"reinicio.{int(time.time())}@exemplo.com"
        cli = comum.chamar(BASE, "POST", "/api/clientes", {"nome": "Cliente Reinício", "telefone": "14911112222", "email": email})
        data = comum.dias_de_funcionamento(7, 1)[0]
        ag = comum.chamar(BASE, "POST", "/api/agendamentos", {"emailCliente": email, "barbeiroId": barbeiros["Carlos Navalha"],
                                                              "servicoId": servicos["Corte de cabelo"], "dataHoraInicio": f"{data}T15:00:00"})
        antes = {"cliente": cli.json(), "agendamento": ag.json()}
        registro["criado_antes_da_parada"] = {"cliente_status": cli.status, "agendamento_status": ag.status,
                                              "codigoAcesso": antes["agendamento"].get("codigoAcesso")}
        time.sleep(3)  # aguarda a gravação periódica do H2 antes de encerrar o processo
        parar(proc)
        registro["parada"] = "processo encerrado (terminate) às " + comum.agora()

        # TNF-03: senha armazenada no banco (consulta direta ao arquivo, com a aplicação parada)
        saida = consultar_banco(banco, "SELECT LOGIN, SENHA_HASH FROM USUARIO")
        linha = next((l for l in saida.splitlines() if l.startswith("admin")), "")
        hash_salvo = linha.split("|")[-1].strip() if "|" in linha else ""
        registro["senha"] = {"prefixo_hash": hash_salvo[:7], "tamanho_hash": len(hash_salvo),
                             "texto_original_no_banco": "admin123" in saida,
                             "bcrypt": hash_salvo.startswith(("$2a$", "$2b$", "$2y$")) and len(hash_salvo) == 60}

        proc = subir(banco, log)
        depois = comum.chamar(BASE, "GET", f"/api/agendamentos/{antes['agendamento']['codigoAcesso']}?email={email}")
        parar(proc)
        registro["depois_do_reinicio"] = {"status": depois.status, "dados": depois.json()}
        iguais = depois.status == 200 and all(depois.json()[k] == antes["agendamento"][k] for k in
                                              ("codigoAcesso", "clienteEmail", "barbeiroId", "servicoId", "dataHoraInicio", "status"))
        registro["TNF-05_atende"] = iguais
        registro["TNF-03_atende"] = registro["senha"]["bcrypt"] and not registro["senha"]["texto_original_no_banco"]
        registro["fim"] = comum.agora()

    (destino / "TNF-05_TNF-03_resultado.json").write_text(json.dumps(registro, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"TNF-05 persistência após reinício: {'ATENDE' if registro['TNF-05_atende'] else 'NÃO ATENDE'}")
    print(f"TNF-03 senha com hash BCrypt: {'ATENDE' if registro['TNF-03_atende'] else 'NÃO ATENDE'} "
          f"(prefixo {registro['senha']['prefixo_hash']}, {registro['senha']['tamanho_hash']} caracteres)")


if __name__ == "__main__":
    main()
