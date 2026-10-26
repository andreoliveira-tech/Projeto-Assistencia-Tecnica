"""Configuração externa dos grupos de APIs, sem acesso à rede."""

import os
from urllib.parse import urlsplit


def load_api_base_url() -> str | None:
    """Retorna a URL do grupo de APIs ou None quando não configurada."""
    return _load_group_url("XANO_CLIENTES_API_BASE_URL")


def load_equipamentos_api_base_url() -> str | None:
    """Configuração independente; não presume grupo publicado nem acessa rede."""
    return _load_group_url("XANO_EQUIPAMENTOS_API_BASE_URL")


def equipamentos_delete_validado() -> bool:
    """Habilita exclusão somente por opt-in após publicação e validação remota."""
    return os.environ.get("XANO_EQUIPAMENTOS_DELETE_VALIDATED", "").strip().lower() == "true"


def _load_group_url(variable: str) -> str | None:
    value = os.environ.get(variable, "").strip()
    if not value:
        return None

    message = (
        f"{variable} deve ser uma URL HTTPS do grupo "
        + ("Clientes" if variable == "XANO_CLIENTES_API_BASE_URL" else "Equipamentos") + ", "
        "sem credenciais, parâmetros de consulta ou fragmento."
    )
    try:
        parts = urlsplit(value)
        port = parts.port
    except ValueError:
        raise ValueError(message) from None

    if (
        parts.scheme != "https"
        or not parts.hostname
        or parts.username is not None
        or parts.password is not None
        or parts.query
        or parts.fragment
        or any(character.isspace() for character in value)
        or (port is not None and port == 0)
    ):
        raise ValueError(message)

    return value.rstrip("/")
