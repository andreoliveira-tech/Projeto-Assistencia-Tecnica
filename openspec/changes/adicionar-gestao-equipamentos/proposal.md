# Proposal: Gestão de equipamentos

## Why

A tabela de equipamentos já existe para proteger a exclusão de clientes, mas não há APIs públicas nem interface para gerenciá-la. O módulo deve permitir CRUD sem duplicar essa estrutura ou ampliar o modelo de domínio.

## What Changes

- Reutilizar `equipamento` (908125) e `equipamentos/validar_cliente` (355571), conferidos por metadados em `149143/v1`.
- Preparar cinco endpoints de CRUD e implementar cliente HTTP e interface Streamlit com os seis atributos documentados.
- Bloquear exclusão quando houver OS e interromper a exclusão se não for possível verificar dependências, sem cascata.
- Testar localmente com HTTP simulado, preservando o módulo de clientes.

## Capabilities

### New Capabilities

- `gestao-equipamentos`: cadastro, listagem, consulta, atualização e exclusão segura de equipamentos.

### Modified Capabilities

Nenhuma. A estrutura e integridade previstas em `garantir-integridade-cliente-equipamento` permanecem como dependência.

## Impact

- Frontend: módulo Streamlit separado, cliente HTTP, configuração externa e testes locais.
- Backend: definições XanoScript locais para um grupo Equipamentos e CRUD, reutilizando tabela e função existentes.
- Dependências: [integridade do vínculo](../garantir-integridade-cliente-equipamento/design.md) e contrato de Clientes existente.
- A verificação de OS depende de estrutura ainda ausente no inventário. As definições correspondentes são preparatórias, sem publicação ou garantia funcional remota.
- Fora do escopo: Técnicos, implementação de OS/Serviços, filtros adicionais, novas entidades ou atributos, alteração de recursos do Xano e testes reais de escrita.
