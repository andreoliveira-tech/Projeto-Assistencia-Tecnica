# Spec Delta

## Purpose

Permitir editar um cliente previamente carregado e confirmar os dados por nova consulta, distinguindo atualização rejeitada de resultado incerto.

## ADDED Requirements

### Requirement: Edição de cliente carregado

A interface SHALL carregar o cliente por GET antes de permitir edição, fixar seu identificador e enviar nome, cpf, telefone e email por PUT somente ao acionar Salvar alterações.

#### Scenario: Salvar cliente carregado

- **WHEN** o usuário alterar os campos válidos e solicitar gravação
- **THEN** a interface deverá enviar uma única tentativa para o identificador carregado

### Requirement: Confirmação de atualização

A interface SHALL apresentar sucesso somente após resposta de PUT válida e GET posterior com os mesmos cinco campos retornados pelo PUT.

#### Scenario: Conferência correspondente

- **WHEN** a nova consulta coincidir com o retorno validado da atualização
- **THEN** a interface deverá confirmar sucesso e apresentar os dados consultados

#### Scenario: Conferência divergente ou falha

- **WHEN** o GET falhar ou retornar dados diferentes
- **THEN** a interface deverá informar incerteza e não confirmar sucesso

### Requirement: Recuperação segura da edição

A interface SHALL preservar os campos em rejeições, invalidar edição de cliente inexistente e bloquear nova escrita após resultado incerto, inclusive HTTP 408, até conferência manual por GET.

#### Scenario: Conferir estado atual

- **WHEN** o usuário solicitar conferência após incerteza
- **THEN** a interface deverá executar somente GET e recarregar os dados sem atribuir sucesso à tentativa anterior

#### Scenario: Cliente não encontrado

- **WHEN** o serviço responder que o cliente não existe
- **THEN** a interface deverá invalidar o formulário de edição sem declarar sucesso
