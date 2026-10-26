"""Contrato proposto de Equipamentos. Sem retry, credenciais ou acesso na importação."""

import requests


CAMPOS = ("tipo", "marca", "modelo", "numero_serie", "id_cliente")
AUSENTE = "Equipamento nao encontrado."
BLOQUEIO = "Equipamento possui ordens de servico vinculadas. Exclusao bloqueada."


class EquipamentoError(Exception):
    def __init__(self, message, *, incerto=False):
        super().__init__(message)
        self.incerto = incerto


class EquipamentoNaoEncontrado(EquipamentoError):
    pass


class ExclusaoBloqueada(EquipamentoError):
    pass


def _id(value):
    if type(value) is not int or value <= 0:
        raise EquipamentoError("Informe um identificador inteiro positivo.")
    return value


def _dados(value):
    if not isinstance(value, dict) or not isinstance(value.get("tipo"), str):
        raise EquipamentoError("Informe tipo como texto e um cliente válido.")
    _id(value.get("id_cliente"))
    for campo in ("marca", "modelo", "numero_serie"):
        if campo not in value or (value[campo] is not None and not isinstance(value[campo], str)):
            raise EquipamentoError("Marca, modelo e número de série devem ser texto ou sem valor.")
    return {campo: value[campo] for campo in CAMPOS}


def _equipamento(value, expected=None):
    if not isinstance(value, dict):
        raise ValueError
    try:
        identificador = _id(value.get("id_equipamento"))
        dados = _dados(value)
    except EquipamentoError:
        raise ValueError from None
    if expected is not None and identificador != expected:
        raise ValueError
    return {"id_equipamento": identificador, **dados}


def _request(base, method, identificador=None, dados=None):
    escrita = method in ("POST", "PUT", "DELETE")
    url = f"{base.rstrip('/')}/equipamentos"
    if identificador is not None:
        url += f"/{_id(identificador)}"
    options = {"timeout": (5, 20), "allow_redirects": False}
    if method in ("POST", "PUT"):
        options["json"] = _dados(dados)
    try:
        response = requests.request(method, url, **options)
    except requests.RequestException:
        raise EquipamentoError(
            "Falha de comunicação. Confira o estado atual antes de tentar novamente.",
            incerto=escrita,
        ) from None
    try:
        body = response.json()
    except ValueError:
        body = None
    status = response.status_code
    if status == 404 and isinstance(body, dict) and (
        body.get("code") == "ERROR_CODE_NOT_FOUND" and body.get("message") == AUSENTE
    ):
        raise EquipamentoNaoEncontrado("Equipamento não encontrado.")
    if method == "DELETE" and status == 400 and isinstance(body, dict) and (
        body.get("code") == "ERROR_CODE_INPUT_ERROR" and body.get("message") == BLOQUEIO
    ):
        raise ExclusaoBloqueada("Equipamento possui OS vinculadas. Exclusão bloqueada.")
    if status != 200:
        incerto = escrita and (status == 408 or status >= 500 or status < 400 or status == 404)
        raise EquipamentoError(
            "Não foi possível confirmar a operação. Confira o estado atual."
            if incerto else "O serviço rejeitou a operação ou não retornou o resultado esperado.",
            incerto=incerto,
        )
    try:
        if method == "DELETE":
            if not isinstance(body, dict) or type(body.get("id_equipamento")) is not int or (
                body["id_equipamento"] != identificador or body.get("excluido") is not True
            ):
                raise ValueError
            return {"id_equipamento": identificador, "excluido": True}
        if method == "GET" and identificador is None:
            if not isinstance(body, list):
                raise ValueError
            return [_equipamento(item) for item in body]
        return _equipamento(body, identificador)
    except ValueError:
        raise EquipamentoError("Resposta fora do contrato esperado. Confira o estado atual.", incerto=escrita) from None


def cadastrar_equipamento(base, dados):
    return _request(base, "POST", dados=dados)


def listar_equipamentos(base):
    return _request(base, "GET")


def consultar_equipamento(base, identificador):
    return _request(base, "GET", _id(identificador))


def atualizar_equipamento(base, identificador, dados):
    return _request(base, "PUT", _id(identificador), dados)


def excluir_equipamento(base, identificador):
    return _request(base, "DELETE", _id(identificador))
