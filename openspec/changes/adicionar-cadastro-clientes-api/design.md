# Design: Cadastro e validação compartilhada no backend

## Context

Disponibilizar cadastro de clientes pela API e centralizar as regras de dados usadas também na atualização, mantendo explícita a verificação integrada ainda pendente. O contrato correspondente está em [specs/cadastro-validacao-clientes-api/spec.md](specs/cadastro-validacao-clientes-api/spec.md).

Dependências: [estruturar-clientes-xano](../estruturar-clientes-xano/proposal.md)

## Goals / Non-Goals

**Goals:** POST /clientes (4099966), quatro campos obrigatórios e retorno do cliente. Validação e normalização compartilhadas antes de criar ou atualizar.

**Non-Goals:** ampliar o modelo de domínio ou alterar os contratos dos demais fluxos. Manter o comportamento dos recursos existentes.

## Decisions

Reutilizar clientes/validar_dados para POST e PUT antes da escrita. Campos nome/cpf/telefone são textuais; email é entrada do tipo e-mail. A função local normaliza máscaras de CPF/telefone e calcula os verificadores do CPF. Não há evidência de equivalência integral entre a função local e sua implementação publicada.

Um validador compartilhado evita divergência de regras entre cadastro e atualização.

### Código e contratos

- [xano/api/clientes/clientes_POST.xs](../../../xano/api/clientes/clientes_POST.xs)
- [xano/function/clientes/validar_dados.xs](../../../xano/function/clientes/validar_dados.xs)
- [xano/api/clientes/clientes/id_cliente_PUT.xs](../../../xano/api/clientes/clientes/id_cliente_PUT.xs)
- [docs/api-clientes.md](../../../docs/api-clientes.md)
- [docs/plano-validacao-backend-clientes.md](../../../docs/plano-validacao-backend-clientes.md)

## Verification

A definição remota publicada registrada na documentação confirma a chamada de clientes/validar_dados antes de db.add e db.edit, sem revelar a implementação interna atual dessa função. O código local contém validação de CPF, telefone, nome e e-mail. POST válido retornou 200 e o GET conferiu o cliente 13 no cenário integrado anterior. A bateria de casos inválidos e a normalização completa no runtime Xano não foram comprovadas.

Fontes de testes e resultados:

- docs/validacao-mvp-clientes.md — POST válido e GET do cliente descartável
- frontend/tests/test_fluxos_clientes.py::FalhasHttpTests.test_cadastro_rejeicoes_comunicacao_e_respostas_invalidas (simulado; não valida o backend)
- docs/plano-validacao-backend-clientes.md — plano de 50 operações NÃO executado

A comprovação integrada da rejeição sem persistência e da normalização permanece aberta em [tasks.md](tasks.md), correspondente à tarefa original 1.3.

## Risks / Trade-offs

Chamada de validador nos metadados e teste HTTP simulado não demonstram rejeição real sem alterações. O lote de 50 requisições está expressamente proibido nesta etapa; nenhum status HTTP genérico de validação é inferido de error_type.

## Histórico e fontes

| Registro | Evidência |
| --- | --- |
| Implementação | A integração Python de POST já aparece em 18/10/2026 (`b153306`). O cadastro do backend consta concluído na tarefa 2.1 do registro de 25/10/2026 (`6cec2f6`). POST e função local de validação foram versionados em 26/10/2026 (`c66fb69`). Nenhum desses marcos estabelece o dia exato de criação ou publicação inicial do backend. |
| Documentação | README do cadastro em 18/10/2026; tarefa 2.1 documentada em 25/10/2026; contrato da API e registro formal do escopo em 26/10/2026. A documentação de 18/10 não comprova execução integrada naquela data. |
| Validação | A tarefa 2.1 já era declarada concluída em 25/10/2026, sem data individual do teste original. Cadastro válido pelo Streamlit e GET posterior estão registrados em 26/10/2026. A verificação integral de rejeição/normalização da 1.3 segue pendente, sem data de execução. |
| Datas indeterminadas | Datas exatas de implementação do POST remoto, do validador publicado e da execução original da 2.1; validação completa da 1.3 ainda não realizada. |

- `git show b153306:frontend/clientes_api.py` — cadastrar_cliente com POST
- `git show 6cec2f6:openspec/changes/mvp-assistencia-tecnica/tasks.md` — 2.1 concluída e 1.3 aberta
- `git show c66fb69:xano/function/clientes/validar_dados.xs` — captura local do validador
- [docs/api-clientes.md](../../../docs/api-clientes.md) e [validação do MVP](../../../docs/validacao-mvp-clientes.md) — conferência e cenário de 26/10/2026

Rastreabilidade: tarefas **2.1 e 1.3** de [mvp-assistencia-tecnica](../mvp-assistencia-tecnica/tasks.md). A cronologia comum e o significado das datas estão em [histórico técnico](../../../docs/historico-clientes.md).
