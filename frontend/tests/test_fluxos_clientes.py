"""Verifica configuração e falhas de todos os fluxos sem acesso ao Xano."""

import os
import unittest
from unittest.mock import patch

import test_exclusao_clientes as suporte
from config import load_api_base_url
import verificar_integracao_clientes as integracao


api = suporte.api
BASE = suporte.BASE
CLIENTE = suporte.CLIENTE
resposta = suporte.resposta


class ConfiguracaoTests(suporte.SemRede):
    def test_ausente_valida_e_normalizada(self):
        for value, expected in (("", None), ("  ", None), (BASE, BASE), (" " + BASE + "/ ", BASE)):
            with self.subTest(value=value), patch.dict(os.environ, {"XANO_CLIENTES_API_BASE_URL": value}):
                self.assertEqual(load_api_base_url(), expected)
        self.http.assert_not_called()

    def test_configuracoes_invalidas_sem_expor_conteudo(self):
        for value in (
            "http://example.invalid", "https://", "https://usuario:segredo@example.invalid",
            "https://example.invalid?token=segredo", "https://example.invalid#segredo",
            "https://example.invalid:abc", "https://example.invalid:0", "https://example.invalid/a b",
        ):
            with self.subTest(value=value), patch.dict(os.environ, {"XANO_CLIENTES_API_BASE_URL": value}):
                with self.assertRaises(ValueError) as error:
                    load_api_base_url()
                self.assertNotIn("segredo", str(error.exception))
        self.http.assert_not_called()


class FalhasHttpTests(suporte.SemRede):
    def test_cadastro_rejeicoes_comunicacao_e_respostas_invalidas(self):
        for result in (
            resposta(400, {"message": "Dados inválidos."}), resposta(400, invalida=True),
            resposta(408), resposta(500), resposta(302), resposta(200, invalida=True),
            resposta(200, {}), resposta(200, {**CLIENTE, "id_cliente": True}),
            resposta(200, {**CLIENTE, "cpf": 123}), requests_timeout(),
            api.requests.ConnectionError(),
        ):
            with self.subTest(result=type(result).__name__):
                self.http.reset_mock()
                self.http.side_effect = [result]
                with self.assertRaises(api.CadastroError):
                    api.cadastrar_cliente(BASE, CLIENTE)
                self.http.assert_called_once()

    def test_listagem_e_consulta_recusam_erros_e_contratos_invalidos(self):
        for function, args, error in (
            (api.listar_clientes, (BASE,), api.ListagemError),
            (api.consultar_cliente, (BASE, 1001), api.ConsultaError),
        ):
            for result in (
                resposta(500), resposta(400), resposta(302), resposta(200, invalida=True),
                resposta(200, None), resposta(200, {"id_cliente": 1001}),
                requests_timeout(), api.requests.ConnectionError(),
            ):
                with self.subTest(function=function.__name__, result=type(result).__name__):
                    self.http.reset_mock()
                    self.http.side_effect = [result]
                    with self.assertRaises(error):
                        function(*args)
                    self.http.assert_called_once()

    def test_atualizacao_separa_rejeicao_e_resultado_incerto(self):
        for result, incerto in (
            (resposta(400, {"message": "Dados inválidos."}), False),
            (resposta(400, invalida=True), False), (resposta(408), True),
            (resposta(500), True), (resposta(302), True), (resposta(200, invalida=True), True),
            (resposta(200, {**CLIENTE, "id_cliente": 1002}), True),
            (resposta(200, {**CLIENTE, "telefone": None}), True),
            (requests_timeout(), True), (api.requests.ConnectionError(), True),
        ):
            with self.subTest(result=type(result).__name__, incerto=incerto):
                self.http.reset_mock()
                self.http.side_effect = [result]
                with self.assertRaises(api.AtualizacaoError) as error:
                    api.atualizar_cliente(BASE, 1001, CLIENTE)
                self.assertEqual(error.exception.incerto, incerto)
                self.http.assert_called_once()

    def test_atualizacao_invalida_localmente_nao_envia(self):
        for dados in ({}, {**CLIENTE, "nome": "  "}, {**CLIENTE, "email": None}):
            with self.subTest(dados=dados), self.assertRaises(api.AtualizacaoError):
                api.atualizar_cliente(BASE, 1001, dados)
        self.http.assert_not_called()


