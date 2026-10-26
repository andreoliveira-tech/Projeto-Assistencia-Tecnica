# Tasks

## 1. Confirmação de exclusão e recuperação de falhas

- [x] 1.1 Exigir GET de carregamento e confirmação explícita antes de um único DELETE, invalidando a confirmação ao trocar cliente ou URL. Critério: testes de cancelamento, reruns e troca de contexto em `test_exclusao_clientes.py`.
- [x] 1.2 Validar DELETE 200 e confirmar ausência somente pelo GET 404 com JSON, código e mensagem conhecidos; tratar 408 e respostas ambíguas como incerteza. Critério: testes de 404 válido/ambíguo/JSON inválido, 408 e invalidação dos estados relacionados.
- [x] 1.3 Verificar o fluxo de exclusão sem atingir clientes preexistentes. Evidência: cenário integrado do descartável 13 e preservação do baseline documentados em `docs/validacao-mvp-clientes.md`.
- [x] 1.4 Tratar falhas dos demais fluxos e documentar o consumo dos cinco endpoints. Critério: testes em `test_fluxos_clientes.py`, contrato em `docs/api-clientes.md` e README do frontend; total global registrado de 49 testes, sem duplicação de contagem.

## Evidências

As marcações se baseiam na implementação e nas verificações registradas em [design.md](design.md#verification), com rastreabilidade às tarefas **3.5 e 3.6; consolidação da rastreabilidade da 2.6** de [mvp-assistencia-tecnica](../../mvp-assistencia-tecnica/tasks.md).

Datas comprovadas e limites estão no [histórico do design](design.md#histórico-e-fontes). Este checklist não registra novas execuções.
