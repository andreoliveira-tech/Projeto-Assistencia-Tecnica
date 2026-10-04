# Spec Delta

## Purpose

Permitir a gestão acadêmica de uma assistência técnica por meio de cinco entidades relacionadas, seus CRUDs e do acompanhamento de ordens de serviço e serviços realizados.

## ADDED Requirements

### Requirement: Modelo com exatamente cinco entidades

O sistema SHALL possuir exatamente as cinco entidades abaixo, com os atributos e chaves indicados:

| Entidade | Atributos |
| --- | --- |
| Cliente | id_cliente (PK), nome, cpf, telefone, email |
| Equipamento | id_equipamento (PK), tipo, marca, modelo, numero_serie, id_cliente (FK) |
| Ordem de Serviço | id_os (PK), data_entrada, data_saida, problema_relatado, status, valor_total, id_equipamento (FK), id_tecnico (FK) |
| Técnico | id_tecnico (PK), nome, especialidade, telefone, email |
| Serviço | id_servico (PK), descricao, valor, id_os (FK) |

#### Scenario: Representação dos dados acadêmicos
- **WHEN** o modelo de dados do sistema é inspecionado
- **THEN** ele contém exatamente Cliente, Equipamento, Ordem de Serviço, Técnico e Serviço, com os atributos, PKs e FKs definidos na tabela

### Requirement: Relacionamentos das entidades

O sistema SHALL representar Cliente 1:N Equipamento, Equipamento 1:N Ordem de Serviço, Ordem de Serviço N:1 Técnico e Ordem de Serviço 1:N Serviço por meio das FKs especificadas.

#### Scenario: Equipamentos de um cliente
- **WHEN** dois equipamentos são cadastrados para o mesmo cliente
- **THEN** ambos referenciam esse cliente por id_cliente

#### Scenario: Ordens de um equipamento
- **WHEN** duas ordens de serviço são cadastradas para o mesmo equipamento
- **THEN** ambas referenciam esse equipamento por id_equipamento

#### Scenario: Técnico de várias ordens
- **WHEN** duas ordens de serviço são vinculadas ao mesmo técnico
- **THEN** cada ordem referencia esse técnico por id_tecnico

#### Scenario: Serviços de uma ordem
- **WHEN** dois serviços são cadastrados para a mesma ordem de serviço
- **THEN** ambos referenciam essa ordem por id_os

### Requirement: CRUD das cinco entidades

O sistema SHALL permitir cadastrar, consultar, atualizar e excluir registros de Cliente, Equipamento, Ordem de Serviço, Técnico e Serviço, utilizando os atributos e relacionamentos definidos. Os cenários abaixo aplicam-se individualmente a cada uma das cinco entidades.

#### Scenario: Cadastro de registro
- **WHEN** o usuário cadastra um registro com seus atributos e referências aplicáveis
- **THEN** o sistema armazena o registro, identificado por sua PK, e permite consultá-lo

#### Scenario: Consulta de registro
- **WHEN** o usuário consulta um registro cadastrado
- **THEN** o sistema apresenta os atributos e referências armazenados desse registro

#### Scenario: Atualização de registro
- **WHEN** o usuário atualiza os dados de um registro cadastrado
- **THEN** uma consulta posterior apresenta os dados atualizados

#### Scenario: Exclusão de registro sem dependentes
- **WHEN** o usuário exclui um registro cadastrado sem registros dependentes
- **THEN** o registro deixa de estar disponível nas consultas

### Requirement: Consulta de ordens de serviço

O sistema SHALL permitir consultar as ordens de serviço cadastradas e os dados de uma ordem: id_os, data_entrada, data_saida, problema_relatado, status, valor_total, id_equipamento e id_tecnico.

#### Scenario: Consulta de ordens cadastradas
- **WHEN** o usuário consulta as ordens de serviço cadastradas
- **THEN** o sistema disponibiliza as ordens existentes para consulta

#### Scenario: Consulta de uma ordem
- **WHEN** o usuário consulta uma ordem de serviço cadastrada
- **THEN** o sistema apresenta seus dados, incluindo o status atual e as referências ao equipamento e ao técnico

### Requirement: Alteração de status da ordem de serviço

O sistema SHALL permitir alterar o status de uma ordem de serviço e SHALL aceitar somente Aguardando avaliação, Em manutenção, Aguardando peça, Concluído e Entregue.

#### Scenario: Alteração para um status previsto
- **WHEN** o usuário altera o status de uma ordem para qualquer um dos cinco valores previstos
- **THEN** o sistema armazena o valor escolhido e o apresenta nas consultas posteriores

#### Scenario: Status fora dos valores previstos
- **WHEN** é informada uma alteração de status para um valor fora dos cinco previstos
- **THEN** o sistema não armazena esse valor como status da ordem

### Requirement: Acompanhamento dos serviços realizados

O sistema SHALL permitir acompanhar os serviços realizados vinculados a uma ordem de serviço, consultando id_servico, descricao, valor e id_os dos serviços associados.

#### Scenario: Consulta de serviços da ordem
- **WHEN** o usuário acompanha os serviços de uma ordem que possui serviços cadastrados
- **THEN** o sistema apresenta os serviços vinculados àquela ordem com seus dados

#### Scenario: Atualização refletida no acompanhamento
- **WHEN** um serviço de uma ordem é cadastrado, atualizado ou excluído
- **THEN** a consulta posterior dos serviços dessa ordem reflete a operação realizada
