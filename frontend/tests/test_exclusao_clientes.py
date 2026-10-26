"""Testes locais da exclusão e regressões de CRUD; HTTP simulado e sockets bloqueados."""

import json
import os
from pathlib import Path
import socket
import sys
import threading
import unittest
from unittest.mock import Mock, patch

sys.dont_write_bytecode = True
FRONTEND = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(FRONTEND))

import requests
from streamlit.testing.v1 import AppTest

import clientes_api as api


BASE = "https://clientes.example.invalid/api:teste"
CLIENTE = {
    "id_cliente": 1001, "nome": "Cliente fictício", "cpf": "00000000000",
    "telefone": "00000000000", "email": "cliente@example.invalid",
}
BLOQUEIO = "Cliente possui equipamentos vinculados. Exclusao bloqueada."
NAO_ENCONTRADO = {"code": "ERROR_CODE_NOT_FOUND", "message": "Cliente não encontrado."}


def resposta(status=200, payload=None, invalida=False):
    response = requests.Response()
    response.status_code = status
    response._content = b"nao-json" if invalida else json.dumps(payload).encode("utf-8")
    response.encoding = "utf-8"
    return response


class SemRede(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.bloqueios = []
        # No Windows, asyncio/AppTest usa TCP loopback dentro de socketpair para
        # sinalização interna. Apenas essa chamada síncrona é permitida; não HTTP.
        original_pair = socket.socketpair
        original_connect = socket.socket.connect
        local = threading.local()
        bloqueio_connect = Mock(side_effect=AssertionError("Rede real proibida nos testes"))
        self.bloqueios.append(bloqueio_connect)

        def par_interno(*args, **kwargs):
            local.socketpair = True
            try:
                return original_pair(*args, **kwargs)
            finally:
                local.socketpair = False

        def conectar(sock, address):
            if (
                getattr(local, "socketpair", False)
                and isinstance(address, tuple)
                and address[0] in ("127.0.0.1", "::1")
            ):
                return original_connect(sock, address)
            return bloqueio_connect(sock, address)

        for target, replacement in (
            ("socket.socketpair", par_interno), ("socket.socket.connect", conectar),
        ):
            guard = patch(target, new=replacement)
            guard.start()
            self.addCleanup(guard.stop)
        for target in ("socket.socket.connect_ex", "socket.getaddrinfo"):
            blocker = patch(target, side_effect=AssertionError("Rede real proibida nos testes"))
            self.bloqueios.append(blocker.start())
            self.addCleanup(blocker.stop)
        http = patch(
            "requests.sessions.Session.request",
            side_effect=AssertionError("HTTP não previsto no teste"),
        )
        self.http = http.start()
        self.addCleanup(http.stop)

    def tearDown(self):
        try:
            for blocker in self.bloqueios:
                blocker.assert_not_called()
        finally:
            super().tearDown()


class ClienteHttpTests(SemRede):
    def test_get_de_confirmacao_reconhece_404_do_cliente(self):
        self.http.side_effect = None
        self.http.return_value = resposta(404, NAO_ENCONTRADO)
        with self.assertRaises(api.ClienteNaoEncontradoError):
            api.consultar_cliente(BASE, 1001, confirmar_ausencia=True)
        self.http.assert_called_once_with(
            method="get", url=BASE + "/clientes/1001",
            params=None, timeout=(5, 20), allow_redirects=False,
        )

    def test_get_de_confirmacao_recusa_404_ambiguo(self):
        for payload in (
            None, [], "Not found", {},
            {"message": "Cliente não encontrado."},
            {"code": "OUTRO_CODIGO", "message": "Cliente não encontrado."},
            {"code": "error_code_not_found", "message": "Cliente não encontrado."},
            {"code": "ERROR_CODE_NOT_FOUND ", "message": "Cliente não encontrado."},
            {"code": "ERROR_CODE_NOT_FOUND"},
            {"code": "ERROR_CODE_NOT_FOUND", "message": "Invalid app."},
            {"code": "ERROR_CODE_NOT_FOUND", "message": "Unable to locate request."},
        ):
            with self.subTest(payload=payload):
                self.http.reset_mock()
                self.http.side_effect = None
                self.http.return_value = resposta(404, payload)
                with self.assertRaises(api.ConsultaError) as captured:
                    api.consultar_cliente(BASE, 1001, confirmar_ausencia=True)
                self.assertNotIsInstance(captured.exception, api.ClienteNaoEncontradoError)
                self.http.assert_called_once()

    def test_get_de_confirmacao_recusa_404_com_json_invalido(self):
        self.http.side_effect = None
        self.http.return_value = resposta(404, invalida=True)
        with self.assertRaises(api.ConsultaError) as captured:
            api.consultar_cliente(BASE, 1001, confirmar_ausencia=True)
        self.assertNotIsInstance(captured.exception, api.ClienteNaoEncontradoError)
        self.http.assert_called_once()

    def test_get_de_confirmacao_preserva_cliente_existente_e_outros_erros(self):
        self.http.side_effect = None
        self.http.return_value = resposta(200, CLIENTE)
        self.assertEqual(api.consultar_cliente(BASE, 1001, confirmar_ausencia=True), CLIENTE)
        for status in (400, 408, 500):
            with self.subTest(status=status):
                self.http.return_value = resposta(status, NAO_ENCONTRADO)
                with self.assertRaises(api.ConsultaError) as captured:
                    api.consultar_cliente(BASE, 1001, confirmar_ausencia=True)
                self.assertNotIsInstance(captured.exception, api.ClienteNaoEncontradoError)

    def test_regressao_404_dos_fluxos_existentes(self):
        self.http.side_effect = None
        self.http.return_value = resposta(404)
        with self.assertRaises(api.ClienteNaoEncontradoError):
            api.consultar_cliente(BASE, 1001)
        with self.assertRaises(api.ClienteNaoEncontradoError):
            api.atualizar_cliente(BASE, 1001, CLIENTE)

    def test_identificador_invalido_nao_envia_http(self):
        for value in (None, True, False, 0, -1, "1001", 1.5):
            with self.subTest(value=value), self.assertRaises(api.ExclusaoError):
                api.excluir_cliente(BASE, value)
        self.http.assert_not_called()

    def test_sucesso_uma_tentativa_sem_corpo_e_sem_redirecionamento(self):
        self.http.side_effect = None
        self.http.return_value = resposta(200, {"id_cliente": 1001, "excluido": True})
        self.assertEqual(api.excluir_cliente(BASE + "/", 1001)["excluido"], True)
        self.http.assert_called_once_with(
            method="delete", url=BASE + "/clientes/1001",
            timeout=(5, 20), allow_redirects=False,
        )

    def test_bloqueio_distinto_de_outros_erros_400(self):
        self.http.side_effect = None
        self.http.return_value = resposta(400, {"code": "ERROR_CODE_INPUT_ERROR", "message": BLOQUEIO})
        with self.assertRaises(api.ExclusaoBloqueadaError) as captured:
            api.excluir_cliente(BASE, 1001)
        self.assertFalse(captured.exception.incerto)

        for payload in (
            {"message": "Nao foi possivel confirmar os vinculos do cliente."},
            {"message": "Informe um identificador inteiro positivo."}, {}, None,
        ):
            with self.subTest(payload=payload):
                self.http.return_value = resposta(400, payload)
                with self.assertRaises(api.ExclusaoError) as captured:
                    api.excluir_cliente(BASE, 1001)
                self.assertNotIsInstance(captured.exception, api.ExclusaoBloqueadaError)
                self.assertFalse(captured.exception.incerto)

    def test_404_cliente_nao_encontrado(self):
        self.http.side_effect = None
        self.http.return_value = resposta(404, None)
        with self.assertRaises(api.ClienteNaoEncontradoError):
            api.excluir_cliente(BASE, 1001)
        self.http.assert_called_once()

    def test_comunicacao_incerta_sem_repeticao(self):
        for error in (requests.Timeout(), requests.ConnectionError()):
            with self.subTest(error=type(error).__name__):
                self.http.reset_mock()
                self.http.side_effect = error
                with self.assertRaises(api.ExclusaoError) as captured:
                    api.excluir_cliente(BASE, 1001)
                self.assertTrue(captured.exception.incerto)
                self.http.assert_called_once()

    def test_http_408_incerto_independentemente_do_corpo_sem_repeticao(self):
        for response in (
            resposta(408, {"message": "Request timeout"}),
            resposta(408, invalida=True),
            resposta(408, {"id_cliente": 1001, "excluido": True}),
        ):
            with self.subTest(body=response.text):
                self.http.reset_mock()
                self.http.side_effect = None
                self.http.return_value = response
                with self.assertRaises(api.ExclusaoError) as captured:
                    api.excluir_cliente(BASE, 1001)
                self.assertTrue(captured.exception.incerto)
                self.assertIn("HTTP 408", str(captured.exception))
                self.assertNotIsInstance(captured.exception, api.ExclusaoBloqueadaError)
                self.http.assert_called_once()

    def test_respostas_incertas_sem_falso_sucesso(self):
        cases = [
            resposta(500, {}), resposta(302, {}), resposta(204),
            resposta(201, {"id_cliente": 1001, "excluido": True}),
            resposta(200, invalida=True), resposta(200, []), resposta(200, {}),
            resposta(200, {"id_cliente": 1002, "excluido": True}),
            resposta(200, {"id_cliente": "1001", "excluido": True}),
            resposta(200, {"id_cliente": True, "excluido": True}),
            resposta(200, {"id_cliente": 1001, "excluido": False}),
            resposta(200, {"id_cliente": 1001, "excluido": 1}),
        ]
        for response in cases:
            with self.subTest(status=response.status_code, body=response.text):
                self.http.reset_mock()
                self.http.side_effect = None
                self.http.return_value = response
                with self.assertRaises(api.ExclusaoError) as captured:
                    api.excluir_cliente(BASE, 1001)
                self.assertTrue(captured.exception.incerto)
                self.http.assert_called_once()


class InterfaceTests(SemRede):
    def setUp(self):
        super().setUp()
        env = patch.dict(os.environ, {
            "XANO_CLIENTES_API_BASE_URL": BASE,
            "STREAMLIT_BROWSER_GATHER_USAGE_STATS": "false",
        })
        env.start()
        self.addCleanup(env.stop)
        self.app = AppTest.from_file(str(FRONTEND / "app.py"), default_timeout=20).run()
        self.sem_excecoes()

    def sem_excecoes(self):
        self.assertEqual(len(self.app.exception), 0, str(self.app.exception))

    def clicar(self, label):
        next(button for button in self.app.button if button.label == label).click().run()
        self.sem_excecoes()

    def carregar(self, cliente=None):
        cliente = cliente or CLIENTE
        self.http.side_effect = None
        self.http.return_value = resposta(200, cliente)
        self.app.text_input(key="exclusao_selecao_id").set_value(str(cliente["id_cliente"])).run()
        self.clicar("Carregar para exclusão")

    def confirmar(self):
        self.app.checkbox[0].check().run()
        self.sem_excecoes()

    def excluir_com(self, responses):
        self.confirmar()
        self.http.reset_mock()
        self.http.side_effect = responses
        self.clicar("Excluir definitivamente")

    def metodos(self):
        return [call.kwargs["method"].lower() for call in self.http.call_args_list]

    def mensagens(self, element):
        return " ".join(item.value for item in getattr(self.app, element))

    def test_abertura_cancelamento_e_reruns_nao_excluem(self):
        self.http.assert_not_called()
        self.carregar()
        self.assertTrue(self.app.button(key="excluir_definitivamente").disabled)
        self.confirmar()
        self.http.reset_mock()
        self.app.run()
        self.clicar("Cancelar")
        self.app.run()
        self.http.assert_not_called()
        self.assertEqual(len(self.app.checkbox), 0)

    def test_ids_invalidos_sem_http(self):
        for texto in ("", "0", "-1", "abc", "1.5"):
            with self.subTest(texto=texto):
                self.app.text_input(key="exclusao_selecao_id").set_value(texto).run()
                self.clicar("Carregar para exclusão")
                self.assertIn("inteiro positivo", self.mensagens("error"))
        self.http.assert_not_called()

    def test_troca_de_selecao_descarta_confirmacao(self):
        self.carregar()
        self.confirmar()
        self.http.reset_mock()
        self.app.text_input(key="exclusao_selecao_id").set_value("1002").run()
        self.assertEqual(len(self.app.checkbox), 0)
        self.http.assert_not_called()
        self.carregar({**CLIENTE, "id_cliente": 1002})
        self.assertFalse(self.app.checkbox[0].value)
        self.assertTrue(self.app.button(key="excluir_definitivamente").disabled)

    def test_recarregar_e_trocar_url_exigem_nova_confirmacao(self):
        self.carregar()
        self.confirmar()
        self.clicar("Carregar para exclusão")
        self.assertFalse(self.app.checkbox[0].value)
        self.confirmar()
        self.http.reset_mock()
        with patch.dict(os.environ, {"XANO_CLIENTES_API_BASE_URL": BASE + "-outro"}):
            self.app.run()
            self.sem_excecoes()
            self.assertEqual(len(self.app.checkbox), 0)
            self.assertIsNone(self.app.session_state["cliente_exclusao"]["dados"])
        self.http.assert_not_called()

    def test_carregamento_404_e_falha_nao_habilitam_delete(self):
        self.app.text_input(key="exclusao_selecao_id").set_value("1001").run()
        self.http.side_effect = [resposta(404), requests.Timeout()]
        self.clicar("Carregar para exclusão")
        self.assertIn("Cliente não encontrado", self.mensagens("info"))
        self.clicar("Carregar para exclusão")
        self.assertIn("Tempo de resposta", self.mensagens("error"))
        self.assertEqual(len(self.app.checkbox), 0)
        self.assertEqual(self.metodos(), ["get", "get"])

    def test_sucesso_confirma_por_get_e_invalida_estados(self):
        self.carregar()
        self.app.session_state["clientes_listagem"] = {
            "base_url": BASE, "dados": [CLIENTE], "erro": None,
        }
        self.app.session_state["cliente_consulta"] = {
            "base_url": BASE, "id_cliente": 1001, "dados": CLIENTE,
            "erro": None, "nao_encontrado": False,
        }
        self.app.session_state["cliente_edicao"] = {
            "base_url": BASE, "id_cliente": 1001, "dados": CLIENTE,
            "geracao": 0, "confirmado": CLIENTE, "erro": None,
            "sucesso": True, "conferir": False,
        }
        self.excluir_com([resposta(200, {"id_cliente": 1001, "excluido": True}), resposta(404, NAO_ENCONTRADO)])
        self.assertEqual(self.metodos(), ["delete", "get"])
        self.assertIn("Exclusão confirmada", self.mensagens("success"))
        for key in ("clientes_listagem", "cliente_consulta", "cliente_edicao", "cliente_exclusao"):
            self.assertIsNone(self.app.session_state[key]["dados"])
        self.assertIsNone(self.app.session_state["cliente_edicao"]["confirmado"])
        self.assertFalse(self.app.session_state["cliente_edicao"]["sucesso"])
        self.http.reset_mock()
        self.app.run()
        self.http.assert_not_called()
        self.assertEqual(len(self.app.checkbox), 0)

    def test_bloqueio_preserva_estados_e_nao_consulta_apos_delete(self):
        self.carregar()
        self.app.session_state["clientes_listagem"] = {
            "base_url": BASE, "dados": [CLIENTE], "erro": None,
        }
        self.excluir_com([resposta(400, {"message": BLOQUEIO})])
        self.assertEqual(self.metodos(), ["delete"])
        self.assertIn("equipamentos vinculados", self.mensagens("error"))
        self.assertEqual(len(self.app.success), 0)
        self.assertEqual(self.app.session_state["clientes_listagem"]["dados"], [CLIENTE])
        self.assertEqual(len(self.app.checkbox), 0)
        self.http.reset_mock()
        self.app.run()
        self.http.assert_not_called()

    def test_erro_de_verificacao_nao_vira_bloqueio_por_equipamentos(self):
        self.carregar()
        self.excluir_com([resposta(400, {"message": "Nao foi possivel confirmar os vinculos do cliente."})])
        self.assertIn("Exclusão rejeitada", self.mensagens("error"))
        self.assertNotIn("equipamentos vinculados", self.mensagens("error"))
        self.assertEqual(len(self.app.success), 0)
        self.assertEqual(self.metodos(), ["delete"])

    def test_delete_404_nao_declara_sucesso(self):
        self.carregar()
        self.excluir_com([resposta(404)])
        self.assertIn("Cliente não encontrado", self.mensagens("info"))
        self.assertEqual(len(self.app.success), 0)
        self.assertEqual(self.metodos(), ["delete"])

    def test_incerto_exige_get_e_nova_confirmacao(self):
        self.carregar()
        self.excluir_com([requests.Timeout()])
        self.assertEqual(self.metodos(), ["delete"])
        self.assertIn("Tempo de resposta", self.mensagens("error"))
        self.assertTrue(self.app.button(key="carregar_exclusao").disabled)
        self.assertEqual(len(self.app.checkbox), 0)
        self.assertEqual(len(self.app.success), 0)
        self.http.reset_mock()
        self.app.run()
        self.http.assert_not_called()
        self.http.side_effect = [resposta(200, CLIENTE)]
        self.clicar("Conferir estado atual da exclusão")
        self.assertEqual(self.metodos(), ["get"])
        self.assertFalse(self.app.checkbox[0].value)
        self.assertTrue(self.app.button(key="excluir_definitivamente").disabled)

    def test_ausencia_apos_incerto_nao_atribui_sucesso_a_tentativa(self):
        self.carregar()
        self.excluir_com([requests.ConnectionError()])
        self.http.reset_mock()
        self.http.side_effect = [resposta(404, NAO_ENCONTRADO)]
        self.clicar("Conferir estado atual da exclusão")
        self.assertIn("não confirma que a tentativa anterior", self.mensagens("info"))
        self.assertEqual(len(self.app.success), 0)
        self.assertEqual(self.metodos(), ["get"])

    def test_http_408_bloqueia_reenvio_e_exige_get_e_nova_confirmacao(self):
        self.carregar()
        self.excluir_com([resposta(408, {"message": "Request timeout"})])
        self.assertIn("HTTP 408", self.mensagens("error"))
        self.assertTrue(self.app.session_state["cliente_exclusao"]["conferir"])
        self.assertTrue(self.app.button(key="carregar_exclusao").disabled)
        self.assertEqual(len(self.app.checkbox), 0)
        self.assertEqual(len(self.app.success), 0)
        self.assertEqual(self.metodos(), ["delete"])
        self.http.reset_mock()
        self.app.run()
        self.sem_excecoes()
        self.http.assert_not_called()
        self.http.side_effect = [resposta(200, CLIENTE)]
        self.clicar("Conferir estado atual da exclusão")
        self.assertEqual(self.metodos(), ["get"])
        self.assertFalse(self.app.checkbox[0].value)
        self.assertTrue(self.app.button(key="excluir_definitivamente").disabled)

    def test_404_ambiguo_apos_delete_nao_confirma_nem_invalida_estados(self):
        for posterior in (
            resposta(404), resposta(404, invalida=True),
            resposta(404, {"message": "Cliente não encontrado."}),
            resposta(404, {"code": "OUTRO_CODIGO", "message": "Cliente não encontrado."}),
            resposta(404, {"code": "ERROR_CODE_NOT_FOUND", "message": "Invalid app."}),
        ):
            with self.subTest(body=posterior.text):
                self.carregar()
                self.app.session_state["clientes_listagem"] = {
                    "base_url": BASE, "dados": [CLIENTE], "erro": None,
                }
                self.app.session_state["cliente_edicao"] = {
                    "base_url": BASE, "id_cliente": 1001, "dados": CLIENTE,
                    "geracao": 0, "confirmado": None, "erro": None,
                    "sucesso": False, "conferir": False,
                }
                self.excluir_com([
                    resposta(200, {"id_cliente": 1001, "excluido": True}), posterior,
                ])
                self.assertIn("Não foi possível conferir", self.mensagens("error"))
                self.assertEqual(len(self.app.success), 0)
                self.assertTrue(self.app.session_state["cliente_exclusao"]["conferir"])
                self.assertEqual(self.app.session_state["clientes_listagem"]["dados"], [CLIENTE])
                self.assertEqual(self.app.session_state["cliente_edicao"]["dados"], CLIENTE)
                self.assertEqual(self.metodos(), ["delete", "get"])
                self.http.reset_mock()
                self.app.run()
                self.sem_excecoes()
                self.http.assert_not_called()
                self.clicar("Cancelar")

    def test_404_ambiguo_na_conferencia_manual_mantem_resultado_incerto(self):
        self.carregar()
        self.excluir_com([resposta(408)])
        for posterior in (
            resposta(404, invalida=True),
            resposta(404, {"code": "ERROR_CODE_NOT_FOUND", "message": "Unable to locate request."}),
        ):
            with self.subTest(body=posterior.text):
                self.http.reset_mock()
                self.http.side_effect = [posterior]
                self.clicar("Conferir estado atual da exclusão")
                self.assertTrue(self.app.session_state["cliente_exclusao"]["conferir"])
                self.assertTrue(self.app.button(key="carregar_exclusao").disabled)
                self.assertEqual(len(self.app.success), 0)
                self.assertEqual(self.metodos(), ["get"])
        self.http.reset_mock()
        self.http.side_effect = [resposta(404, NAO_ENCONTRADO)]
        self.clicar("Conferir estado atual da exclusão")
        self.assertFalse(self.app.session_state["cliente_exclusao"]["conferir"])
        self.assertEqual(len(self.app.success), 0)
        self.assertIn("não confirma que a tentativa anterior", self.mensagens("info"))
        self.assertEqual(self.metodos(), ["get"])

    def test_falha_ou_presenca_na_confirmacao_posterior_nao_confirma_exclusao(self):
        for posterior in (requests.Timeout(), resposta(200, CLIENTE)):
            with self.subTest(posterior=type(posterior).__name__):
                self.carregar()
                self.excluir_com([
                    resposta(200, {"id_cliente": 1001, "excluido": True}), posterior,
                ])
                self.assertEqual(len(self.app.success), 0)
                self.assertTrue(self.app.session_state["cliente_exclusao"]["conferir"])
                self.assertEqual(self.metodos(), ["delete", "get"])
                self.clicar("Cancelar")

    def test_falha_na_conferencia_manual_mantem_bloqueio_de_reenvio(self):
        self.carregar()
        self.excluir_com([resposta(500)])
        self.http.reset_mock()
        self.http.side_effect = [requests.ConnectionError()]
        self.clicar("Conferir estado atual da exclusão")
        self.assertTrue(self.app.button(key="carregar_exclusao").disabled)
        self.assertEqual(self.metodos(), ["get"])
        self.assertEqual(len(self.app.success), 0)

    def test_resposta_delete_invalida_nao_dispara_get_automatico(self):
        self.carregar()
        self.excluir_com([resposta(200, {"id_cliente": 9999, "excluido": True})])
        self.assertIn("formato esperado", self.mensagens("error"))
        self.assertEqual(self.metodos(), ["delete"])
        self.assertEqual(len(self.app.success), 0)

    def test_exclusao_preserva_edicao_e_consulta_de_outro_cliente(self):
        self.carregar()
        outro = {**CLIENTE, "id_cliente": 1002}
        self.app.session_state["cliente_consulta"] = {
            "base_url": BASE, "id_cliente": 1002, "dados": outro,
            "erro": None, "nao_encontrado": False,
        }
        self.app.session_state["cliente_edicao"] = {
            "base_url": BASE, "id_cliente": 1002, "dados": outro,
            "geracao": 0, "confirmado": None, "erro": None,
            "sucesso": False, "conferir": False,
        }
        self.excluir_com([resposta(200, {"id_cliente": 1001, "excluido": True}), resposta(404, NAO_ENCONTRADO)])
        self.assertEqual(self.app.session_state["cliente_consulta"]["dados"], outro)
        self.assertEqual(self.app.session_state["cliente_edicao"]["dados"], outro)

    def test_regressao_cadastro_listagem_consulta_e_edicao(self):
        self.http.side_effect = None
        self.http.return_value = resposta(200, CLIENTE)
        for key in ("nome", "cpf", "telefone", "email"):
            self.app.text_input(key=key).set_value(CLIENTE[key])
        self.clicar("Cadastrar")
        self.assertIn("Cliente cadastrado", self.mensagens("success"))

        self.http.return_value = resposta(200, [CLIENTE])
        self.clicar("Atualizar lista")
        self.assertEqual(self.app.session_state["clientes_listagem"]["dados"], [CLIENTE])

        self.http.return_value = resposta(200, CLIENTE)
        self.app.text_input(key="consulta_id_cliente").set_value("1001")
        self.clicar("Consultar cliente")
        self.assertEqual(self.app.session_state["cliente_consulta"]["dados"], CLIENTE)
        self.app.text_input(key="edicao_selecao_id").set_value("1001")
        self.clicar("Carregar para edição")
        self.http.side_effect = [resposta(200, CLIENTE), resposta(200, CLIENTE)]
        self.clicar("Salvar alterações")
        self.assertIn("Atualização confirmada", self.mensagens("success"))
        self.assertNotIn("delete", self.metodos())


if __name__ == "__main__":
    unittest.main()
