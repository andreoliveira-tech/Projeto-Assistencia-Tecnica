# Proposal: Persistência e identidade de clientes

## Why

Manter os dados de Cliente no Xano com correspondência explícita entre o modelo conceitual e a identidade física, sem duplicar identificadores.

## What Changes

- Estrutura Cliente com nome, CPF, telefone e e-mail.
- Mapeamento do id gerado pelo Xano para id_cliente nas APIs.

## Capabilities

### New Capabilities

- `persistencia-clientes`: persistência e identidade de clientes.

### Modified Capabilities

Nenhuma.

## Impact

- Código e contratos: [xano/table/cliente.xs](../../../xano/table/cliente.xs), [docs/domain-model.md](../../../docs/domain-model.md), [docs/api-clientes.md](../../../docs/api-clientes.md).
- Dependências: Nenhuma outra Change.
- Compatibilidade: manter os contratos de Cliente e a arquitetura Xano/Streamlit existentes.
- Fora do escopo: novas entidades, autenticação de usuários e gerenciamento de equipamentos além da integridade do vínculo.

## Verification

A estrutura local e a conferência registrada nas tarefas 1.1/1.2 sustentam o modelo. O cenário integrado já documentado criou o cliente descartável 13, recebeu seu identificador gerado e conferiu os quatro campos por GET antes de removê-lo. Não houve nova inspeção remota nesta revisão documental.

Os critérios e as fontes de verificação estão em [tasks.md](tasks.md) e [design.md](design.md).
