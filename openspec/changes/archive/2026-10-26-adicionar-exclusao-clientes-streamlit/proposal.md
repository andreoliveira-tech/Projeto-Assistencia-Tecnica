# Proposal: Exclusão confirmada e tratamento de falhas no Streamlit

## Why

Concluir o fluxo de exclusão com confirmação explícita e preservar informação confiável diante de bloqueios, respostas ambíguas e falhas de comunicação nos fluxos do frontend.

## What Changes

- Carregamento e confirmação explícita antes de DELETE único.
- Validação do retorno e GET estrito de ausência, sem reenvio automático.
- Invalidação dos estados pertinentes e tratamento transversal de falhas.
- Rastreabilidade do contrato documentado dos cinco endpoints.

## Capabilities

### New Capabilities

- `exclusao-falhas-clientes-ui`: exclusão confirmada e tratamento de falhas no streamlit.

### Modified Capabilities

Nenhuma.

## Impact

- Código e contratos: [frontend/app.py](../../../../frontend/app.py), [frontend/clientes_api.py](../../../../frontend/clientes_api.py), [frontend/tests/test_exclusao_clientes.py](../../../../frontend/tests/test_exclusao_clientes.py), [frontend/tests/test_fluxos_clientes.py](../../../../frontend/tests/test_fluxos_clientes.py), [frontend/verificar_integracao_clientes.py](../../../../frontend/verificar_integracao_clientes.py), [frontend/README.md](../../../../frontend/README.md), [docs/api-clientes.md](../../../../docs/api-clientes.md), [docs/validacao-mvp-clientes.md](../../../../docs/validacao-mvp-clientes.md).
- Dependências: [adicionar-consulta-clientes-api](../2026-10-26-adicionar-consulta-clientes-api/proposal.md), [adicionar-exclusao-clientes-api](../2026-10-26-adicionar-exclusao-clientes-api/proposal.md), [adicionar-cadastro-clientes-streamlit](../2026-10-26-adicionar-cadastro-clientes-streamlit/proposal.md), [adicionar-consulta-clientes-streamlit](../2026-10-26-adicionar-consulta-clientes-streamlit/proposal.md), [adicionar-edicao-clientes-streamlit](../../adicionar-edicao-clientes-streamlit/proposal.md)
- Compatibilidade: manter os contratos de Cliente e a arquitetura Xano/Streamlit existentes.
- Fora do escopo: novas entidades, autenticação de usuários e gerenciamento de equipamentos além da integridade do vínculo.

## Verification

A suíte já executada aprovou 49 testes: 31 em test_exclusao_clientes.py e 18 em test_fluxos_clientes.py. O cenário integrado anterior via AppTest executou quatro GETs, um POST e um DELETE somente do descartável 13; sete clientes preexistentes permaneceram iguais nos campos retornados. O bloqueio na UI foi simulado e o backend já possuía evidência integrada da 2.5. Não foram executados novos testes nesta revisão documental.

Os critérios e as fontes de verificação estão em [tasks.md](tasks.md) e [design.md](design.md).
