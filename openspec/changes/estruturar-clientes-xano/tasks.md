# Tasks

## 1. Persistência e contrato de identidade

- [x] 1.1 Manter a tabela `cliente` com `id` nativo, nome, CPF, telefone e e-mail, conforme `docs/domain-model.md`. Critério: estrutura descrita em `xano/table/cliente.xs` e conferência registrada nas tarefas originais 1.1/1.2.
- [x] 1.2 Representar `cliente.id` como `id_cliente` nas respostas, sem duplicar identificadores. Critério: mapeamento dos endpoints compatível com `docs/api-clientes.md`.
- [x] 1.3 Verificar geração do identificador e persistência dos quatro campos no cadastro. Evidência: criação e GET do descartável 13 registrados em `docs/validacao-mvp-clientes.md`.

## Evidências

As marcações se baseiam na implementação e nas verificações registradas em [design.md](design.md#verification), com rastreabilidade às tarefas **1.1 e 1.2** de [mvp-assistencia-tecnica](../mvp-assistencia-tecnica/tasks.md).

Datas comprovadas e limites estão no [histórico do design](design.md#histórico-e-fontes). Este checklist não registra novas execuções.
