# Tasks

## 1. Cadastro e validação compartilhada

- [x] 1.1 Disponibilizar POST `/clientes` com nome, CPF, telefone e e-mail obrigatórios e retorno dos cinco campos do cliente. Critério: contrato do endpoint 4099966 e `xano/api/clientes/clientes_POST.xs`.
- [x] 1.2 Aplicar a validação compartilhada antes de criar ou atualizar registros. Critério: chamadas anteriores a `db.add`/`db.edit` nas definições documentadas e regras presentes em `xano/function/clientes/validar_dados.xs`; o interior publicado da função não foi conferido nesta inspeção.
- [x] 1.3 Verificar cadastro válido consultável. Evidência: POST 200 e GET do descartável 13 registrados em `docs/validacao-mvp-clientes.md`.

## 2. Validação de rejeições e normalização

- [ ] 2.1 Comprovar no backend a rejeição integral de dados inválidos sem criar ou alterar registros e a normalização completa em POST/PUT, correspondente à tarefa original 1.3. Critério: respostas de rejeição e consultas antes/depois para conferir persistência, conforme [plano de validação](../../../docs/plano-validacao-backend-clientes.md). O lote de 50 requisições não foi executado e exige autorização específica; não faz parte desta refatoração documental.

## Evidências

As marcações se baseiam na implementação e nas verificações registradas em [design.md](design.md#verification), com rastreabilidade às tarefas **2.1 e 1.3** de [mvp-assistencia-tecnica](../mvp-assistencia-tecnica/tasks.md).

Datas comprovadas e limites estão no [histórico do design](design.md#histórico-e-fontes). Este checklist não registra novas execuções.
