# Tasks

## 1. Atualização de cliente existente

- [x] 1.1 Disponibilizar PUT `/clientes/{id_cliente}` com quatro campos obrigatórios, confirmação de existência e preservação do identificador. Critério: endpoint 4100488, XanoScript local e contrato em `docs/api-clientes.md`.
- [x] 1.2 Reutilizar o validador de dados antes de `db.edit`. Critério: chamada compartilhada na definição; comprovação integral de rejeições controlada em `adicionar-cadastro-clientes-api`, sem duplicar a pendência original 1.3.
- [x] 1.3 Verificar atualização válida e integração Python. Evidência: conclusão histórica da 2.4 e regressões locais citadas no design; a rodada documentada de 49 testes não executou novo PUT real.

## Evidências

As marcações se baseiam na implementação e nas verificações registradas em [design.md](design.md#verification), com rastreabilidade às tarefas **2.4; parcela de 2.6 relativa ao PUT** de [mvp-assistencia-tecnica](../../mvp-assistencia-tecnica/tasks.md).

Datas comprovadas e limites estão no [histórico do design](design.md#histórico-e-fontes). Este checklist não registra novas execuções.
