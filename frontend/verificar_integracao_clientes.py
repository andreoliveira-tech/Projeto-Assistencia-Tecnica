"""Validação integrada opt-in: cria e exclui somente um cliente descartável novo.

Não é coletado pela suíte local. Sem --executar, apenas apresenta o escopo.
Não reutiliza nem exclui clientes encontrados antes do início da execução.
"""

import argparse
import json
import os
from pathlib import Path
import sys
from unittest.mock import patch

sys.dont_write_bytecode = True
import requests
from requests.adapters import HTTPAdapter

BASE = "https://x8ki-letl-twmt.n7.xano.io/api:assistencia-tecnica-clientes"
FICTICIO = {
    "nome": "T35-EXCLUSAO-20261026-01", "cpf": "52998224725",
    "telefone": "11900000000", "email": "t35-exclusao-20261026-01@example.invalid",
}


class EscopoDescartavel:
    def __init__(self, transporte):
        self.transporte = transporte
        self.anteriores = None
        self.id_criado = None
        self.posts = 0
        self.deletes = 0
        self.permitir_delete = False
        self.chamadas = []

    def request(self, session, method, url, **kwargs):
        method = method.upper()
        lista = BASE + "/clientes"
        individual = lista + f"/{self.id_criado}" if self.id_criado is not None else None
        if kwargs.get("allow_redirects") is not False or kwargs.get("timeout") != (5, 20):
            raise RuntimeError("Timeout e bloqueio de redirecionamento obrigatórios.")
        if method == "GET" and url in (lista, individual):
            pass
        elif method == "POST" and url == lista:
            if self.posts or self.anteriores is None or kwargs.get("json") != FICTICIO:
                raise RuntimeError("POST fora do escopo descartável.")
            if any(item.get("nome") == FICTICIO["nome"] for item in self.anteriores):
                raise RuntimeError("Já existe registro com o marcador; não será reutilizado.")
            self.posts += 1
        elif method == "DELETE" and url == individual and self.id_criado is not None:
            if not self.permitir_delete or self.deletes or any(
                item["id_cliente"] == self.id_criado for item in self.anteriores
            ):
                raise RuntimeError("DELETE fora do escopo descartável.")
            self.deletes += 1
        else:
            raise RuntimeError("Operação fora da lista permitida.")
        session.trust_env = False
        session.mount("https://", HTTPAdapter(max_retries=0))
        response = self.transporte(session, method, url, **kwargs)
        self.chamadas.append({"metodo": method, "rota": url.removeprefix(BASE), "http": response.status_code})
        if method == "POST":
            if response.status_code != 200:
                raise RuntimeError("Cadastro sem HTTP 200; sem nova tentativa.")
            item = response.json()
            identificador = item.get("id_cliente") if isinstance(item, dict) else None
            if (
                type(identificador) is not int or identificador <= 0
                or any(cliente["id_cliente"] == identificador for cliente in self.anteriores)
                or any(item.get(campo) != valor for campo, valor in FICTICIO.items())
            ):
                raise RuntimeError("Identidade do registro novo não comprovada; exclusão proibida.")
            self.id_criado = identificador
            print(json.dumps({"cliente_descartavel_criado": identificador, "marcador": FICTICIO["nome"]}), flush=True)
        return response


def executar():
    from streamlit.testing.v1 import AppTest

    root = Path(__file__).resolve().parent
    escopo = EscopoDescartavel(requests.sessions.Session.request)
    evidencia = {"workspace": 149143, "branch": "v1", "grupo": 436987}
    with patch.dict(os.environ, {"XANO_CLIENTES_API_BASE_URL": BASE,
                                  "STREAMLIT_BROWSER_GATHER_USAGE_STATS": "false"}), patch.object(
        requests.sessions.Session, "request", autospec=True, side_effect=escopo.request
    ):
        app = AppTest.from_file(str(root / "app.py"), default_timeout=90).run()

        def conferir(condicao, mensagem):
            if not condicao:
                raise RuntimeError(mensagem)

        def clicar(rotulo):
            next(button for button in app.button if button.label == rotulo).click().run()
            conferir(not app.exception, "Erro na interface; cenário interrompido.")

        conferir(not app.exception, "Inicialização falhou.")
        conferir(not escopo.chamadas, "Abertura não pode chamar o backend.")
        evidencia["inicializacao_sem_chamadas"] = True
        clicar("Atualizar lista")
        anteriores = app.session_state["clientes_listagem"]["dados"]
        conferir(isinstance(anteriores, list), "Não foi possível obter o baseline.")
        escopo.anteriores = anteriores
        evidencia["clientes_anteriores"] = len(anteriores)

        for campo, valor in FICTICIO.items():
            app.text_input(key=campo).set_value(valor)
        clicar("Cadastrar")
        conferir(escopo.id_criado is not None and bool(app.success), "Cadastro não confirmado.")
        evidencia["cadastro_pela_interface"] = True
        app.text_input(key="exclusao_selecao_id").set_value(str(escopo.id_criado)).run()
        clicar("Carregar para exclusão")
        carregado = app.session_state["cliente_exclusao"]["dados"]
        conferir(carregado and carregado["id_cliente"] == escopo.id_criado, "Cliente não carregado.")
        conferir(all(carregado[campo] == valor for campo, valor in FICTICIO.items()), "Dados divergentes.")
        conferir(app.button(key="excluir_definitivamente").disabled, "Confirmação ausente não bloqueou exclusão.")
        chamadas = len(escopo.chamadas)
        app.checkbox[0].check().run()
        conferir(len(escopo.chamadas) == chamadas, "Marcar confirmação chamou o backend.")
        escopo.permitir_delete = True
        clicar("Excluir definitivamente")
        conferir(escopo.deletes == 1, "Número de DELETEs inesperado.")
        conferir(app.session_state["cliente_exclusao"]["sucesso"], "Ausência não confirmada pelo frontend.")
        conferir(app.session_state["clientes_listagem"]["dados"] is None, "Listagem não invalidada.")
        evidencia["exclusao_e_get_posterior_confirmados"] = True
        chamadas = len(escopo.chamadas)
        app.run()
        conferir(not app.exception and len(escopo.chamadas) == chamadas, "Rerun executou operação adicional.")
        clicar("Atualizar lista")
        posteriores = app.session_state["clientes_listagem"]["dados"]
        comparar = lambda itens: sorted(itens, key=lambda item: item["id_cliente"])
        conferir(isinstance(posteriores, list) and comparar(posteriores) == comparar(anteriores),
                 "Baseline de clientes divergente; nenhuma correção automática será feita.")
        evidencia.update(
            id_descartavel=escopo.id_criado, clientes_preexistentes_preservados=True,
            posts=escopo.posts, deletes=escopo.deletes, chamadas=escopo.chamadas,
        )
        print(json.dumps(evidencia, ensure_ascii=True, indent=2), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--executar", action="store_true")
    args = parser.parse_args()
    if not args.executar:
        print("Planejado: GET lista, POST descartável, GET próprio, DELETE próprio, GET de ausência, GET lista.")
        print("A execução real exige --executar e autorização prévia para o cenário.")
    else:
        try:
            executar()
        except Exception:
            print("Cenário interrompido. Sem repetição, recuperação ou exclusão adicional automática.", flush=True)
            sys.exit(1)
