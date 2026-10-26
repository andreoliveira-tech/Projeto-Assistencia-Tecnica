"""Página do módulo Equipamentos; HTTP apenas nas ações e confirmações indicadas."""

import streamlit as st

import equipamentos_api as api
from config import equipamentos_delete_validado, load_equipamentos_api_base_url


def _identificador(text):
    try:
        if not text.strip().isdecimal():
            raise ValueError
        value = int(text)
        if value <= 0:
            raise ValueError
        return value
    except (ValueError, TypeError):
        raise api.EquipamentoError("Informe um identificador inteiro positivo.") from None


def _campos(prefix, dados=None):
    dados = dados or {}
    values = {"tipo": st.text_input("Tipo", value=dados.get("tipo", ""), key=prefix + "tipo")}
    for campo, label in (("marca", "Marca"), ("modelo", "Modelo"), ("numero_serie", "Número de série")):
        texto = st.text_input(label, value=dados.get(campo) or "", key=prefix + campo)
        nulo = st.checkbox("Sem valor: " + label, value=dados.get(campo) is None, key=prefix + campo + "_null")
        values[campo] = None if nulo else texto
    cliente = st.text_input("ID do cliente", value=str(dados.get("id_cliente", "")), key=prefix + "cliente")
    return values, cliente


def _limpar_carregamento(estado):
    estado["dados"] = None
    estado["geracao"] += 1


def render():
    st.set_page_config(page_title="Equipamentos | Sistema de Assistência Técnica", layout="wide")
    st.title("Equipamentos")
    st.caption("Cadastro e gerenciamento de equipamentos vinculados a clientes.")
    try:
        base = load_equipamentos_api_base_url()
    except ValueError as error:
        st.error(str(error))
        return
    if base is None:
        st.info("Configure XANO_EQUIPAMENTOS_API_BASE_URL com a URL do grupo publicado antes de usar o módulo.")
        return
    if "equipamentos" not in st.session_state or st.session_state.equipamentos["base"] != base:
        anterior = st.session_state.get("equipamentos", {})
        st.session_state.equipamentos = {
            "base": base, "lista": None, "dados": None, "selecao": "", "geracao": anterior.get("geracao", 0) + 1,
            "aviso": None, "sucesso": None,
        }
    estado = st.session_state.equipamentos
    st.subheader("Cadastrar equipamento")
    with st.form("cadastro_equipamento", enter_to_submit=False):
        dados, cliente = _campos("novo_")
        cadastrar = st.form_submit_button("Cadastrar equipamento")
    if cadastrar:
        estado.update(sucesso=None, aviso=None)
        try:
            dados["id_cliente"] = _identificador(cliente)
            criado = api.cadastrar_equipamento(base, dados)
        except api.EquipamentoError as error:
            st.error(str(error))
        else:
            estado["lista"] = None
            st.success(f"Equipamento cadastrado. Identificador: {criado['id_equipamento']}.")

    st.subheader("Equipamentos cadastrados")
    if st.button("Atualizar equipamentos"):
        estado["lista"] = None
        try:
            estado["lista"] = api.listar_equipamentos(base)
        except api.EquipamentoError as error:
            st.error(str(error))
    if estado["lista"] is not None:
        if estado["lista"]:
            st.caption("Resultado da última consulta.")
            st.dataframe(estado["lista"], hide_index=True)
        else:
            st.info("Nenhum equipamento cadastrado.")

    st.subheader("Consultar, editar ou excluir equipamento")
    selecao = st.text_input("ID do equipamento", key="equipamento_selecao")
    if selecao != estado["selecao"]:
        _limpar_carregamento(estado)
        estado.update(selecao=selecao, aviso=None, sucesso=None)
    if st.button("Carregar equipamento"):
        _limpar_carregamento(estado)
        estado.update(sucesso=None, aviso=None)
        try:
            estado["dados"] = api.consultar_equipamento(base, _identificador(selecao))
        except api.EquipamentoError as error:
            st.error(str(error))
    if estado["sucesso"]:
        st.success(estado["sucesso"])
    if estado["aviso"]:
        st.warning(estado["aviso"])
    atual = estado["dados"]
    if atual is None:
        return
    st.write(atual)
    identificador = atual["id_equipamento"]
    prefix = f"editar_{estado['geracao']}_"
    with st.form("editar_equipamento", enter_to_submit=False):
        alterado, cliente = _campos(prefix, atual)
        salvar = st.form_submit_button("Salvar equipamento")
    if salvar:
        estado.update(sucesso=None, aviso=None)
        try:
            alterado["id_cliente"] = _identificador(cliente)
            retorno = api.atualizar_equipamento(base, identificador, alterado)
        except api.EquipamentoError as error:
            if isinstance(error, api.EquipamentoNaoEncontrado) or error.incerto:
                _limpar_carregamento(estado)
                estado["aviso"] = "Carregue o equipamento novamente antes de outra escrita. " + str(error)
                st.rerun()
            st.error(str(error))
        else:
            try:
                conferido = api.consultar_equipamento(base, identificador)
                if conferido != retorno:
                    raise api.EquipamentoError("Consulta posterior divergente.")
            except api.EquipamentoError:
                _limpar_carregamento(estado)
                estado["aviso"] = "Atualização não confirmada. Carregue novamente para conferir o estado atual."
            else:
                _limpar_carregamento(estado)
                estado.update(dados=conferido, lista=None, sucesso="Equipamento atualizado e conferido.")
            st.rerun()

    if equipamentos_delete_validado():
        st.warning(f"A exclusão do equipamento {identificador} é definitiva e depende da ausência de OS vinculadas.")
        confirmar = st.checkbox(f"Confirmo excluir o equipamento {identificador}", key=f"excluir_{estado['geracao']}")
        if st.button("Excluir equipamento", disabled=not confirmar) and confirmar:
            # Consome o carregamento e a confirmação antes da tentativa de escrita.
            _limpar_carregamento(estado)
            estado.update(sucesso=None, aviso=None)
            try:
                api.excluir_equipamento(base, identificador)
            except api.EquipamentoError as error:
                estado["aviso"] = str(error) + " Carregue novamente antes de tentar outra operação."
            else:
                try:
                    api.consultar_equipamento(base, identificador)
                except api.EquipamentoNaoEncontrado:
                    estado.update(lista=None, sucesso="Equipamento excluído e ausência confirmada.")
                except api.EquipamentoError:
                    estado["aviso"] = "Exclusão não confirmada. Carregue novamente para conferir o estado atual."
                else:
                    estado["aviso"] = "O equipamento ainda foi encontrado. Exclusão não confirmada."
            st.rerun()
    else:
        st.info("A exclusão de equipamentos está indisponível até o endpoint DELETE ser publicado e validado.")
    if st.button("Cancelar operação de equipamento"):
        _limpar_carregamento(estado)
        estado.update(aviso=None, sucesso=None)
        st.rerun()
