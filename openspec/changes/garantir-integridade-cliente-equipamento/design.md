# Design: Estrutura mínima e integridade sequencial de equipamentos

## Context

Preparar o vínculo Cliente 1:N Equipamento necessário ao bloqueio de exclusão, sem antecipar gerenciamento de equipamentos. O contrato correspondente está em [specs/integridade-cliente-equipamento/spec.md](specs/integridade-cliente-equipamento/spec.md).

Dependências: [estruturar-clientes-xano](../estruturar-clientes-xano/proposal.md)

## Goals / Non-Goals

**Goals:** Tabela equipamento e nulabilidade aprovada dos campos. Referência obrigatória id_cliente e índice não exclusivo. Validação de cliente existente e consulta de dependências com garantia delimitada a operações sequenciais.

**Non-Goals:** ampliar o modelo de domínio ou alterar os contratos dos demais fluxos. Não criar APIs ou interface de gerenciamento de equipamentos.

## Decisions

Usar equipamento.id como id_equipamento conceitual; tipo textual obrigatório não nulo; marca, modelo e numero_serie textuais opcionais e anuláveis; id_cliente inteiro obrigatório não nulo referenciando cliente.id com índice não exclusivo. A referência declarada não substitui a verificação de existência antes de persistir.

O índice não exclusivo representa a cardinalidade 1:N; as verificações de existência complementam a referência declarada.

### Código e contratos

- [xano/table/equipamento.xs](../../../xano/table/equipamento.xs)
- [docs/domain-model.md](../../../docs/domain-model.md)
- [openspec/changes/mvp-assistencia-tecnica/design.md](../../../openspec/changes/mvp-assistencia-tecnica/design.md)

## Verification

O design original registra inspeção das funções publicadas equipamentos/validar_cliente e clientes/consultar_dependencias na tarefa 1.6, além de cenários sequenciais de vínculos ausentes, nulos, inexistentes e válidos. A tabela local confirma campos e índice. Nenhuma função foi consultada novamente nesta revisão documental. A inspeção de endpoints da 2.6 não reinspecionou o interior das auxiliares.

Fontes de testes e resultados:

- openspec/changes/mvp-assistencia-tecnica/design.md — Evidências da tarefa 1.6
- openspec/changes/mvp-assistencia-tecnica/specs/cadastro-clientes/spec.md — estrutura e relacionamento



## Risks / Trade-offs

Verificações prévias não eliminam corridas entre vínculo e exclusão; a limitação concorrente foi aceita. As auxiliares constam de evidência remota histórica no design, mas não têm arquivos locais próprios neste repositório. Não há API nem interface de equipamentos.

## Histórico e fontes

| Registro | Evidência |
| --- | --- |
| Implementação | A estrutura de equipamento já consta concluída na tarefa 1.5 em 25/10/2026 (`6cec2f6`). A conclusão das decisões sequenciais e das verificações 1.4/1.6 aparece em 26/10/2026 (`c66fb69`). O design original registra a versão publicada de clientes/consultar_dependencias como `2026-10-26 03:22:11+0000` e do procedimento de investigação como `2026-10-26 03:27:53+0000`; ambas correspondem a 26/10 também em UTC−03. Esses horários datam versões publicadas registradas, não o início da codificação. |
| Documentação | Decisões de campos e preparação estrutural já registradas em 25/10/2026; consolidação da garantia sequencial e evidências da 1.6 em 26/10/2026 no design original; registro formal do escopo em 26/10/2026. |
| Validação | A seção Evidências da tarefa 1.6 é explicitamente datada de 26/10/2026 e já está no commit c66fb69. Ela registra inspeção e cenários sequenciais. A data da preparação inicial da tabela, anterior ao registro de conclusão em 25/10, não é determinada. |
| Datas indeterminadas | Dia exato de criação inicial da tabela e início da implementação das funções; não há garantia concorrente datada ou comprovada. |

- `git show 6cec2f6:openspec/changes/mvp-assistencia-tecnica/tasks.md` — 1.5 concluída; 1.4/1.6 ainda abertas
- `git show c66fb69:openspec/changes/mvp-assistencia-tecnica/design.md` — versões e evidências da 1.6
- [Design original, evidências da 1.6](../mvp-assistencia-tecnica/design.md)

Rastreabilidade: tarefas **1.4, 1.5 e 1.6** de [mvp-assistencia-tecnica](../mvp-assistencia-tecnica/tasks.md). A cronologia comum e o significado das datas estão em [histórico técnico](../../../docs/historico-clientes.md).
