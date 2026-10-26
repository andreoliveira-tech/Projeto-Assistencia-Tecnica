# Proposal: Configuração e cadastro na interface Streamlit

## Why

Permitir operar o cadastro pelo Streamlit com configuração externa do grupo de APIs e confirmação de resposta compatível, sem incluir segredos no código.

## What Changes

- Aplicação Streamlit/Python e XANO_CLIENTES_API_BASE_URL.
- Formulário de cadastro com quatro campos e envio por ação explícita.
- Erros de configuração e de cadastro sem falsa confirmação.

## Capabilities

### New Capabilities

- `configuracao-cadastro-clientes-ui`: configuração e cadastro na interface streamlit.

### Modified Capabilities

Nenhuma.

## Impact

- Código e contratos: [frontend/config.py](../../../../frontend/config.py), [frontend/app.py](../../../../frontend/app.py), [frontend/clientes_api.py](../../../../frontend/clientes_api.py), [frontend/requirements.txt](../../../../frontend/requirements.txt), [frontend/README.md](../../../../frontend/README.md), [docs/api-clientes.md](../../../../docs/api-clientes.md).
- Dependências: [adicionar-cadastro-clientes-api](../../adicionar-cadastro-clientes-api/proposal.md), [adicionar-consulta-clientes-api](../2026-10-26-adicionar-consulta-clientes-api/proposal.md)
- Compatibilidade: manter os contratos de Cliente e a arquitetura Xano/Streamlit existentes.
- Fora do escopo: novas entidades, autenticação de usuários e gerenciamento de equipamentos além da integridade do vínculo.

## Verification

O cenário integrado já documentado iniciou a aplicação real por AppTest, consultou a lista e criou o descartável 13 pelo formulário, conferido por GET. Os 49 testes locais existentes incluem configuração ausente/inválida, cadastro sem campos, rejeições e resultados incertos. A ligação da URL ao workspace 149143, grupo 436987 e v1 live foi confirmada anteriormente por metadados.

Os critérios e as fontes de verificação estão em [tasks.md](tasks.md) e [design.md](design.md).
