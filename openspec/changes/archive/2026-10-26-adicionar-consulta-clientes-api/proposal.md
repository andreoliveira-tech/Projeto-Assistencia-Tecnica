# Proposal: Listagem e consulta individual pela API

## Why

Permitir recuperar clientes para consulta e para carregar os fluxos de edição e exclusão com um contrato público verificável.

## What Changes

- GET /clientes (4100486).
- GET /clientes/{id_cliente} (4100487), incluindo o erro conhecido de cliente inexistente.
- Contrato de resposta de cinco campos sem presumir paginação, ordenação ou filtros adicionais.

## Capabilities

### New Capabilities

- `consulta-clientes-api`: listagem e consulta individual pela api.

### Modified Capabilities

Nenhuma.

## Impact

- Código e contratos: [xano/api/clientes/clientes_GET.xs](../../../../xano/api/clientes/clientes_GET.xs), [xano/api/clientes/clientes/id_cliente_GET.xs](../../../../xano/api/clientes/clientes/id_cliente_GET.xs), [docs/api-clientes.md](../../../../docs/api-clientes.md).
- Dependências: [estruturar-clientes-xano](../../estruturar-clientes-xano/proposal.md)
- Compatibilidade: manter os contratos de Cliente e a arquitetura Xano/Streamlit existentes.
- Fora do escopo: novas entidades, autenticação de usuários e gerenciamento de equipamentos além da integridade do vínculo.

## Verification

As definições publicadas dos dois GETs foram conferidas anteriormente por metadados. O cenário integrado registrou lista 200, cliente existente 200 e ausência posterior 404. O GET anterior de ID inexistente confirmou code ERROR_CODE_NOT_FOUND e message Cliente não encontrado.; o campo adicional payload não tem valor presumido.

Os critérios e as fontes de verificação estão em [tasks.md](tasks.md) e [design.md](design.md).
