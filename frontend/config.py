"""Configuração externa da API de Clientes, sem acesso à rede."""

import os
from urllib.parse import urlsplit


def load_api_base_url() -> str | None:
    """Retorna a URL do grupo de APIs ou None quando não configurada."""
    value = os.environ.get("XANO_CLIENTES_API_BASE_URL", "").strip()
    if not value:
        return None

    message = (
        "XANO_CLIENTES_API_BASE_URL deve ser uma URL HTTPS do grupo Clientes, "
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
