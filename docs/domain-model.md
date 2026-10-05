# Domain Model — Sistema de Assistência Técnica

## 1. Visão geral do domínio

O sistema de Assistência Técnica possui cinco conceitos principais:

- Cliente;
- Equipamento;
- Ordem de Serviço;
- Técnico;
- Serviço.

Esses conceitos representam as informações necessárias para registrar e acompanhar os atendimentos realizados pela assistência técnica.

## 2. Cliente

Representa a pessoa proprietária de um ou mais equipamentos atendidos pela assistência técnica.

### Principais informações

- id_cliente;
- nome;
- cpf;
- telefone;
- email.

### Relacionamentos

Um Cliente pode possuir vários Equipamentos.

Cada Equipamento pertence a um único Cliente.

**Cardinalidade:** Cliente 1:N Equipamento.

---

## 3. Equipamento

Representa um equipamento pertencente a um cliente e que poderá ser encaminhado para atendimento técnico.

### Principais informações

- id_equipamento;
- tipo;
- marca;
- modelo;
- numero_serie;
- id_cliente.

### Relacionamentos

Cada Equipamento pertence a um único Cliente.

Um Equipamento pode possuir várias Ordens de Serviço.

**Cardinalidades:**

- Cliente 1:N Equipamento;
- Equipamento 1:N Ordem de Serviço.

---

## 4. Ordem de Serviço

Representa o registro de um atendimento técnico realizado para determinado equipamento.

A Ordem de Serviço concentra as informações necessárias para acompanhar o atendimento, incluindo o problema relatado, o técnico responsável, o status e os serviços associados.

### Principais informações

- id_os;
- data_entrada;
- data_saida;
- problema_relatado;
- status;
- valor_total;
- id_equipamento;
- id_tecnico.

### Status previstos

Uma Ordem de Serviço deverá utilizar um dos seguintes status:

- Aguardando avaliação;
- Em manutenção;
- Aguardando peça;
- Concluído;
- Entregue.

### Relacionamentos

Cada Ordem de Serviço pertence a um único Equipamento.

Um Equipamento pode possuir várias Ordens de Serviço.

Cada Ordem de Serviço está relacionada a um Técnico.

Um Técnico pode estar relacionado a várias Ordens de Serviço.

Uma Ordem de Serviço pode possuir vários Serviços.

**Cardinalidades:**

- Equipamento 1:N Ordem de Serviço;
- Técnico 1:N Ordem de Serviço;
- Ordem de Serviço 1:N Serviço.

---

## 5. Técnico

Representa o profissional responsável pelo atendimento técnico associado às ordens de serviço.

### Principais informações

- id_tecnico;
- nome;
- especialidade;
- telefone;
- email.

### Relacionamentos

Um Técnico pode estar relacionado a várias Ordens de Serviço.

Cada Ordem de Serviço está relacionada a um Técnico.

**Cardinalidade:** Técnico 1:N Ordem de Serviço.

---

## 6. Serviço

Representa um serviço realizado no contexto de uma Ordem de Serviço.

Exemplos previstos para o domínio incluem:

- Formatação;
- Troca de tela;
- Troca de bateria;
- Limpeza interna;
- Instalação de sistema;
- Troca de componente.

### Principais informações

- id_servico;
- descricao;
- valor;
- id_os.

### Relacionamentos

Cada Serviço pertence a uma única Ordem de Serviço.

Uma Ordem de Serviço pode possuir vários Serviços.

**Cardinalidade:** Ordem de Serviço 1:N Serviço.

---

## 7. Visão geral dos relacionamentos

O modelo de domínio pode ser representado conceitualmente da seguinte forma:

Cliente
  1
  |
  N
Equipamento
  1
  |
  N
Ordem de Serviço
  |
  |--- N:1 ---> Técnico
  |
  |--- 1:N ---> Serviço

Os quatro relacionamentos principais do domínio são:

1. Cliente 1:N Equipamento;
2. Equipamento 1:N Ordem de Serviço;
3. Técnico 1:N Ordem de Serviço;
4. Ordem de Serviço 1:N Serviço.

## 8. Limites do modelo

O modelo inicial é composto pelos cinco conceitos definidos para o projeto acadêmico.

Novas entidades, atributos de domínio ou relacionamentos não deverão ser adicionados sem que uma necessidade seja identificada e analisada no processo incremental de desenvolvimento.

Este documento representa o modelo conceitual global do projeto. Detalhes físicos de persistência e implementação no Xano deverão ser tratados nas mudanças correspondentes durante o desenvolvimento.