"""Cadastro de clientes com envio exclusivamente por submissão do formulário."""

import streamlit as st
from pathlib import Path

from config import load_api_base_url
from clientes_api import CadastroError, ListagemError, cadastrar_cliente, listar_clientes


st.set_page_config(
    page_title="Clientes | Sistema de Assistência Técnica",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(
    "<style>" + Path(__file__).with_name("styles.css").read_text(encoding="utf-8") + "</style>",
    unsafe_allow_html=True,
)
with st.sidebar:
    st.markdown(
        '<div class="system-brand"><div class="brand-symbol">AT</div>'
        '<div><strong>Assistência Técnica</strong><span>Gestão de clientes</span></div></div>',
        unsafe_allow_html=True,
    )
    st.markdown('<p class="nav-label">CLIENTES</p>', unsafe_allow_html=True)
    st.markdown(
        '<nav class="client-nav" aria-label="Navegação de clientes">'
        '<a href="#cadastrar-cliente" target="_self">Cadastrar cliente <span>↗</span></a>'
        '<a href="#clientes-cadastrados" target="_self">Clientes cadastrados <span>↗</span></a>'
        '</nav>',
        unsafe_allow_html=True,
    )
    st.divider()
    st.caption("Sistema de Assistência Técnica")

st.markdown('<p class="page-eyebrow">RELACIONAMENTO E ATENDIMENTO</p>', unsafe_allow_html=True)
st.title("Clientes")
st.markdown("Cadastre seus clientes e mantenha as informações de contato organizadas.")
st.divider()

try:
    api_base_url = load_api_base_url()
except ValueError as error:
    st.error(str(error))
else:
    if api_base_url is None:
        st.info(
            "Configure XANO_CLIENTES_API_BASE_URL no ambiente antes de iniciar "
            "a integração com as APIs de Clientes."
        )
    else:
        st.subheader("Cadastrar cliente", anchor="cadastrar-cliente")
        st.caption("Preencha os dados abaixo para adicionar um novo cliente. Todos os campos são obrigatórios.")
        with st.form("cadastro_cliente", clear_on_submit=False, enter_to_submit=False):
            nome = st.text_input("Nome", key="nome")
            coluna_cpf, coluna_telefone = st.columns(2)
            with coluna_cpf:
                cpf = st.text_input("CPF", key="cpf", help="Com ou sem máscara.")
            with coluna_telefone:
                telefone = st.text_input("Telefone", key="telefone", help="Inclua o DDD.")
            email = st.text_input("E-mail", key="email")
            enviar = st.form_submit_button("Cadastrar", type="primary")

        if enviar:
            dados = {"nome": nome, "cpf": cpf, "telefone": telefone, "email": email}
            if not all(value.strip() for value in dados.values()):
                st.error("Preencha nome, CPF, telefone e e-mail.")
            else:
                try:
                    with st.spinner("Enviando cadastro..."):
                        cliente = cadastrar_cliente(api_base_url, dados)
                except CadastroError as error:
                    st.error(str(error))
                else:
                    st.success(f"Cliente cadastrado com sucesso. Identificador: {cliente['id_cliente']}.")

        st.divider()
        st.subheader("Clientes cadastrados", anchor="clientes-cadastrados")
        st.caption("Consulte os dados de identificação e contato dos seus clientes.")
        if (
            "clientes_listagem" not in st.session_state
            or st.session_state.clientes_listagem["base_url"] != api_base_url
        ):
            st.session_state.clientes_listagem = {
                "base_url": api_base_url, "dados": None, "erro": None
            }

        if st.button("Atualizar lista", key="atualizar_clientes"):
            try:
                with st.spinner("Consultando clientes..."):
                    clientes = listar_clientes(api_base_url)
            except ListagemError as error:
                st.session_state.clientes_listagem = {
                    "base_url": api_base_url, "dados": None, "erro": str(error)
                }
            else:
                st.session_state.clientes_listagem = {
                    "base_url": api_base_url, "dados": clientes, "erro": None
                }

        listagem = st.session_state.clientes_listagem
        if listagem["erro"]:
            st.error(listagem["erro"])
        elif listagem["dados"] is None:
            st.info("Clique em Atualizar lista para consultar os clientes.")
        elif not listagem["dados"]:
            st.info("Nenhum cliente cadastrado.")
        else:
            st.caption("Resultado da última consulta. Use Atualizar lista para buscar os dados atuais.")
            st.dataframe(
                [
                    {
                        "ID": cliente["id_cliente"],
                        "Nome": cliente["nome"],
                        "CPF": cliente["cpf"],
                        "Telefone": cliente["telefone"],
                        "E-mail": cliente["email"],
                    }
                    for cliente in listagem["dados"]
                ],
                hide_index=True,
            )
