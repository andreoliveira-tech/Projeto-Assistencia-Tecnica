"""Contrato proposto e interface de Equipamentos, com HTTP simulado e rede bloqueada."""

import copy
import os
from pathlib import Path
from unittest.mock import patch

import test_exclusao_clientes as suporte
import equipamentos_api as api
from config import equipamentos_delete_validado, load_equipamentos_api_base_url
from streamlit.testing.v1 import AppTest


BASE = "https://equipamentos.example.invalid/api:teste"
DADOS = {"tipo": "Notebook", "marca": None, "modelo": "", "numero_serie": "000ABC", "id_cliente": 1001}
EQUIPAMENTO = {"id_equipamento": 2001, **DADOS}
AUSENTE = {"code": "ERROR_CODE_NOT_FOUND", "message": api.AUSENTE}
resposta = suporte.resposta


class EquipamentosHttpTests(suporte.SemRede):
    def setUp(self):
        super().setUp()
        self.http.side_effect = None

    def test_configuracao_independente_e_segura(self):
        with patch.dict(os.environ, {"XANO_EQUIPAMENTOS_API_BASE_URL": "", "XANO_CLIENTES_API_BASE_URL": BASE}):
            self.assertIsNone(load_equipamentos_api_base_url())
        with patch.dict(os.environ, {"XANO_EQUIPAMENTOS_API_BASE_URL": " " + BASE + "/ "}):
            self.assertEqual(load_equipamentos_api_base_url(), BASE)
        for value in ["http://example.invalid", "https://user:segredo@example.invalid", BASE + "?token=segredo", BASE + "#segredo"]:
            with self.subTest(value=value), patch.dict(os.environ, {"XANO_EQUIPAMENTOS_API_BASE_URL": value}):
                with self.assertRaises(ValueError) as error:
                    load_equipamentos_api_base_url()
                self.assertNotIn("segredo", str(error.exception))
        self.http.assert_not_called()

    def test_exclusao_exige_flag_de_validacao_explicita(self):
        for value in [None, "", "false", "1", "yes"]:
            with self.subTest(value=value), patch.dict(os.environ, {}, clear=False):
                os.environ.pop("XANO_EQUIPAMENTOS_DELETE_VALIDATED", None)
                if value is not None:
                    os.environ["XANO_EQUIPAMENTOS_DELETE_VALIDATED"] = value
                self.assertFalse(equipamentos_delete_validado())
        with patch.dict(os.environ, {"XANO_EQUIPAMENTOS_DELETE_VALIDATED": "true"}):
            self.assertTrue(equipamentos_delete_validado())

    def test_cadastro_preserva_texto_vazio_null_e_zeros_sem_campos_extras(self):
        self.http.return_value = resposta(200, EQUIPAMENTO)
        self.assertEqual(api.cadastrar_equipamento(BASE, {**DADOS, "ignorado": "x"}), EQUIPAMENTO)
        self.http.assert_called_once_with(method="POST", url=BASE + "/equipamentos", json=DADOS, timeout=(5, 20), allow_redirects=False)

    def test_tipo_vazio_nao_introduz_validacao_nao_aprovada(self):
        self.http.return_value = resposta(200, {**EQUIPAMENTO, "tipo": ""})
        self.assertEqual(api.cadastrar_equipamento(BASE, {**DADOS, "tipo": ""})["tipo"], "")

    def test_listagem_valida_e_vazia(self):
        for payload in [[EQUIPAMENTO], []]:
            self.http.return_value = resposta(200, payload)
            self.assertEqual(api.listar_equipamentos(BASE), payload)

    def test_consulta_e_atualizacao_usam_id_da_rota(self):
        self.http.return_value = resposta(200, EQUIPAMENTO)
        self.assertEqual(api.consultar_equipamento(BASE, 2001), EQUIPAMENTO)
        self.assertEqual(api.atualizar_equipamento(BASE, 2001, DADOS), EQUIPAMENTO)
        self.assertEqual(self.http.call_args.kwargs["method"], "PUT")
        self.assertEqual(self.http.call_args.kwargs["json"], DADOS)

    def test_ids_invalidos_nao_enviam_http(self):
        for value in [None, True, False, 0, -1, 1.5, "2001"]:
            for method in [api.consultar_equipamento, api.excluir_equipamento]:
                with self.subTest(value=value), self.assertRaises(api.EquipamentoError):
                    method(BASE, value)
            with self.assertRaises(api.EquipamentoError):
                api.atualizar_equipamento(BASE, value, DADOS)
        self.http.assert_not_called()

    def test_dados_invalidos_nao_enviam_http(self):
        for dados in [None, {}, {**DADOS, "tipo": None}, {**DADOS, "id_cliente": True}, {**DADOS, "id_cliente": 0}, {**DADOS, "marca": 12}]:
            with self.subTest(dados=dados), self.assertRaises(api.EquipamentoError):
                api.cadastrar_equipamento(BASE, dados)
        self.http.assert_not_called()

    def test_contratos_invalidos_de_lista_e_consulta(self):
        for payload in [None, {}, [EQUIPAMENTO, {**EQUIPAMENTO, "marca": 1}], "texto"]:
            self.http.return_value = resposta(200, payload)
            with self.assertRaises(api.EquipamentoError):
                api.listar_equipamentos(BASE)
        for payload in [None, {**EQUIPAMENTO, "id_equipamento": 2}, {**EQUIPAMENTO, "id_equipamento": True}, {k: v for k, v in EQUIPAMENTO.items() if k != "marca"}]:
            self.http.return_value = resposta(200, payload)
            with self.assertRaises(api.EquipamentoError):
                api.consultar_equipamento(BASE, 2001)

    def test_ausencia_so_com_envelope_conhecido(self):
        self.http.return_value = resposta(404, AUSENTE)
        with self.assertRaises(api.EquipamentoNaoEncontrado):
            api.consultar_equipamento(BASE, 2001)
        for payload in [{}, {"code": "ERROR_CODE_NOT_FOUND", "message": "Invalid app."}, {"message": api.AUSENTE}, []]:
            self.http.return_value = resposta(404, payload)
            with self.assertRaises(api.EquipamentoError) as error:
                api.consultar_equipamento(BASE, 2001)
            self.assertNotIsInstance(error.exception, api.EquipamentoNaoEncontrado)
        self.http.return_value = resposta(404, invalida=True)
        with self.assertRaises(api.EquipamentoError) as error:
            api.consultar_equipamento(BASE, 2001)
        self.assertNotIsInstance(error.exception, api.EquipamentoNaoEncontrado)

    def test_bloqueio_distinto_de_falha_de_verificacao(self):
        self.http.return_value = resposta(400, {"code": "ERROR_CODE_INPUT_ERROR", "message": api.BLOQUEIO})
        with self.assertRaises(api.ExclusaoBloqueada):
            api.excluir_equipamento(BASE, 2001)
        self.http.return_value = resposta(400, {"code": "ERROR_CODE_INPUT_ERROR", "message": "Nao foi possivel confirmar as ordens do equipamento."})
        with self.assertRaises(api.EquipamentoError) as error:
            api.excluir_equipamento(BASE, 2001)
        self.assertNotIsInstance(error.exception, api.ExclusaoBloqueada)
        self.assertFalse(error.exception.incerto)

    def test_delete_unico_sem_corpo(self):
        self.http.return_value = resposta(200, {"id_equipamento": 2001, "excluido": True})
        self.assertTrue(api.excluir_equipamento(BASE, 2001)["excluido"])
        self.http.assert_called_once_with(method="DELETE", url=BASE + "/equipamentos/2001", timeout=(5, 20), allow_redirects=False)

    def test_escritas_incertas_sem_retry(self):
        for method, args in [(api.cadastrar_equipamento, (DADOS,)), (api.atualizar_equipamento, (2001, DADOS)), (api.excluir_equipamento, (2001,))]:
            for failure in [resposta(408, {}), resposta(500, {}), resposta(302, {}), resposta(200, invalida=True), suporte.requests.Timeout(), suporte.requests.ConnectionError()]:
                self.http.reset_mock()
                self.http.side_effect = failure if isinstance(failure, Exception) else None
                self.http.return_value = failure
                with self.subTest(method=method.__name__, failure=type(failure).__name__), self.assertRaises(api.EquipamentoError) as error:
                    method(BASE, *args)
                self.assertTrue(error.exception.incerto)
                self.http.assert_called_once()

    def test_delete_nao_aceita_sucesso_incompativel(self):
        for payload in [{"id_equipamento": True, "excluido": True}, {"id_equipamento": 2001, "excluido": 1}, {"id_equipamento": 2, "excluido": True}, {}]:
            self.http.return_value = resposta(200, payload)
            with self.assertRaises(api.EquipamentoError) as error:
                api.excluir_equipamento(BASE, 2001)
            self.assertTrue(error.exception.incerto)


