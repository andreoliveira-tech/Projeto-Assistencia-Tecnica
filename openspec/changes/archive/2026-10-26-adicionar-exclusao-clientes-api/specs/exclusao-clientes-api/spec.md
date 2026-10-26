# Spec Delta

## Purpose

Disponibilizar exclusão de cliente sem equipamentos, preservando os relacionamentos e recusando exclusão quando a verificação de dependências não for segura.

## ADDED Requirements

### Requirement: Exclusão pela API

A API SHALL receber DELETE /clientes/{id_cliente} com identificador inteiro positivo, verificar a existência e excluir somente o cliente sem equipamentos após consulta de dependências bem-sucedida.

#### Scenario: Sem equipamentos

- **WHEN** o cliente existir e a consulta confirmar ausência de vínculos
- **THEN** a API deverá excluir o cliente e retornar id_cliente correspondente e excluido true

#### Scenario: Cliente inexistente

- **WHEN** o cliente não existir
- **THEN** a API deverá informar ausência sem declarar uma nova exclusão

### Requirement: Proteção dos vínculos na exclusão

A API SHALL bloquear a exclusão se houver equipamentos, preservar os registros vinculados e interromper a exclusão quando a consulta de dependências falhar ou retornar dados incompatíveis, sem cascata.

#### Scenario: Bloqueio por equipamentos

- **WHEN** houver equipamento vinculado ao cliente
- **THEN** o backend deverá recusar a exclusão e manter cliente e equipamentos

#### Scenario: Falha na verificação

- **WHEN** a consulta de vínculos falhar ou não produzir um retorno válido
- **THEN** a API deverá interromper a exclusão e informar erro, sem atribuir automaticamente a falha à existência de equipamentos
