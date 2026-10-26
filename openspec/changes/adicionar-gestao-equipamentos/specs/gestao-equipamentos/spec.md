# Spec Delta

## Purpose

Permitir gerenciar equipamentos vinculados a clientes existentes, preservando os atributos de domínio e impedindo exclusão que viole vínculos com ordens de serviço.

## ADDED Requirements

### Requirement: CRUD com os atributos de Equipamento

O sistema SHALL cadastrar, listar, consultar, atualizar e excluir equipamentos usando exclusivamente `id_equipamento`, `tipo`, `marca`, `modelo`, `numero_serie` e `id_cliente`. O identificador SHALL ser gerado pelo backend e permanecer imutável. Tipo SHALL ser textual obrigatório não nulo, sem impor conteúdo mínimo não aprovado; os três demais campos descritivos SHALL aceitar texto ou null. Número de série SHALL permanecer textual, preservando zeros à esquerda.

#### Scenario: Cadastro e atualização válidos
- **WHEN** os dados e o cliente forem válidos
- **THEN** o backend deverá persistir os campos e retorná-los em consulta posterior, sem alterar o identificador em atualizações

#### Scenario: Consulta de equipamento inexistente
- **WHEN** não existir equipamento para o identificador consultado
- **THEN** o sistema deverá informar ausência, sem apresentar dados anteriores como resultado atual

### Requirement: Cliente existente antes da persistência

O backend SHALL exigir um cliente existente por `id_cliente`, confirmando o vínculo antes de criar ou atualizar equipamento e interrompendo a operação em falha de verificação.

#### Scenario: Cliente inválido
- **WHEN** a referência for ausente, nula, não positiva ou inexistente
- **THEN** o backend deverá rejeitar a gravação sem criar ou alterar equipamento

### Requirement: Exclusão sem cascata e com verificação de OS

O backend SHALL impedir a exclusão de equipamento com OS vinculada, permitir a exclusão sem dependências após verificação bem-sucedida e interromper a exclusão se a consulta falhar ou não produzir resultado válido. Nenhuma OS SHALL ser excluída em cascata. Esta decisão complementa o planejamento atual, sem atribuição histórica, com garantia delimitada a operações sequenciais.

#### Scenario: Equipamento vinculado a OS
- **WHEN** houver OS referenciando o equipamento
- **THEN** a exclusão deverá ser bloqueada, preservando equipamento e OS

#### Scenario: Verificação indisponível
- **WHEN** não houver implementação válida da consulta de OS ou ocorrer falha na verificação
- **THEN** a exclusão deverá ser interrompida, nunca tratando desconhecimento como ausência de vínculos

### Requirement: Ações explícitas e resultados verificáveis na interface

A interface SHALL executar HTTP somente por ação do usuário, exceto os GETs posteriores para conferir gravações aceitas. Exclusão SHALL exigir carregamento e confirmação explícita; trocar identificador, recarregar ou trocar URL SHALL invalidar a confirmação. Escritas SHALL ocorrer uma vez por ação, sem retry nem redirecionamento automático. Falhas de comunicação, HTTP 408, 5xx e contratos inesperados SHALL ser apresentados como incerteza sem falso sucesso.

#### Scenario: Exclusão ainda não publicada e validada
- **WHEN** a configuração explícita `XANO_EQUIPAMENTOS_DELETE_VALIDATED` não tiver o valor `true`
- **THEN** a interface deverá manter indisponíveis os controles de exclusão, mesmo que a URL base esteja configurada, e não deverá enviar DELETE

#### Scenario: Exclusão confirmada
- **WHEN** um DELETE válido for seguido de GET com o erro de ausência previsto no contrato
- **THEN** a interface deverá confirmar exclusão e invalidar os estados pertinentes

#### Scenario: Resposta ambígua ou rerun
- **WHEN** houver resposta ambígua, rerun ou cancelamento
- **THEN** a interface não deverá repetir escrita nem afirmar exclusão com base apenas em HTTP 404 genérico
