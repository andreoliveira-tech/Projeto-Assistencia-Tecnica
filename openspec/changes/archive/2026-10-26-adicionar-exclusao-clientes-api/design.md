# Design: Exclusão de clientes pela API com bloqueio de vínculos

## Context

Disponibilizar exclusão de cliente sem equipamentos, preservando os relacionamentos e recusando exclusão quando a verificação de dependências não for segura. O contrato correspondente está em [specs/exclusao-clientes-api/spec.md](specs/exclusao-clientes-api/spec.md).

Dependências: [estruturar-clientes-xano](../../estruturar-clientes-xano/proposal.md), [adicionar-consulta-clientes-api](../2026-10-26-adicionar-consulta-clientes-api/proposal.md), [garantir-integridade-cliente-equipamento](../../garantir-integridade-cliente-equipamento/proposal.md)

## Goals / Non-Goals

**Goals:** DELETE /clientes/{id_cliente} (4107955), identificador positivo sem corpo. Verificações de existência e dependências antes da única exclusão. Resposta id_cliente/excluido, bloqueio por equipamentos e interrupção em falha de consulta.

**Non-Goals:** ampliar o modelo de domínio ou alterar os contratos dos demais fluxos. Não realizar exclusão em cascata nem prometer integridade concorrente.

## Decisions

Consultar clientes/consultar_dependencias; conferir retorno e identificador e exigir bloqueia_exclusao=false e possui_equipamentos=false antes de db.del cliente. Não remover equipamentos nem fazer cascata. Reutilizar o endpoint publicado, sem recriá-lo nem publicar recursos.

Uma falha ao consultar vínculos precisa interromper a operação: um resultado desconhecido não equivale a ausência de dependências.

### Código e contratos

- [docs/api-clientes.md](../../../../docs/api-clientes.md)
- [openspec/changes/mvp-assistencia-tecnica/design.md](../../mvp-assistencia-tecnica/design.md)
- [frontend/clientes_api.py](../../../../frontend/clientes_api.py)

## Verification

A definição publicada foi inspecionada anteriormente com include_draft=false e include_xanoscript=true; o DELETE não possui arquivo XanoScript local. A 2.5 registra testes reais de bloqueio com equipamento (400), inexistente (404) e exclusão sem vínculo (200). A falha de dependências foi verificada por inspeção e simulação Python, não por falha integrada no Xano. O cenário posterior da interface excluiu somente o descartável 13.

Fontes de testes e resultados:

- openspec/changes/mvp-assistencia-tecnica/design.md — Evidências da tarefa 2.5
- docs/validacao-mvp-clientes.md — DELETE único e GET posterior do cliente descartável



## Risks / Trade-offs

A garantia é sequencial, sem proteção completa a concorrência. A ausência do arquivo local DELETE limita a reprodução a partir do repositório; a fonte é a definição publicada registrada em docs/api-clientes.md. Indisponibilidade de vínculos não foi provocada em teste integrado.

## Histórico e fontes

| Registro | Evidência |
| --- | --- |
| Implementação | A versão publicada do DELETE é datada de `2026-10-26 04:30:46+0000` (26/10/2026 às 01:30:46 em UTC−03), conforme o design original já contido em c66fb69. A tarefa 2.5 estava aberta no registro de 25/10/2026 e concluída no de 26/10/2026. Está comprovada a versão publicada de 26/10, sem inferir o instante inicial de codificação ou de criação do recurso. |
| Documentação | Requisito e tarefa ainda pendente registrados em 25/10/2026; versão publicada e resultados consolidados no design original em 26/10/2026; contrato da API e registro formal do escopo em 26/10/2026. |
| Validação | Os três testes integrados da 2.5 (bloqueio, inexistência e exclusão permitida) estão explicitamente registrados em 26/10/2026 e presentes em c66fb69. A validação posterior pela interface com o descartável 13 também está registrada em 26/10/2026, em etapa distinta. A simulação de falha de consulta não é convertida em teste integrado. |
| Datas indeterminadas | Instante exato do início da codificação/criação do endpoint. A versão publicada e a data dos registros de validação são conhecidas. |

- `git show 6cec2f6:openspec/changes/mvp-assistencia-tecnica/tasks.md` — 2.5 aberta
- `git show c66fb69:openspec/changes/mvp-assistencia-tecnica/design.md` — endpoint 4107955, versão e testes da 2.5
- [docs/validacao-mvp-clientes.md](../../../../docs/validacao-mvp-clientes.md) — cenário posterior do descartável

Rastreabilidade: tarefas **2.5; parcela de 2.6 relativa ao DELETE** de [mvp-assistencia-tecnica](../../mvp-assistencia-tecnica/tasks.md). A cronologia comum e o significado das datas estão em [histórico técnico](../../../../docs/historico-clientes.md).
