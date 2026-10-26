# consulta-clientes-ui Specification

## Purpose
Exibir clientes e permitir consulta por identificador sem disparar chamadas em reruns e sem conservar um resultado anterior como se fosse a consulta atual.

## Requirements

### Requirement: Listagem na interface

A interface SHALL listar id_cliente, nome, cpf, telefone e email ao acionar Atualizar lista e informar lista vazia ou falha sem apresentar um resultado anterior como o atual.

#### Scenario: Atualizar lista

- **WHEN** o usuário acionar a atualização e a API retornar uma lista válida
- **THEN** a interface deverá exibir os registros ou informar que a lista está vazia

#### Scenario: Falha na lista

- **WHEN** a atualização falhar ou retornar contrato inválido
- **THEN** o resultado anterior deverá ser descartado e a falha apresentada

### Requirement: Consulta individual na interface

A interface SHALL consultar por inteiro positivo somente ao submeter o formulário, exibir os cinco campos do cliente e informar ausência ou falha, mantendo estado independente da listagem.

#### Scenario: Identificador inválido

- **WHEN** o usuário informar identificador vazio ou não positivo
- **THEN** a interface deverá rejeitar localmente sem fazer HTTP

#### Scenario: Consulta com sucesso ou ausência

- **WHEN** o usuário consultar identificador válido
- **THEN** a interface deverá apresentar o cliente retornado ou informar Cliente não encontrado para HTTP 404

#### Scenario: Troca da URL base

- **WHEN** a URL de consumo mudar
- **THEN** os resultados anteriores deverão ser invalidados
