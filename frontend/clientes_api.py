"""Integração com cadastro e consultas de clientes, sem repetição automática."""

import requests


class CadastroError(Exception):
    """Falha de cadastro que pode ser apresentada ao usuário."""


def cadastrar_cliente(base_url: str, dados: dict[str, str]) -> dict:
    """Envia uma tentativa e só confirma sucesso com resposta no contrato esperado."""
    incerto = (
        "Não foi possível confirmar o cadastro. Verifique se ele foi realizado "
        "antes de enviar novamente."
    )
    try:
        response = requests.post(
            f"{base_url.rstrip('/')}/clientes",
            json={campo: dados[campo] for campo in ("nome", "cpf", "telefone", "email")},
            timeout=(5, 20),
            allow_redirects=False,
        )
    except requests.exceptions.Timeout:
        raise CadastroError(f"Tempo de resposta excedido. {incerto}") from None
    except requests.exceptions.RequestException:
        raise CadastroError(f"Falha de comunicação com o serviço. {incerto}") from None

    if response.status_code == 408:
        raise CadastroError(f"O serviço retornou HTTP 408. {incerto}")
    try:
        payload = response.json()
    except ValueError:
        payload = None

    if 400 <= response.status_code < 500:
        message = payload.get("message") if isinstance(payload, dict) else None
        if isinstance(message, str) and message.strip():
            raise CadastroError(f"Cadastro rejeitado pelo serviço: {message[:500]}")
        raise CadastroError("O serviço rejeitou o cadastro. Confira os dados informados.")

    if not 200 <= response.status_code < 300:
        raise CadastroError(f"O serviço retornou uma resposta inesperada. {incerto}")

    if (
        not isinstance(payload, dict)
        or type(payload.get("id_cliente")) is not int
        or payload["id_cliente"] <= 0
        or any(not isinstance(payload.get(campo), str) for campo in ("nome", "cpf", "telefone", "email"))
    ):
        raise CadastroError(f"Resposta de cadastro fora do formato esperado. {incerto}")

    return payload


class ConsultaError(Exception):
    """Falha de consulta individual que pode ser apresentada ao usuário."""


class ClienteNaoEncontradoError(ConsultaError):
    """O identificador consultado não corresponde a um cliente."""


def consultar_cliente(base_url: str, id_cliente: int, *, confirmar_ausencia: bool = False) -> dict:
    """Consulta Cliente; a confirmação de exclusão exige o erro de ausência conhecido."""
    if type(id_cliente) is not int or id_cliente <= 0:
        raise ConsultaError("Informe um identificador inteiro positivo.")

    try:
        response = requests.get(
            f"{base_url.rstrip('/')}/clientes/{id_cliente}",
            timeout=(5, 20),
            allow_redirects=False,
        )
    except requests.exceptions.Timeout:
        raise ConsultaError("Tempo de resposta excedido ao consultar o cliente. Tente novamente.") from None
    except requests.exceptions.RequestException:
        raise ConsultaError("Não foi possível comunicar com o serviço de clientes. Tente novamente.") from None

    if response.status_code == 404:
        if confirmar_ausencia:
            try:
                erro = response.json()
            except ValueError:
                raise ConsultaError("HTTP 404 sem JSON válido para confirmar a ausência do cliente.") from None
            # Envelope observado no GET /clientes/2. O código sozinho também pode
            # identificar falhas de rota; a mensagem deve ser a do cliente ausente.
            if (
                not isinstance(erro, dict)
                or erro.get("code") != "ERROR_CODE_NOT_FOUND"
                or erro.get("message") != "Cliente não encontrado."
            ):
                raise ConsultaError("HTTP 404 não corresponde ao erro conhecido de cliente inexistente.")
        raise ClienteNaoEncontradoError("Cliente não encontrado.")
    if not 200 <= response.status_code < 300:
        raise ConsultaError("O serviço não conseguiu retornar o cliente. Tente novamente mais tarde.")
    try:
        payload = response.json()
    except ValueError:
        raise ConsultaError("O serviço retornou um cliente em formato inválido.") from None

    if (
        not isinstance(payload, dict)
        or type(payload.get("id_cliente")) is not int
        or payload["id_cliente"] != id_cliente
        or any(not isinstance(payload.get(campo), str) for campo in ("nome", "cpf", "telefone", "email"))
    ):
        raise ConsultaError("O serviço retornou um cliente em formato inválido.")
    return payload


class ListagemError(Exception):
    """Falha de consulta que pode ser apresentada ao usuário."""


class AtualizacaoError(Exception):
    """Falha de atualização, com indicação de resultado possivelmente incerto."""

    def __init__(self, mensagem: str, incerto: bool = False):
        super().__init__(mensagem)
        self.incerto = incerto


class ExclusaoError(Exception):
    """Falha de exclusão; resultados incertos exigem consulta antes de novo envio."""

    def __init__(self, mensagem: str, incerto: bool = False):
        super().__init__(mensagem)
        self.incerto = incerto


class ExclusaoBloqueadaError(ExclusaoError):
    """O backend recusou a exclusão por equipamentos vinculados."""


