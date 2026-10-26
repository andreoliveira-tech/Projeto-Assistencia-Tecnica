# consulta-clientes-api Specification

## Purpose
Permitir recuperar clientes para consulta e para carregar os fluxos de edição e exclusão com um contrato público verificável.

## Requirements

### Requirement: Listagem pela API

A API SHALL disponibilizar GET /clientes com resposta em array de objetos contendo id_cliente, nome, cpf, telefone e email.

#### Scenario: Consulta da coleção

- **WHEN** a listagem for solicitada com sucesso
- **THEN** a API deverá retornar os clientes cadastrados no contrato documentado

### Requirement: Consulta individual pela API

A API SHALL disponibilizar GET /clientes/{id_cliente} com identificador inteiro e retornar os cinco campos do cliente existente.

#### Scenario: Cliente existente

- **WHEN** o identificador corresponder a um cliente
- **THEN** a API deverá retornar esse cliente e seu identificador

#### Scenario: Cliente inexistente

- **WHEN** o identificador não corresponder a um cliente
- **THEN** a API deverá informar ausência; o erro conhecido observado é HTTP 404 com code ERROR_CODE_NOT_FOUND e message Cliente não encontrado.