class EquipamentosInterfaceTests(suporte.SemRede):
    def app(self, base=BASE, delete_validated=False):
        env = patch.dict(os.environ, {"XANO_EQUIPAMENTOS_API_BASE_URL": base})
        env.start()
        self.addCleanup(env.stop)
        os.environ.pop("XANO_EQUIPAMENTOS_DELETE_VALIDATED", None)
        if delete_validated:
            os.environ["XANO_EQUIPAMENTOS_DELETE_VALIDATED"] = "true"
        at = AppTest.from_file(str(suporte.FRONTEND / "pages" / "1_Equipamentos.py"), default_timeout=15).run()
        self.assertFalse(at.exception)
        return at

    def click(self, at, label):
        next(b for b in at.button if b.label == label).click().run()
        self.assertFalse(at.exception)

    def load(self, at, item=EQUIPAMENTO):
        self.http.side_effect = None
        self.http.return_value = resposta(200, item)
        at.text_input(key="equipamento_selecao").set_value(str(item["id_equipamento"])).run()
        self.click(at, "Carregar equipamento")

    def confirm(self, at):
        next(c for c in at.checkbox if c.label.startswith("Confirmo excluir")).check().run()

    def test_abertura_sem_configuracao_e_url_invalida_sem_http(self):
        for value in ["", "http://invalido", "https://user:segredo@example.invalid"]:
            at = self.app(value)
            self.assertFalse(at.exception)
        self.http.assert_not_called()

    def test_abertura_reruns_e_selecao_nao_fazem_http(self):
        at = self.app()
        at.run()
        at.text_input(key="equipamento_selecao").set_value("2001").run()
        self.http.assert_not_called()

    def test_identificadores_invalidos_sem_http(self):
        at = self.app()
        for value in ["", "0", "-2", "abc", "1.5"]:
            at.text_input(key="equipamento_selecao").set_value(value).run()
            self.click(at, "Carregar equipamento")
        self.http.assert_not_called()

    def test_cadastro_e_campos_nullable(self):
        at = self.app()
        at.text_input(key="novo_tipo").set_value("Notebook")
        at.text_input(key="novo_cliente").set_value("1001")
        self.http.side_effect = None
        self.http.return_value = resposta(200, EQUIPAMENTO)
        self.click(at, "Cadastrar equipamento")
        sent = self.http.call_args.kwargs["json"]
        self.assertEqual(sent["id_cliente"], 1001)
        self.assertIsNone(sent["marca"])
        self.assertTrue(at.success)
        at.run()
        self.http.assert_called_once()

    def test_cadastro_invalido_rejeitado_e_incerto_sem_retry(self):
        at = self.app()
        self.click(at, "Cadastrar equipamento")
        self.http.assert_not_called()
        at.text_input(key="novo_cliente").set_value("1001")
        for response in [resposta(400, {}), resposta(408, {}), resposta(200, invalida=True)]:
            self.http.reset_mock()
            self.http.side_effect = None
            self.http.return_value = response
            self.click(at, "Cadastrar equipamento")
            self.assertTrue(at.error)
            self.assertFalse(at.success)
            at.run()
            self.http.assert_called_once()

    def test_lista_vazia_e_falha_limpam_resultado(self):
        at = self.app()
        self.http.side_effect = None
        for payload in [[EQUIPAMENTO], []]:
            self.http.return_value = resposta(200, payload)
            self.click(at, "Atualizar equipamentos")
            self.assertEqual(at.session_state.equipamentos["lista"], payload)
        self.http.return_value = resposta(500, {})
        self.click(at, "Atualizar equipamentos")
        self.assertIsNone(at.session_state.equipamentos["lista"])

    def test_troca_de_id_url_recarregamento_e_cancelamento_invalidam_confirmacao(self):
        at = self.app(delete_validated=True)
        self.load(at)
        self.confirm(at)
        self.click(at, "Carregar equipamento")
        self.assertFalse(next(c for c in at.checkbox if c.label.startswith("Confirmo excluir")).value)
        self.confirm(at)
        at.text_input(key="equipamento_selecao").set_value("2002").run()
        self.assertIsNone(at.session_state.equipamentos["dados"])
        self.load(at)
        self.confirm(at)
        self.click(at, "Cancelar operação de equipamento")
        self.assertIsNone(at.session_state.equipamentos["dados"])
        self.load(at)
        self.confirm(at)
        with patch.dict(os.environ, {"XANO_EQUIPAMENTOS_API_BASE_URL": BASE + "-outro"}):
            at.run()
        self.assertIsNone(at.session_state.equipamentos["dados"])
        self.assertTrue(all(c.kwargs["method"] == "GET" for c in self.http.call_args_list))

    def test_edicao_confirma_por_get(self):
        at = self.app()
        self.load(at)
        self.http.reset_mock()
        self.http.side_effect = [resposta(200, EQUIPAMENTO), resposta(200, EQUIPAMENTO)]
        self.click(at, "Salvar equipamento")
        self.assertEqual([c.kwargs["method"] for c in self.http.call_args_list], ["PUT", "GET"])
        self.assertTrue(at.success)
        at.run()
        self.assertEqual(self.http.call_count, 2)

    def test_edicao_incerta_exige_novo_carregamento(self):
        for responses in [[resposta(408, {})], [resposta(200, EQUIPAMENTO), resposta(200, {**EQUIPAMENTO, "tipo": "outro"})], [resposta(200, EQUIPAMENTO), resposta(500, {})]]:
            at = self.app()
            self.load(at)
            self.http.reset_mock()
            self.http.side_effect = responses
            self.click(at, "Salvar equipamento")
            self.assertFalse(at.success)
            self.assertIsNone(at.session_state.equipamentos["dados"])
            count = self.http.call_count
            at.run()
            self.assertEqual(self.http.call_count, count)

    def test_troca_de_contexto_descarta_mensagem_de_sucesso_anterior(self):
        at = self.app()
        self.load(at)
        self.http.side_effect = [resposta(200, EQUIPAMENTO), resposta(200, EQUIPAMENTO)]
        self.click(at, "Salvar equipamento")
        self.assertTrue(at.success)
        self.http.reset_mock()
        at.text_input(key="equipamento_selecao").set_value("2002").run()
        self.assertFalse(at.success)
        self.assertIsNone(at.session_state.equipamentos["dados"])
        self.http.assert_not_called()

    def test_delete_exige_confirmacao_e_confere_ausencia(self):
        at = self.app(delete_validated=True)
        self.load(at)
        self.assertTrue(next(b for b in at.button if b.label == "Excluir equipamento").disabled)
        self.confirm(at)
        self.http.reset_mock()
        self.http.side_effect = [resposta(200, {"id_equipamento": 2001, "excluido": True}), resposta(404, AUSENTE)]
        self.click(at, "Excluir equipamento")
        self.assertEqual([c.kwargs["method"] for c in self.http.call_args_list], ["DELETE", "GET"])
        self.assertTrue(at.success)
        self.assertIsNone(at.session_state.equipamentos["dados"])
        self.assertIsNone(at.session_state.equipamentos["lista"])
        at.run()
        self.assertEqual(self.http.call_count, 2)

    def test_404_ambiguo_invalido_presenca_e_falha_nao_confirmam_delete(self):
        for posterior in [resposta(404, {}), resposta(404, invalida=True), resposta(200, EQUIPAMENTO), resposta(500, {})]:
            at = self.app(delete_validated=True)
            self.load(at)
            self.confirm(at)
            at.session_state.equipamentos["lista"] = [EQUIPAMENTO]
            self.http.reset_mock()
            self.http.side_effect = [resposta(200, {"id_equipamento": 2001, "excluido": True}), posterior]
            self.click(at, "Excluir equipamento")
            self.assertFalse(at.success)
            self.assertEqual(at.session_state.equipamentos["lista"], [EQUIPAMENTO])
            at.run()
            self.assertEqual(self.http.call_count, 2)

    def test_bloqueio_rejeicao_ausencia_e_incerto_sem_get_ou_reenvio(self):
        for response in [resposta(400, {"code": "ERROR_CODE_INPUT_ERROR", "message": api.BLOQUEIO}), resposta(400, {"message": "Falha na verificação"}), resposta(404, AUSENTE), resposta(408, {}), resposta(500, {}), resposta(200, {"excluido": True})]:
            at = self.app(delete_validated=True)
            self.load(at)
            self.confirm(at)
            self.http.reset_mock()
            self.http.side_effect = None
            self.http.return_value = response
            self.click(at, "Excluir equipamento")
            self.assertFalse(at.success)
            self.assertIsNone(at.session_state.equipamentos["dados"])
            at.run()
            self.http.assert_called_once()

    def test_estados_de_clientes_preservados(self):
        at = self.app(delete_validated=True)
        clientes = {"base_url": suporte.BASE, "dados": [suporte.CLIENTE]}
        at.session_state.clientes_listagem = copy.deepcopy(clientes)
        self.load(at)
        self.confirm(at)
        self.http.side_effect = [resposta(200, {"id_equipamento": 2001, "excluido": True}), resposta(404, AUSENTE)]
        self.click(at, "Excluir equipamento")
        self.assertEqual(at.session_state.clientes_listagem, clientes)

    def test_exclusao_indisponivel_por_padrao_mesmo_com_url_configurada(self):
        at = self.app()
        self.load(at)
        self.assertIn("até o endpoint DELETE ser publicado e validado", at.info[0].value)
        self.assertFalse(any(button.label == "Excluir equipamento" for button in at.button))
        self.assertFalse(any(checkbox.label.startswith("Confirmo excluir") for checkbox in at.checkbox))
        self.assertEqual([call.kwargs["method"] for call in self.http.call_args_list], ["GET"])

    def test_rede_externa_e_http_nao_previsto_bloqueados(self):
        with self.assertRaises(AssertionError):
            suporte.requests.get("https://nao-previsto.example.invalid")
        self.http.assert_called_once()
