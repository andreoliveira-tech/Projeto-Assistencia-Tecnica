# Tasks

## 1. Exclusão com proteção de vínculos

- [x] 1.1 Disponibilizar DELETE `/clientes/{id_cliente}` com identificador positivo, existência e consulta de dependências antes da única exclusão. Critério: definição publicada do endpoint 4107955 registrada em `docs/api-clientes.md`.
- [x] 1.2 Bloquear vínculos e interromper exclusão quando a verificação falhar, sem cascata. Evidência: bloqueio e inexistência testados na 2.5; falha de consulta verificada por inspeção e simulação, conforme o design original.
- [x] 1.3 Verificar exclusão permitida e ausência posterior. Evidência: cenário da 2.5 e cenário posterior do descartável 13 registrados, mantendo separados os testes do backend e da interface.

## Evidências

As marcações se baseiam na implementação e nas verificações registradas em [design.md](design.md#verification), com rastreabilidade às tarefas **2.5; parcela de 2.6 relativa ao DELETE** de [mvp-assistencia-tecnica](../../mvp-assistencia-tecnica/tasks.md).

Datas comprovadas e limites estão no [histórico do design](design.md#histórico-e-fontes). Este checklist não registra novas execuções.
