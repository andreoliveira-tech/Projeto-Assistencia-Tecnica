# Proposal: Listagem e consulta individual no Streamlit

## Why

Exibir clientes e permitir consulta por identificador sem disparar chamadas em reruns e sem conservar um resultado anterior como se fosse a consulta atual.

## What Changes

- Listagem sob ação Atualizar lista.
- Consulta individual por inteiro positivo e mensagem de cliente inexistente.
- Estados independentes e descarte de resultados anteriores em falhas ou troca da URL.

## Capabilities

### New Capabilities

- `consulta-clientes-ui`: listagem e consulta individual no streamlit.

### Modified Capabilities

Nenhuma.

## Impact

- Código e contratos: [frontend/app.py](../../../../frontend/app.py), [frontend/clientes_api.py](../../../../frontend/clientes_api.py), [frontend/README.md](../../../../frontend/README.md).
- Dependências: [adicionar-consulta-clientes-api](../2026-10-26-adicionar-consulta-clientes-api/proposal.md), [adicionar-cadastro-clientes-streamlit](../2026-10-26-adicionar-cadastro-clientes-streamlit/proposal.md)
- Compatibilidade: manter os contratos de Cliente e a arquitetura Xano/Streamlit existentes.
- Fora do escopo: novas entidades, autenticação de usuários e gerenciamento de equipamentos além da integridade do vínculo.

## Verification

Os testes locais exercitam lista vazia, falhas, consulta inválida/inexistente e regressão dos fluxos. O cenário integrado existente consultou lista inicial/final e carregou o cliente descartável, com resultados 200; o GET posterior retornou o 404 conhecido. O erro 404 genérico da consulta comum é distinto do modo estrito de confirmação de exclusão.

Os critérios e as fontes de verificação estão em [tasks.md](tasks.md) e [design.md](design.md).
