"""Integração com cadastro e listagem de clientes, sem repetição automática."""

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


class ListagemError(Exception):
    """Falha de consulta que pode ser apresentada ao usuário."""


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
