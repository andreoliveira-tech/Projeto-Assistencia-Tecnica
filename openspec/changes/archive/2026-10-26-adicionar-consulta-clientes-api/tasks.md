# Tasks

## 1. Listagem e consulta individual

- [x] 1.1 Disponibilizar GET `/clientes` e GET `/clientes/{id_cliente}` com os cinco campos públicos. Critério: definições dos endpoints 4100486/4100487 e XanoScripts locais correspondentes.
- [x] 1.2 Verificar retorno da lista e de cliente existente. Evidência: GETs 200 registrados em `docs/validacao-mvp-clientes.md` e conclusão histórica das tarefas 2.2/2.3.
- [x] 1.3 Documentar o erro conhecido de cliente inexistente. Critério: HTTP 404 com `code: ERROR_CODE_NOT_FOUND` e `message: Cliente não encontrado.` observado no GET, conforme `docs/api-clientes.md`, sem presumir o valor de `payload`.

## Evidências

As marcações se baseiam na implementação e nas verificações registradas em [design.md](design.md#verification), com rastreabilidade às tarefas **2.2 e 2.3; parcela de 2.6 relativa aos GETs** de [mvp-assistencia-tecnica](../../mvp-assistencia-tecnica/tasks.md).

Datas comprovadas e limites estão no [histórico do design](design.md#histórico-e-fontes). Este checklist não registra novas execuções.
