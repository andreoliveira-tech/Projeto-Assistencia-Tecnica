"""Cadastro de clientes com envio exclusivamente por submissão do formulário."""

import streamlit as st
from pathlib import Path

from config import load_api_base_url
from clientes_api import (
    CadastroError, ClienteNaoEncontradoError, ConsultaError, ListagemError,
    AtualizacaoError, atualizar_cliente, cadastrar_cliente, consultar_cliente, listar_clientes,
    ExclusaoError, ExclusaoBloqueadaError, excluir_cliente,
)


def novo_estado_exclusao(base_url, selecao="", geracao=0):
    return {
        "base_url": base_url, "selecao": selecao, "geracao": geracao,
        "id_cliente": None, "dados": None, "erro": None, "aviso": None,
        "sucesso": False, "conferir": False,
    }


def invalidar_cliente_ausente(base_url, id_cliente):
    """Invalida resultados locais, sem novas consultas nem alterações de outros clientes."""
    listagem = st.session_state.get("clientes_listagem")
    if listagem and listagem["base_url"] == base_url:
        listagem.update(dados=None, erro=None)
    consulta = st.session_state.get("cliente_consulta")
    if consulta and consulta["base_url"] == base_url and consulta["id_cliente"] == id_cliente:
        consulta.update(dados=None, erro="Cliente não encontrado.", nao_encontrado=True)
    edicao = st.session_state.get("cliente_edicao")
    if edicao and edicao["base_url"] == base_url and edicao["id_cliente"] == id_cliente:
        edicao.update(
            id_cliente=None, dados=None, confirmado=None, sucesso=False,
            conferir=False, erro="Cliente não encontrado.", geracao=edicao["geracao"] + 1,
        )


