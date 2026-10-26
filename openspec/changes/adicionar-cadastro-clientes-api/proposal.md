# Proposal: Cadastro e validação compartilhada no backend

## Why

Disponibilizar cadastro de clientes pela API e centralizar as regras de dados usadas também na atualização, mantendo explícita a verificação integrada ainda pendente.

## What Changes

- POST /clientes (4099966), quatro campos obrigatórios e retorno do cliente.
- Validação e normalização compartilhadas antes de criar ou atualizar.

## Capabilities

### New Capabilities

- `cadastro-validacao-clientes-api`: cadastro e validação compartilhada no backend.

### Modified Capabilities

Nenhuma.

## Impact

- Código e contratos: [xano/api/clientes/clientes_POST.xs](../../../xano/api/clientes/clientes_POST.xs), [xano/function/clientes/validar_dados.xs](../../../xano/function/clientes/validar_dados.xs), [xano/api/clientes/clientes/id_cliente_PUT.xs](../../../xano/api/clientes/clientes/id_cliente_PUT.xs), [docs/api-clientes.md](../../../docs/api-clientes.md), [docs/plano-validacao-backend-clientes.md](../../../docs/plano-validacao-backend-clientes.md).
- Dependências: [estruturar-clientes-xano](../estruturar-clientes-xano/proposal.md)
- Compatibilidade: manter os contratos de Cliente e a arquitetura Xano/Streamlit existentes.
- Fora do escopo: novas entidades, autenticação de usuários e gerenciamento de equipamentos além da integridade do vínculo.

## Verification

A definição remota publicada registrada na documentação confirma a chamada de clientes/validar_dados antes de db.add e db.edit, sem revelar a implementação interna atual dessa função. O código local contém validação de CPF, telefone, nome e e-mail. POST válido retornou 200 e o GET conferiu o cliente 13 no cenário integrado anterior. A bateria de casos inválidos e a normalização completa no runtime Xano não foram comprovadas.

A validação integrada de rejeições e normalização em POST/PUT permanece pendente em [tasks.md](tasks.md).
