# Proposal

## Why

Estruturar o MVP acadêmico de Assistência Técnica conforme os requisitos do trabalho da faculdade. O sistema permitirá cadastrar os dados da assistência e acompanhar ordens de serviço e serviços realizados.

## What Changes

- Definir exatamente cinco entidades: Cliente, Equipamento, Ordem de Serviço, Técnico e Serviço, com os atributos, chaves e relacionamentos informados.
- Permitir cadastro, consulta, atualização e exclusão (CRUD) das cinco entidades.
- Permitir consulta de ordens de serviço e alteração de status entre Aguardando avaliação, Em manutenção, Aguardando peça, Concluído e Entregue.
- Permitir acompanhamento dos serviços realizados vinculados a cada ordem de serviço.
- Nesta mudança de planejamento, produzir somente proposta, especificações, design e tarefas; a implementação depende de uma solicitação posterior.

## Capabilities

### New Capabilities

- `gestao-assistencia-tecnica`: Modelo das cinco entidades e seus relacionamentos, CRUDs, consulta de ordens, alteração de status e acompanhamento de serviços.

### Modified Capabilities

Nenhuma.

## Impact

O repositório contém apenas a estrutura do OpenSpec e as skills, sem implementação ou especificações anteriores. A futura implementação abrangerá persistência e operações de acesso às cinco entidades. A arquitetura será Xano para backend, persistência e APIs REST, e Streamlit com Python para frontend web, consumindo as APIs REST do Xano. Código e artefatos serão versionados com Git e GitHub; OpenSpec e Codex continuarão sendo utilizados para especificação e desenvolvimento assistido. As tarefas separam configuração manual no Xano de implementação no projeto Streamlit. Esta revisão altera apenas o planejamento técnico e preserva integralmente os requisitos funcionais, entidades, atributos, relacionamentos e regras existentes.