def requests_timeout():
    return api.requests.Timeout()


class EscopoIntegradoTests(suporte.SemRede):
    def setUp(self):
        super().setUp()
        from unittest.mock import Mock
        self.transporte = Mock(return_value=resposta(200, CLIENTE))
        self.escopo = integracao.EscopoDescartavel(self.transporte)
        self.escopo.anteriores = [CLIENTE]
        self.session = api.requests.Session()
        self.addCleanup(self.session.close)

    def chamar(self, method, url, **kwargs):
        return self.escopo.request(self.session, method, url, timeout=(5, 20), allow_redirects=False, **kwargs)

    def test_nunca_exclui_registro_preexistente(self):
        self.escopo.id_criado = CLIENTE["id_cliente"]
        self.escopo.permitir_delete = True
        with self.assertRaises(RuntimeError):
            self.chamar("DELETE", integracao.BASE + "/clientes/1001")
        self.transporte.assert_not_called()

    def test_recusa_put_ou_endpoint_fora_do_escopo(self):
        for method, url in (
            ("PUT", integracao.BASE + "/clientes/1001"),
            ("GET", integracao.BASE + "/clientes/1001"),
            ("DELETE", integracao.BASE + "/clientes/1001"),
            ("POST", integracao.BASE + "/equipamentos"),
        ):
            with self.subTest(method=method), self.assertRaises(RuntimeError):
                self.chamar(method, url)
        self.transporte.assert_not_called()

    def test_recusa_post_duplicado_ou_corpo_diferente(self):
        for dados in (CLIENTE, {}):
            with self.subTest(dados=dados), self.assertRaises(RuntimeError):
                self.chamar("POST", integracao.BASE + "/clientes", json=dados)
        self.escopo.posts = 1
        with self.assertRaises(RuntimeError):
            self.chamar("POST", integracao.BASE + "/clientes", json=integracao.FICTICIO)
        self.transporte.assert_not_called()

    def test_recusa_delete_repetido_mesmo_para_id_novo(self):
        self.escopo.id_criado = 2001
        self.escopo.permitir_delete = True
        self.chamar("DELETE", integracao.BASE + "/clientes/2001")
        with self.assertRaises(RuntimeError):
            self.chamar("DELETE", integracao.BASE + "/clientes/2001")
        self.transporte.assert_called_once()