def excluir_cliente(base_url: str, id_cliente: int) -> dict:
    """Envia um único DELETE sem corpo; a confirmação por GET cabe à interface."""
    if type(id_cliente) is not int or id_cliente <= 0:
        raise ExclusaoError("Informe um identificador inteiro positivo.")

    aviso = "Não foi possível confirmar a exclusão. Confira o estado atual antes de tentar novamente."
    try:
        response = requests.delete(
            f"{base_url.rstrip('/')}/clientes/{id_cliente}",
            timeout=(5, 20),
            allow_redirects=False,
        )
    except requests.exceptions.Timeout:
        raise ExclusaoError(f"Tempo de resposta excedido. {aviso}", incerto=True) from None
    except requests.exceptions.RequestException:
        raise ExclusaoError(f"Falha de comunicação com o serviço. {aviso}", incerto=True) from None

    if response.status_code == 408:
        raise ExclusaoError(f"O serviço retornou HTTP 408. {aviso}", incerto=True)
    if response.status_code == 404:
        raise ClienteNaoEncontradoError("Cliente não encontrado.")
    try:
        payload = response.json()
    except ValueError:
        payload = None

    if 400 <= response.status_code < 500:
        mensagem = payload.get("message") if isinstance(payload, dict) else None
        if (
            response.status_code == 400
            and mensagem == "Cliente possui equipamentos vinculados. Exclusao bloqueada."
        ):
            raise ExclusaoBloqueadaError("Cliente possui equipamentos vinculados. Exclusão bloqueada.")
        if isinstance(mensagem, str) and mensagem.strip():
            raise ExclusaoError(f"Exclusão rejeitada pelo serviço: {mensagem[:500]}")
        raise ExclusaoError("O serviço rejeitou a exclusão. Nenhum sucesso foi confirmado.")

    if response.status_code != 200:
        raise ExclusaoError(f"Resposta inesperada do serviço. {aviso}", incerto=True)
    if (
        not isinstance(payload, dict)
        or type(payload.get("id_cliente")) is not int
        or payload["id_cliente"] != id_cliente
        or payload.get("excluido") is not True
    ):
        raise ExclusaoError(f"Resposta de exclusão fora do formato esperado. {aviso}", incerto=True)
    return payload


def atualizar_cliente(base_url: str, id_cliente: int, dados: dict[str, str]) -> dict:
    """Envia um único PUT; a confirmação por GET cabe ao chamador."""
    if type(id_cliente) is not int or id_cliente <= 0:
        raise AtualizacaoError("Informe um identificador inteiro positivo.")
    campos = ("nome", "cpf", "telefone", "email")
    if any(not isinstance(dados.get(campo), str) or not dados[campo].strip() for campo in campos):
        raise AtualizacaoError("Preencha nome, CPF, telefone e e-mail.")
    aviso = "Não foi possível confirmar a atualização. Confira o estado atual antes de salvar novamente."
    try:
        response = requests.put(
            f"{base_url.rstrip('/')}/clientes/{id_cliente}",
            json={campo: dados[campo] for campo in campos},
            timeout=(5, 20),
            allow_redirects=False,
        )
    except requests.exceptions.Timeout:
        raise AtualizacaoError(f"Tempo de resposta excedido. {aviso}", incerto=True) from None
    except requests.exceptions.RequestException:
        raise AtualizacaoError(f"Falha de comunicação com o serviço. {aviso}", incerto=True) from None
    if response.status_code == 408:
        raise AtualizacaoError(f"O serviço retornou HTTP 408. {aviso}", incerto=True)
    if response.status_code == 404:
        raise ClienteNaoEncontradoError("Cliente não encontrado.")
    try:
        payload = response.json()
    except ValueError:
        payload = None
    if 400 <= response.status_code < 500:
        mensagem = payload.get("message") if isinstance(payload, dict) else None
        if isinstance(mensagem, str) and mensagem.strip():
            raise AtualizacaoError(f"Atualização rejeitada pelo serviço: {mensagem[:500]}")
        raise AtualizacaoError("O serviço rejeitou a atualização. Confira os dados informados.")
    if not 200 <= response.status_code < 300:
        raise AtualizacaoError(f"Resposta inesperada do serviço. {aviso}", incerto=True)
    if (
        not isinstance(payload, dict)
        or type(payload.get("id_cliente")) is not int
        or payload["id_cliente"] != id_cliente
        or any(not isinstance(payload.get(campo), str) for campo in campos)
    ):
        raise AtualizacaoError(f"Resposta de atualização fora do formato esperado. {aviso}", incerto=True)
    return payload


def listar_clientes(base_url: str) -> list[dict]:
    """Consulta GET /clientes e verifica o contrato de lista retornado pela API."""
    try:
        response = requests.get(
            f"{base_url.rstrip('/')}/clientes",
            timeout=(5, 20),
            allow_redirects=False,
        )
    except requests.exceptions.Timeout:
        raise ListagemError("Tempo de resposta excedido ao consultar clientes. Tente atualizar a lista novamente.") from None
    except requests.exceptions.RequestException:
        raise ListagemError("Não foi possível comunicar com o serviço de clientes. Tente atualizar a lista novamente.") from None

    if not 200 <= response.status_code < 300:
        raise ListagemError("O serviço não conseguiu retornar a lista de clientes. Tente novamente mais tarde.")
    try:
        payload = response.json()
    except ValueError:
        raise ListagemError("O serviço retornou uma lista em formato inválido.") from None

    if not isinstance(payload, list) or any(
        not isinstance(cliente, dict)
        or type(cliente.get("id_cliente")) is not int
        or cliente["id_cliente"] <= 0
        or any(not isinstance(cliente.get(campo), str) for campo in ("nome", "cpf", "telefone", "email"))
        for cliente in payload
    ):
        raise ListagemError("O serviço retornou uma lista em formato inválido.")

    return payload
