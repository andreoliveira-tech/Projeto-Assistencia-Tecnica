# Spec Delta

## Purpose

Permitir atualizar os quatro campos de um cliente existente, preservando sua identidade e reutilizando o validador compartilhado.

## ADDED Requirements

### Requirement: Atualização pela API

A API SHALL receber PUT /clientes/{id_cliente} com nome, cpf, telefone e email obrigatórios, confirmar que o cliente existe e reutilizar o validador compartilhado dos dados de clientes antes de alterar os dados.

#### Scenario: Atualização válida

- **WHEN** um cliente existente receber dados válidos
- **THEN** a API deverá persistir os quatro campos e retorná-los para conferência por nova consulta

#### Scenario: Identificador inexistente

- **WHEN** não houver cliente para o identificador informado
- **THEN** a API deverá informar Cliente não encontrado. sem executar a alteração

### Requirement: Preservação da identidade

A atualização SHALL manter inalterado o id do cliente e apresentá-lo como id_cliente na resposta.

#### Scenario: Alteração dos dados descritivos

- **WHEN** nome, CPF, telefone ou e-mail forem atualizados com sucesso
- **THEN** o identificador retornado deverá permanecer o do cliente selecionado
