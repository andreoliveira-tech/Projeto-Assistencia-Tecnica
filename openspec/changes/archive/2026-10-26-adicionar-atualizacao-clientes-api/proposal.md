# Proposal: Atualização de clientes pela API

## Why

Permitir atualizar os quatro campos de um cliente existente, preservando sua identidade e reutilizando o validador compartilhado.

## What Changes

- PUT /clientes/{id_cliente} (4100488), com os quatro campos obrigatórios.
- Consulta de existência, validação compartilhada e retorno dos dados atualizados.
- Separação entre evidência de atualização válida e a validação completa pendente na Change `adicionar-cadastro-clientes-api`.

## Capabilities

### New Capabilities

- `atualizacao-clientes-api`: atualização de clientes pela api.

### Modified Capabilities

Nenhuma.

## Impact

- Código e contratos: [xano/api/clientes/clientes/id_cliente_PUT.xs](../../../../xano/api/clientes/clientes/id_cliente_PUT.xs), [docs/api-clientes.md](../../../../docs/api-clientes.md), [frontend/clientes_api.py](../../../../frontend/clientes_api.py).
- Dependências: [estruturar-clientes-xano](../../estruturar-clientes-xano/proposal.md), [adicionar-cadastro-clientes-api](../../adicionar-cadastro-clientes-api/proposal.md), [adicionar-consulta-clientes-api](../2026-10-26-adicionar-consulta-clientes-api/proposal.md)
- Compatibilidade: manter os contratos de Cliente e a arquitetura Xano/Streamlit existentes.
- Fora do escopo: novas entidades, autenticação de usuários e gerenciamento de equipamentos além da integridade do vínculo.

## Verification

O PUT local e a definição publicada documentada consultam a existência, chamam clientes/validar_dados e então db.edit. A tarefa original 2.4 já estava concluída com persistência e nova consulta. A rodada documentada de 49 testes verificou a integração Python por simulação e não executou novo PUT real.

Os critérios e as fontes de verificação estão em [tasks.md](tasks.md) e [design.md](design.md).
