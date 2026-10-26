# Design: Listagem e consulta individual pela API

## Context

Permitir recuperar clientes para consulta e para carregar os fluxos de edição e exclusão com um contrato público verificável. O contrato correspondente está em [specs/consulta-clientes-api/spec.md](specs/consulta-clientes-api/spec.md).

Dependências: [estruturar-clientes-xano](../../estruturar-clientes-xano/proposal.md)

## Goals / Non-Goals

**Goals:** GET /clientes (4100486). GET /clientes/{id_cliente} (4100487), incluindo o erro conhecido de cliente inexistente. Contrato de resposta de cinco campos sem presumir paginação, ordenação ou filtros adicionais.

**Non-Goals:** ampliar o modelo de domínio ou alterar os contratos dos demais fluxos. Manter o comportamento dos recursos existentes.

## Decisions

A lista é um array de objetos, e a consulta individual é um objeto com id_cliente, nome, cpf, telefone e email. Preservar CPF/telefone como texto. Para confirmar ausência no frontend usa-se o envelope conhecido, não apenas o status HTTP.

Um contrato comum de cinco campos permite que consultas alimentem os fluxos de edição e exclusão.

### Código e contratos

- [xano/api/clientes/clientes_GET.xs](../../../../xano/api/clientes/clientes_GET.xs)
- [xano/api/clientes/clientes/id_cliente_GET.xs](../../../../xano/api/clientes/clientes/id_cliente_GET.xs)
- [docs/api-clientes.md](../../../../docs/api-clientes.md)

## Verification

As definições publicadas dos dois GETs foram conferidas anteriormente por metadados. O cenário integrado registrou lista 200, cliente existente 200 e ausência posterior 404. O GET anterior de ID inexistente confirmou code ERROR_CODE_NOT_FOUND e message Cliente não encontrado.; o campo adicional payload não tem valor presumido.

Fontes de testes e resultados:

- docs/validacao-mvp-clientes.md — etapas 1, 3, 5 e 6
- frontend/tests/test_exclusao_clientes.py::ClienteHttpTests.test_get_de_confirmacao_reconhece_404_do_cliente (simulado)



## Risks / Trade-offs

O arquivo local da listagem e a definição publicada usam formas diferentes da expressão de mapeamento (inline e bloco); não se declara identidade textual. O funcionamento da listagem foi exercitado, mas não se acrescentam garantias de paginação ou ordenação.

## Histórico e fontes

| Registro | Evidência |
| --- | --- |
| Implementação | O consumidor GET de listagem já aparece no frontend em 18/10/2026 (`b153306`). As APIs de listagem e consulta individual constam concluídas nas tarefas 2.2/2.3 em 25/10/2026 (`6cec2f6`); seus XanoScripts foram adicionados ao Git em 26/10/2026 (`c66fb69`). A data inicial de criação dessas APIs no Xano permanece indeterminada. |
| Documentação | Consumo da lista descrito no README de 18/10/2026; tarefas 2.2/2.3 no registro de 25/10/2026; contrato por metadados e registro formal do escopo em 26/10/2026. |
| Validação | As tarefas 2.2/2.3 já eram declaradas concluídas em 25/10/2026, sem data individual dos testes originais. A conferência dos contratos é datada de 26/10/2026 em docs/api-clientes.md; os GETs de lista, cliente existente e ausência posterior do descartável estão registrados no cenário integrado de 26/10/2026. Não há data individual adicional para cada leitura do envelope de erro. |
| Datas indeterminadas | Dia exato de criação das duas APIs e dos testes originais de listagem/consulta. |

- `git show b153306:frontend/clientes_api.py` — listar_clientes
- `git show 6cec2f6:openspec/changes/mvp-assistencia-tecnica/tasks.md` — 2.2/2.3 concluídas
- `git show c66fb69:xano/api/clientes/clientes_GET.xs` e `git show c66fb69:xano/api/clientes/clientes/id_cliente_GET.xs`
- [docs/api-clientes.md](../../../../docs/api-clientes.md) e [validação do MVP](../../../../docs/validacao-mvp-clientes.md)

Rastreabilidade: tarefas **2.2 e 2.3; parcela de 2.6 relativa aos GETs** de [mvp-assistencia-tecnica](../../mvp-assistencia-tecnica/tasks.md). A cronologia comum e o significado das datas estão em [histórico técnico](../../../../docs/historico-clientes.md).
