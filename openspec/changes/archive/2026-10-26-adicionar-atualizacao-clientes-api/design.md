# Design: Atualização de clientes pela API

## Context

Permitir atualizar os quatro campos de um cliente existente, preservando sua identidade e reutilizando o validador compartilhado. O contrato correspondente está em [specs/atualizacao-clientes-api/spec.md](specs/atualizacao-clientes-api/spec.md).

Dependências: [estruturar-clientes-xano](../../estruturar-clientes-xano/proposal.md), [adicionar-cadastro-clientes-api](../../adicionar-cadastro-clientes-api/proposal.md), [adicionar-consulta-clientes-api](../2026-10-26-adicionar-consulta-clientes-api/proposal.md)

## Goals / Non-Goals

**Goals:** PUT /clientes/{id_cliente} (4100488), com os quatro campos obrigatórios. Consulta de existência, validação compartilhada e retorno dos dados atualizados. Separação entre evidência de atualização válida e a validação completa pendente na Change `adicionar-cadastro-clientes-api`.

**Non-Goals:** ampliar o modelo de domínio ou alterar os contratos dos demais fluxos. Manter o comportamento dos recursos existentes.

## Decisions

Reutilizar PUT completo de nome, cpf, telefone e email e impedir mudança de identidade. A validação compartilhada e sua única pendência de comprovação integral são de responsabilidade da Change `adicionar-cadastro-clientes-api`; não criar um segundo validador.

A verificação de existência antes da escrita distingue cliente ausente de alteração válida, mantendo a identidade.

### Código e contratos

- [xano/api/clientes/clientes/id_cliente_PUT.xs](../../../../xano/api/clientes/clientes/id_cliente_PUT.xs)
- [docs/api-clientes.md](../../../../docs/api-clientes.md)
- [frontend/clientes_api.py](../../../../frontend/clientes_api.py)

## Verification

O PUT local e a definição publicada documentada consultam a existência, chamam clientes/validar_dados e então db.edit. A tarefa original 2.4 já estava concluída com persistência e nova consulta. A rodada documentada de 49 testes verificou a integração Python por simulação e não executou novo PUT real.

Fontes de testes e resultados:

- openspec/changes/mvp-assistencia-tecnica/tasks.md — conclusão anterior da 2.4
- frontend/tests/test_exclusao_clientes.py::InterfaceTests.test_regressao_cadastro_listagem_consulta_e_edicao
- frontend/tests/test_fluxos_clientes.py::FalhasHttpTests.test_atualizacao_separa_rejeicao_e_resultado_incerto

A validação integral do backend é acompanhada em [adicionar-cadastro-clientes-api](../../adicionar-cadastro-clientes-api/tasks.md); a cobertura simulada não substitui esse critério.

## Risks / Trade-offs

A evidência de conclusão é limitada à atualização válida já registrada e ao contrato inspecionado. A validação integral de rejeições em PUT continua pendente na Change `adicionar-cadastro-clientes-api`. Não há controle de versão ou garantia contra sobrescrita por atualizações concorrentes.

## Histórico e fontes

| Registro | Evidência |
| --- | --- |
| Implementação | O PUT do backend já consta concluído na tarefa 2.4 em 25/10/2026 (`6cec2f6`). O arquivo XanoScript de PUT aparece pela primeira vez no Git em 26/10/2026 (`c66fb69`). Essa captura não permite datar a criação inicial do endpoint no Xano. |
| Documentação | Tarefa 2.4 registrada em 25/10/2026; XanoScript capturado em 26/10/2026; contrato da API e registro formal do escopo em 26/10/2026. |
| Validação | O registro de 25/10/2026 declara a 2.4 concluída segundo o critério de persistência e nova consulta, mas não fornece data nem relatório individual daquela execução. A documentação da 2.6 registra inspeção de contrato em 26/10/2026, sem teste funcional de PUT nessa conferência. A suíte local relatada em 26/10/2026 cobre regressões simuladas, sem novo PUT real. |
| Datas indeterminadas | Datas exatas da criação/publicação inicial do PUT e do teste integrado original da tarefa 2.4. |

- `git show 6cec2f6:openspec/changes/mvp-assistencia-tecnica/tasks.md` — 2.4 marcada
- `git show c66fb69:xano/api/clientes/clientes/id_cliente_PUT.xs` — primeira captura local
- [docs/api-clientes.md](../../../../docs/api-clientes.md) — inspeção do PUT sem teste funcional nessa etapa
- [docs/validacao-mvp-clientes.md](../../../../docs/validacao-mvp-clientes.md) — sem novo PUT real

Rastreabilidade: tarefas **2.4; parcela de 2.6 relativa ao PUT** de [mvp-assistencia-tecnica](../../mvp-assistencia-tecnica/tasks.md). A cronologia comum e o significado das datas estão em [histórico técnico](../../../../docs/historico-clientes.md).