def conferir_exclusao(base_url, estado, resposta_valida=False):
    """Confere ausência por GET; somente uma resposta válida anterior permite declarar sucesso."""
    estado.update(erro=None, aviso=None, sucesso=False)
    try:
        cliente = consultar_cliente(base_url, estado["id_cliente"], confirmar_ausencia=True)
    except ClienteNaoEncontradoError:
        invalidar_cliente_ausente(base_url, estado["id_cliente"])
        estado.update(dados=None, conferir=False, sucesso=resposta_valida)
        if not resposta_valida:
            estado["aviso"] = (
                "Cliente não encontrado na conferência atual. "
                "Isso não confirma que a tentativa anterior realizou a exclusão."
            )
    except ConsultaError:
        estado.update(dados=None, conferir=True)
        estado["erro"] = (
            "Não foi possível conferir a ausência do cliente. "
            "Use Conferir estado atual da exclusão antes de uma nova tentativa."
        )
    else:
        if resposta_valida:
            estado.update(dados=None, conferir=True)
            estado["erro"] = (
                "O serviço respondeu à exclusão, mas o cliente ainda foi encontrado. "
                "Confira o estado atual antes de tentar novamente."
            )
        else:
            estado.update(dados=cliente, conferir=False)
            estado["aviso"] = "O cliente existe na consulta atual. Uma nova exclusão exige nova confirmação."


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
        '<a href="#consultar-cliente" target="_self">Consultar cliente <span>↗</span></a>'
        '<a href="#editar-cliente" target="_self">Editar cliente <span>↗</span></a>'
        '<a href="#excluir-cliente" target="_self">Excluir cliente <span>↗</span></a>'
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

        st.divider()
        st.subheader("Consultar cliente", anchor="consultar-cliente")
        st.caption("Informe o identificador para consultar um cliente específico.")
        if (
            "cliente_consulta" not in st.session_state
            or st.session_state.cliente_consulta["base_url"] != api_base_url
        ):
            st.session_state.cliente_consulta = {
                "base_url": api_base_url, "id_cliente": None,
                "dados": None, "erro": None, "nao_encontrado": False,
            }

        with st.form("consulta_cliente", clear_on_submit=False, enter_to_submit=False):
            identificador = st.text_input("Identificador do cliente", key="consulta_id_cliente")
            consultar = st.form_submit_button("Consultar cliente", type="primary")

        if consultar:
            estado = {
                "base_url": api_base_url, "id_cliente": None,
                "dados": None, "erro": None, "nao_encontrado": False,
            }
            st.session_state.cliente_consulta = estado
            texto_id = identificador.strip()
            try:
                if not texto_id or any(caractere not in "0123456789" for caractere in texto_id):
                    raise ValueError
                id_consulta = int(texto_id)
                if id_consulta <= 0:
                    raise ValueError
            except ValueError:
                estado["erro"] = "Informe um identificador inteiro positivo."
            else:
                estado["id_cliente"] = id_consulta
                try:
                    with st.spinner("Consultando cliente..."):
                        estado["dados"] = consultar_cliente(api_base_url, id_consulta)
                except ClienteNaoEncontradoError as error:
                    estado["erro"] = str(error)
                    estado["nao_encontrado"] = True
                except ConsultaError as error:
                    estado["erro"] = str(error)

        consulta = st.session_state.cliente_consulta
        if consulta["erro"]:
            if consulta["nao_encontrado"]:
                st.info(consulta["erro"])
            else:
                st.error(consulta["erro"])
        elif consulta["dados"] is not None:
            st.caption(f"Resultado da última consulta ao cliente {consulta['id_cliente']}.")
            cliente_consultado = consulta["dados"]
            st.dataframe(
                [{
                    "ID": cliente_consultado["id_cliente"],
                    "Nome": cliente_consultado["nome"],
                    "CPF": cliente_consultado["cpf"],
                    "Telefone": cliente_consultado["telefone"],
                    "E-mail": cliente_consultado["email"],
                }],
                hide_index=True,
            )
        else:
            st.info("Informe o identificador e clique em Consultar cliente.")

        st.divider()
        st.subheader("Editar cliente", anchor="editar-cliente")
        if (
            "cliente_edicao" not in st.session_state
            or st.session_state.cliente_edicao["base_url"] != api_base_url
        ):
            st.session_state.cliente_edicao = {
                "base_url": api_base_url, "id_cliente": None, "geracao": 0,
                "dados": None, "confirmado": None, "erro": None,
                "sucesso": False, "conferir": False,
            }
        edicao = st.session_state.cliente_edicao
        with st.form("carregar_edicao", clear_on_submit=False, enter_to_submit=False):
            id_edicao = st.text_input("Identificador para edição", key="edicao_selecao_id")
            carregar = st.form_submit_button("Carregar para edição")

        conferir = False
        if edicao["conferir"]:
            conferir = st.button("Conferir estado atual", key="conferir_edicao")
        if carregar or conferir:
            edicao.update(erro=None, sucesso=False, confirmado=None)
            try:
                if carregar:
                    texto = id_edicao.strip()
                    if not texto or any(c not in "0123456789" for c in texto):
                        raise ValueError
                    alvo = int(texto)
                    if alvo <= 0:
                        raise ValueError
                else:
                    alvo = edicao["id_cliente"]
                # Descarta o alvo anterior antes de carregar outro cliente.
                edicao["dados"] = None
                edicao["id_cliente"] = alvo
                with st.spinner("Carregando cliente para edição..."):
                    edicao["dados"] = consultar_cliente(api_base_url, alvo)
            except ValueError:
                edicao.update(dados=None, id_cliente=None, conferir=False)
                edicao["erro"] = "Informe um identificador inteiro positivo."
            except ConsultaError as error:
                edicao["erro"] = str(error)
            else:
                edicao["geracao"] += 1
                edicao["conferir"] = False

        if edicao["dados"] is not None:
            st.caption(f"Cliente em edição: {edicao['id_cliente']}. O identificador será preservado.")
            with st.form("editar_cliente", clear_on_submit=False, enter_to_submit=False):
                dados_edicao = {
                    campo: st.text_input(
                        rotulo, value=edicao["dados"][campo],
                        key=f"edicao_{campo}_{edicao['geracao']}",
                    )
                    for campo, rotulo in (
                        ("nome", "Nome para edição"), ("cpf", "CPF para edição"),
                        ("telefone", "Telefone para edição"), ("email", "E-mail para edição"),
                    )
                }
                salvar = st.form_submit_button("Salvar alterações", disabled=edicao["conferir"])
            if salvar and not edicao["conferir"]:
                edicao.update(erro=None, sucesso=False, confirmado=None)
                try:
                    with st.spinner("Salvando alterações..."):
                        atualizado = atualizar_cliente(api_base_url, edicao["id_cliente"], dados_edicao)
                except ClienteNaoEncontradoError as error:
                    edicao.update(dados=None, erro=str(error))
                except AtualizacaoError as error:
                    edicao.update(erro=str(error), conferir=error.incerto)
                else:
                    edicao["conferir"] = True
                    try:
                        with st.spinner("Confirmando atualização por nova consulta..."):
                            confirmado = consultar_cliente(api_base_url, edicao["id_cliente"])
                    except ConsultaError:
                        edicao["erro"] = (
                            "O serviço respondeu à atualização, mas a nova consulta falhou. "
                            "Confira o estado atual antes de salvar novamente."
                        )
                    else:
                        campos = ("id_cliente", "nome", "cpf", "telefone", "email")
                        if any(confirmado[c] != atualizado[c] for c in campos):
                            edicao["erro"] = (
                                "Os dados consultados diferem da resposta da atualização. "
                                "Confira o estado atual antes de salvar novamente."
                            )
                        else:
                            edicao.update(confirmado=confirmado, sucesso=True, conferir=False)
                # Reflete imediatamente o bloqueio de novo envio ou o sucesso,
                # sem depender de uma interação posterior para redesenhar o botão.
                st.rerun()
        if edicao["erro"]:
            st.error(edicao["erro"])
        if edicao["sucesso"]:
            st.success("Atualização confirmada por nova consulta.")
            cliente_confirmado = edicao["confirmado"]
            st.dataframe(
                [{rotulo: cliente_confirmado[campo] for campo, rotulo in (
                    ("id_cliente", "ID"), ("nome", "Nome"), ("cpf", "CPF"),
                    ("telefone", "Telefone"), ("email", "E-mail"),
                )}], hide_index=True,
            )
        if edicao["conferir"]:
            st.warning("Atualização sem confirmação. Use Conferir estado atual antes de um novo envio.")

        st.divider()
        st.subheader("Excluir cliente", anchor="excluir-cliente")
        anterior = st.session_state.get("cliente_exclusao")
        if anterior is None or anterior["base_url"] != api_base_url:
            st.session_state.cliente_exclusao = novo_estado_exclusao(
                api_base_url, geracao=(anterior["geracao"] + 1 if anterior else 0)
            )
        exclusao = st.session_state.cliente_exclusao
        selecao = st.text_input(
            "Identificador para exclusão", key="exclusao_selecao_id",
            disabled=exclusao["conferir"],
        ).strip()
        if selecao != exclusao["selecao"]:
            exclusao = novo_estado_exclusao(api_base_url, selecao, exclusao["geracao"] + 1)
            st.session_state.cliente_exclusao = exclusao

        if st.button("Carregar para exclusão", key="carregar_exclusao", disabled=exclusao["conferir"]):
            exclusao = novo_estado_exclusao(api_base_url, selecao, exclusao["geracao"] + 1)
            st.session_state.cliente_exclusao = exclusao
            try:
                if not selecao or any(c not in "0123456789" for c in selecao):
                    raise ValueError
                alvo = int(selecao)
                if alvo <= 0:
                    raise ValueError
                exclusao["id_cliente"] = alvo
                with st.spinner("Carregando cliente para exclusão..."):
                    exclusao["dados"] = consultar_cliente(api_base_url, alvo)
            except ValueError:
                exclusao["erro"] = "Informe um identificador inteiro positivo."
            except ClienteNaoEncontradoError as error:
                invalidar_cliente_ausente(api_base_url, alvo)
                exclusao["aviso"] = str(error)
                st.rerun()
            except ConsultaError as error:
                exclusao["erro"] = str(error)

        if exclusao["conferir"]:
            st.warning("Resultado sem confirmação. Não reenvie a exclusão antes de conferir o estado atual.")
            if st.button("Conferir estado atual da exclusão", key="conferir_exclusao"):
                with st.spinner("Conferindo estado atual..."):
                    conferir_exclusao(api_base_url, exclusao)
                st.rerun()

        if exclusao["dados"] is not None:
            cliente_alvo = exclusao["dados"]
            st.write(f"Cliente selecionado: {cliente_alvo['id_cliente']} — {cliente_alvo['nome']}")
            st.warning(
                "A exclusão é definitiva. Clientes com equipamentos vinculados "
                "terão a exclusão bloqueada pelo serviço."
            )
            confirmar = st.checkbox(
                f"Confirmo a exclusão do cliente {cliente_alvo['id_cliente']} — {cliente_alvo['nome']}",
                key=f"exclusao_confirmacao_{exclusao['geracao']}",
            )
            if st.button("Excluir definitivamente", key="excluir_definitivamente", disabled=not confirmar) and confirmar:
                # Consome a seleção antes da tentativa: reruns não podem reenviar o DELETE.
                exclusao.update(dados=None, erro=None, aviso=None, sucesso=False)
                exclusao["geracao"] += 1
                try:
                    with st.spinner("Excluindo cliente..."):
                        excluir_cliente(api_base_url, exclusao["id_cliente"])
                except ClienteNaoEncontradoError as error:
                    invalidar_cliente_ausente(api_base_url, exclusao["id_cliente"])
                    exclusao["aviso"] = str(error)
                except ExclusaoBloqueadaError as error:
                    exclusao["erro"] = str(error)
                except ExclusaoError as error:
                    exclusao.update(erro=str(error), conferir=error.incerto)
                else:
                    with st.spinner("Confirmando ausência por nova consulta..."):
                        conferir_exclusao(api_base_url, exclusao, resposta_valida=True)
                st.rerun()

        if exclusao["id_cliente"] is not None:
            if st.button("Cancelar", key="cancelar_exclusao"):
                st.session_state.cliente_exclusao = novo_estado_exclusao(
                    api_base_url, selecao, exclusao["geracao"] + 1
                )
                st.rerun()
        if exclusao["erro"]:
            st.error(exclusao["erro"])
        if exclusao["aviso"]:
            st.info(exclusao["aviso"])
        if exclusao["sucesso"]:
            st.success("Exclusão confirmada por nova consulta: cliente não encontrado.")
