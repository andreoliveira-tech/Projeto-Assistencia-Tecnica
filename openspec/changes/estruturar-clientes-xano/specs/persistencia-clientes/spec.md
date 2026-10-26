# Spec Delta

## Purpose

Manter os dados de Cliente no Xano com correspondência explícita entre o modelo conceitual e a identidade física, sem duplicar identificadores.

## ADDED Requirements

### Requirement: Persistência de Cliente

O sistema SHALL persistir Cliente no Xano com id inteiro gerado pelo backend e com nome, cpf e telefone textuais e email do tipo e-mail.

#### Scenario: Estrutura compatível com o domínio

- **WHEN** a estrutura de Cliente for conferida
- **THEN** os campos deverão corresponder a id_cliente, nome, cpf, telefone e email do modelo, usando id como representação física de id_cliente

### Requirement: Identidade pública do cliente

As APIs SHALL representar cliente.id como id_cliente, sem exigir um identificador fornecido no cadastro nem criar um segundo identificador de domínio.

#### Scenario: Cadastro sem identificador informado

- **WHEN** um cliente válido for cadastrado sem identificador
- **THEN** o backend deverá gerar id e devolvê-lo como id_cliente para consultas posteriores
