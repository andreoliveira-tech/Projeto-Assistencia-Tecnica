# Spec Delta

## Purpose

Preparar o vínculo Cliente 1:N Equipamento necessário ao bloqueio de exclusão, sem antecipar gerenciamento de equipamentos.

## ADDED Requirements

### Requirement: Estrutura mínima de Equipamento

O backend SHALL manter equipamento com id inteiro nativo, tipo textual obrigatório não nulo, marca, modelo e numero_serie textuais opcionais e anuláveis e id_cliente inteiro obrigatório não nulo referenciando cliente.id, com índice não exclusivo.

#### Scenario: Correspondência conceitual

- **WHEN** a estrutura for conferida
- **THEN** id deverá representar id_equipamento, numero_serie deverá preservar representação textual e não deverá existir identificador de domínio duplicado

### Requirement: Vínculo obrigatório em operações sequenciais

O backend SHALL permitir vários equipamentos para um cliente e confirmar a existência do cliente antes de persistir um vínculo, rejeitando referência ausente, nula ou inexistente e interrompendo a operação se a consulta falhar.

#### Scenario: Vínculo inválido

- **WHEN** for tentado um vínculo sem cliente válido
- **THEN** o backend deverá rejeitar a persistência do vínculo

#### Scenario: Cardinalidade um para muitos

- **WHEN** dois equipamentos forem vinculados sequencialmente ao mesmo cliente existente
- **THEN** ambos deverão referenciar o mesmo cliente.id por id_cliente

### Requirement: Consulta de dependências para exclusão

O backend SHALL identificar vínculos por equipamento.id_cliente para apoiar a exclusão de clientes e interromper o procedimento se a verificação falhar, no escopo sequencial aprovado.

#### Scenario: Dependência existente

- **WHEN** houver equipamento cujo id_cliente corresponda ao cliente consultado
- **THEN** a consulta deverá indicar bloqueio da exclusão do cliente
