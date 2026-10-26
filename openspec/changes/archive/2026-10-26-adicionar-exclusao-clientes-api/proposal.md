# Proposal: Exclusão de clientes pela API com bloqueio de vínculos

## Why

Disponibilizar exclusão de cliente sem equipamentos, preservando os relacionamentos e recusando exclusão quando a verificação de dependências não for segura.

## What Changes

- DELETE /clientes/{id_cliente} (4107955), identificador positivo sem corpo.
- Verificações de existência e dependências antes da única exclusão.
- Resposta id_cliente/excluido, bloqueio por equipamentos e interrupção em falha de consulta.

## Capabilities

### New Capabilities

- `exclusao-clientes-api`: exclusão de clientes pela api com bloqueio de vínculos.

### Modified Capabilities

Nenhuma.

## Impact

- Código e contratos: [docs/api-clientes.md](../../../../docs/api-clientes.md), [openspec/changes/mvp-assistencia-tecnica/design.md](../../mvp-assistencia-tecnica/design.md), [frontend/clientes_api.py](../../../../frontend/clientes_api.py).
- Dependências: [estruturar-clientes-xano](../../estruturar-clientes-xano/proposal.md), [adicionar-consulta-clientes-api](../2026-10-26-adicionar-consulta-clientes-api/proposal.md), [garantir-integridade-cliente-equipamento](../../garantir-integridade-cliente-equipamento/proposal.md)
- Compatibilidade: manter os contratos de Cliente e a arquitetura Xano/Streamlit existentes.
- Fora do escopo: novas entidades, autenticação de usuários e gerenciamento de equipamentos além da integridade do vínculo.

## Verification

A definição publicada foi inspecionada anteriormente com include_draft=false e include_xanoscript=true; o DELETE não possui arquivo XanoScript local. A 2.5 registra testes reais de bloqueio com equipamento (400), inexistente (404) e exclusão sem vínculo (200). A falha de dependências foi verificada por inspeção e simulação Python, não por falha integrada no Xano. O cenário posterior da interface excluiu somente o descartável 13.

Os critérios e as fontes de verificação estão em [tasks.md](tasks.md) e [design.md](design.md).