class FalhasInterfaceTests(suporte.SemRede):
    def setUp(self):
        super().setUp()
        env = patch.dict(os.environ, {"XANO_CLIENTES_API_BASE_URL": BASE})
        env.start()
        self.addCleanup(env.stop)
        self.app = suporte.AppTest.from_file(str(suporte.FRONTEND / "app.py"), default_timeout=20).run()
        self.check()

    def check(self):
        self.assertEqual(len(self.app.exception), 0, str(self.app.exception))

    def clicar(self, label):
        next(button for button in self.app.button if button.label == label).click().run()
        self.check()

    def sem_sucesso(self):
        self.assertEqual(len(self.app.success), 0)
        self.assertGreater(len(self.app.error), 0)

    def preparar_cadastro(self):
        for campo in ("nome", "cpf", "telefone", "email"):
            self.app.text_input(key=campo).set_value(CLIENTE[campo])

    def carregar_edicao(self):
        self.http.side_effect = [resposta(200, CLIENTE)]
        self.app.text_input(key="edicao_selecao_id").set_value("1001")
        self.clicar("Carregar para edição")
        self.http.reset_mock()

    def test_app_sem_configuracao_ou_configuracao_invalida_nao_acessa_rede(self):
        for value in ("", "http://invalido.example.invalid"):
            with self.subTest(value=value), patch.dict(os.environ, {"XANO_CLIENTES_API_BASE_URL": value}):
                self.app.run()
                self.check()
                self.assertEqual(len(self.app.success), 0)
        self.http.assert_not_called()

    def test_cadastro_falhas_preservam_campos_e_nao_reenviam_em_rerun(self):
        for result in (resposta(400, {"message": "CPF inválido."}), resposta(408), resposta(500), requests_timeout()):
            with self.subTest(result=type(result).__name__):
                self.preparar_cadastro()
                self.http.reset_mock()
                self.http.side_effect = [result]
                self.clicar("Cadastrar")
                self.sem_sucesso()
                self.http.assert_called_once()
                for campo in ("nome", "cpf", "telefone", "email"):
                    self.assertEqual(self.app.text_input(key=campo).value, CLIENTE[campo])
                self.http.reset_mock()
                self.app.run()
                self.http.assert_not_called()

    def test_campos_vazios_no_cadastro_nao_enviam(self):
        self.clicar("Cadastrar")
        self.sem_sucesso()
        self.http.assert_not_called()

    def test_listagem_vazia_e_falha_descartam_resultado_anterior(self):
        self.http.side_effect = [resposta(200, [CLIENTE]), resposta(200, []), resposta(500)]
        self.clicar("Atualizar lista")
        self.assertEqual(self.app.session_state["clientes_listagem"]["dados"], [CLIENTE])
        self.clicar("Atualizar lista")
        self.assertEqual(self.app.session_state["clientes_listagem"]["dados"], [])
        self.assertTrue(any("Nenhum cliente" in item.value for item in self.app.info))
        self.clicar("Atualizar lista")
        self.sem_sucesso()
        self.assertIsNone(self.app.session_state["clientes_listagem"]["dados"])

    def test_consulta_com_falha_limpa_resultado_anterior(self):
        self.http.side_effect = [resposta(200, CLIENTE), requests_timeout()]
        self.app.text_input(key="consulta_id_cliente").set_value("1001")
        self.clicar("Consultar cliente")
        self.clicar("Consultar cliente")
        self.sem_sucesso()
        self.assertIsNone(self.app.session_state["cliente_consulta"]["dados"])

    def test_edicao_rejeitada_preserva_campos_sem_sucesso(self):
        self.carregar_edicao()
        campo = next(item for item in self.app.text_input if item.label == "Nome para edição")
        campo.set_value("Nome fictício digitado")
        self.http.side_effect = [resposta(400, {"message": "Dados inválidos."})]
        self.clicar("Salvar alterações")
        self.sem_sucesso()
        self.assertEqual(next(item for item in self.app.text_input if item.label == "Nome para edição").value,
                         "Nome fictício digitado")
        self.http.assert_called_once()

    def test_edicao_incerta_e_confirmacao_divergente_impedem_novo_envio(self):
        for results in (
            [resposta(408)], [requests_timeout()],
            [resposta(200, CLIENTE), resposta(500)],
            [resposta(200, CLIENTE), resposta(200, {**CLIENTE, "nome": "Outro nome fictício"})],
        ):
            with self.subTest(resultados=len(results)):
                self.carregar_edicao()
                self.http.side_effect = results
                self.clicar("Salvar alterações")
                self.sem_sucesso()
                self.assertTrue(self.app.session_state["cliente_edicao"]["conferir"])
                self.assertTrue(next(b for b in self.app.button if b.label == "Salvar alterações").disabled)
                self.http.reset_mock()
                self.app.run()
                self.http.assert_not_called()

    def test_edicao_404_invalida_formulario_sem_sucesso(self):
        self.carregar_edicao()
        self.http.side_effect = [resposta(404)]
        self.clicar("Salvar alterações")
        self.sem_sucesso()
        self.assertIsNone(self.app.session_state["cliente_edicao"]["dados"])


if __name__ == "__main__":
    unittest.main()
