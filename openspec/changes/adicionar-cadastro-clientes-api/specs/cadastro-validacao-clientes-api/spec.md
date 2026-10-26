# Spec Delta

## Purpose

Disponibilizar cadastro de clientes pela API e centralizar as regras de dados usadas também na atualização, mantendo explícita a verificação integrada ainda pendente.

## ADDED Requirements

### Requirement: Cadastro pela API

A API SHALL receber POST /clientes com nome, cpf, telefone e email obrigatórios, sem identificador no corpo, validar os dados antes da escrita e retornar id_cliente e os quatro campos persistidos.

#### Scenario: Cadastro válido consultável

- **WHEN** um cadastro válido for aceito
- **THEN** a API deverá retornar o cliente com identificador gerado e permitir sua consulta

### Requirement: Validação compartilhada antes da escrita

O backend SHALL exigir nome não vazio após trim, CPF com 11 dígitos e dois verificadores matematicamente válidos, telefone com DDD e 10 ou 11 dígitos e e-mail obrigatório em formato válido, tanto no cadastro quanto na atualização.

#### Scenario: Campo inválido ou obrigatório ausente

- **WHEN** POST ou PUT contiver campo obrigatório ausente, nulo ou inválido, ainda que os demais sejam válidos
- **THEN** o backend deverá rejeitar a solicitação inteira e informar erro sem criar nem alterar registros

#### Scenario: CPF com dígitos inválidos

- **WHEN** o CPF possuir quantidade incorreta de dígitos, todos os dígitos iguais ou verificadores inválidos
- **THEN** o backend deverá rejeitar a escrita

#### Scenario: Nome, telefone ou e-mail inválido

- **WHEN** o nome for vazio após trim, o telefone não tiver DDD e 10 ou 11 dígitos ou o e-mail tiver formato inválido
- **THEN** o backend deverá rejeitar a escrita

### Requirement: Normalização textual

O backend SHALL aceitar CPF e telefone com ou sem máscara, remover as máscaras previstas antes de validar e persistir somente dígitos como texto, preservando zeros à esquerda em POST e PUT.

#### Scenario: Máscara e zeros à esquerda

- **WHEN** dados válidos com máscaras ou zeros à esquerda forem enviados
- **THEN** o backend deverá preservar os dígitos e os zeros à esquerda, armazenando CPF e telefone como texto sem máscara
