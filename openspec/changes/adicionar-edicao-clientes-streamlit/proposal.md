# Proposal: Edição e confirmação de atualização no Streamlit

## Why

Permitir editar um cliente previamente carregado e confirmar os dados por nova consulta, distinguindo atualização rejeitada de resultado incerto.

## What Changes

- GET para carregar edição e PUT por ação Salvar alterações.
- GET posterior e comparação dos cinco campos para confirmar sucesso.
- Bloqueio de reenvio em incerteza e conferência manual por GET.

## Capabilities

### New Capabilities

- `edicao-clientes-ui`: edição e confirmação de atualização no streamlit.

### Modified Capabilities

Nenhuma.

## Impact

- Código e contratos: [frontend/app.py](../../../frontend/app.py), [frontend/clientes_api.py](../../../frontend/clientes_api.py), [frontend/README.md](../../../frontend/README.md).
- Dependências: [adicionar-atualizacao-clientes-api](../archive/2026-10-26-adicionar-atualizacao-clientes-api/proposal.md), [adicionar-cadastro-clientes-streamlit](../archive/2026-10-26-adicionar-cadastro-clientes-streamlit/proposal.md), [adicionar-consulta-clientes-streamlit](../archive/2026-10-26-adicionar-consulta-clientes-streamlit/proposal.md)
- Compatibilidade: manter os contratos de Cliente e a arquitetura Xano/Streamlit existentes.
- Fora do escopo: novas entidades, autenticação de usuários e gerenciamento de equipamentos além da integridade do vínculo.

## Verification

A tarefa 3.4 já constava concluída na Change original; o registro atual verificou código e regressão local, sem novo PUT real. Os testes simulados cobrem resposta divergente, 408, falhas de comunicação, inexistência, campos vazios e bloqueio do botão até conferência.

Os critérios e as fontes de verificação estão em [tasks.md](tasks.md) e [design.md](design.md).
