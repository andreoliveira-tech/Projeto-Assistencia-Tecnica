# Proposal: Estrutura mínima e integridade sequencial de equipamentos

## Why

Preparar o vínculo Cliente 1:N Equipamento necessário ao bloqueio de exclusão, sem antecipar gerenciamento de equipamentos.

## What Changes

- Tabela equipamento e nulabilidade aprovada dos campos.
- Referência obrigatória id_cliente e índice não exclusivo.
- Validação de cliente existente e consulta de dependências com garantia delimitada a operações sequenciais.

## Capabilities

### New Capabilities

- `integridade-cliente-equipamento`: estrutura mínima e integridade sequencial de equipamentos.

### Modified Capabilities

Nenhuma.

## Impact

- Código e contratos: [xano/table/equipamento.xs](../../../xano/table/equipamento.xs), [docs/domain-model.md](../../../docs/domain-model.md), [openspec/changes/mvp-assistencia-tecnica/design.md](../../../openspec/changes/mvp-assistencia-tecnica/design.md).
- Dependências: [estruturar-clientes-xano](../estruturar-clientes-xano/proposal.md)
- Compatibilidade: manter os contratos de Cliente e a arquitetura Xano/Streamlit existentes.
- Fora do escopo: novas entidades, autenticação de usuários e gerenciamento de equipamentos além da integridade do vínculo.

## Verification

O design original registra inspeção das funções publicadas equipamentos/validar_cliente e clientes/consultar_dependencias na tarefa 1.6, além de cenários sequenciais de vínculos ausentes, nulos, inexistentes e válidos. A tabela local confirma campos e índice. Nenhuma função foi consultada novamente nesta revisão documental. A inspeção de endpoints da 2.6 não reinspecionou o interior das auxiliares.

Os critérios e as fontes de verificação estão em [tasks.md](tasks.md) e [design.md](design.md).
