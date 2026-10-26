# Tasks

## 1. Vínculo obrigatório e integridade sequencial

- [x] 1.1 Definir obrigatoriedade, nulabilidade e garantia sequencial do vínculo Cliente–Equipamento. Critério: decisões aprovadas da tarefa original 1.4, com limitação concorrente explícita no design.
- [x] 1.2 Manter `equipamento` com identificador nativo, campos descritivos e `id_cliente` obrigatório não nulo com índice não exclusivo. Critério: `xano/table/equipamento.xs` e correspondência com o domínio.
- [x] 1.3 Verificar cardinalidade 1:N e rejeição de vínculos ausentes, nulos ou inexistentes antes da persistência. Evidência: inspeção e cenários sequenciais da tarefa 1.6 registrados no design original.

## Evidências

As marcações se baseiam na implementação e nas verificações registradas em [design.md](design.md#verification), com rastreabilidade às tarefas **1.4, 1.5 e 1.6** de [mvp-assistencia-tecnica](../mvp-assistencia-tecnica/tasks.md).

Datas comprovadas e limites estão no [histórico do design](design.md#histórico-e-fontes). Este checklist não registra novas execuções.
