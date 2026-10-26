# Design: Edição e confirmação de atualização no Streamlit

## Context

Permitir editar um cliente previamente carregado e confirmar os dados por nova consulta, distinguindo atualização rejeitada de resultado incerto. O contrato correspondente está em [specs/edicao-clientes-ui/spec.md](specs/edicao-clientes-ui/spec.md).

Dependências: [adicionar-atualizacao-clientes-api](../archive/2026-10-26-adicionar-atualizacao-clientes-api/proposal.md), [adicionar-cadastro-clientes-streamlit](../archive/2026-10-26-adicionar-cadastro-clientes-streamlit/proposal.md), [adicionar-consulta-clientes-streamlit](../archive/2026-10-26-adicionar-consulta-clientes-streamlit/proposal.md)

## Goals / Non-Goals

**Goals:** GET para carregar edição e PUT por ação Salvar alterações. GET posterior e comparação dos cinco campos para confirmar sucesso. Bloqueio de reenvio em incerteza e conferência manual por GET.

**Non-Goals:** ampliar o modelo de domínio ou alterar os contratos dos demais fluxos. Manter o comportamento dos recursos existentes.

## Decisions

Manter o identificador carregado separado do campo de seleção e não editável. Exigir quatro campos e comparar GET posterior com o retorno validado do PUT, já normalizado. Resultado incerto bloqueia Salvar imediatamente via rerun; conferir estado atual faz GET, sem confirmar retroativamente a tentativa.

A consulta posterior reduz falsas confirmações; impedir reenvio após incerteza evita sobrescritas repetidas sem conferência.

### Código e contratos

- [frontend/app.py](../../../frontend/app.py)
- [frontend/clientes_api.py](../../../frontend/clientes_api.py)
- [frontend/README.md](../../../frontend/README.md)

## Verification

A tarefa 3.4 já constava concluída na Change original; o registro atual verificou código e regressão local, sem novo PUT real. Os testes simulados cobrem resposta divergente, 408, falhas de comunicação, inexistência, campos vazios e bloqueio do botão até conferência.

O status histórico da 3.4 é mantido com ressalva: em `c66fb69`, o checkbox está concluído e o README declara validação integrada pendente. As regressões locais são comprovadas; data e comprovação individual do teste integrado da interface não são determinadas por esses registros.

Fontes de testes e resultados:

- frontend/tests/test_exclusao_clientes.py::InterfaceTests.test_regressao_cadastro_listagem_consulta_e_edicao
- frontend/tests/test_fluxos_clientes.py::FalhasHttpTests.test_atualizacao_separa_rejeicao_e_resultado_incerto
- frontend/tests/test_fluxos_clientes.py::FalhasInterfaceTests.test_edicao_rejeitada_preserva_campos_sem_sucesso
- frontend/tests/test_fluxos_clientes.py::FalhasInterfaceTests.test_edicao_incerta_e_confirmacao_divergente_impedem_novo_envio
- frontend/tests/test_fluxos_clientes.py::FalhasInterfaceTests.test_edicao_404_invalida_formulario_sem_sucesso



## Risks / Trade-offs

Não há controle de versão: concorrência pode sobrescrever dados. Lista e consulta preservam suas últimas consultas após edição, sem atualização automática. A comprovação integral de rejeição pelo backend pertence à Change `adicionar-cadastro-clientes-api` e não é substituída por mocks.

## Histórico e fontes

| Registro | Evidência |
| --- | --- |
| Implementação | Edição não está implementada no snapshot de 18/10/2026 (`b153306`) e já está presente no cliente Python e no app de c66fb69, registrado em 26/10/2026. A presença no segundo snapshot comprova que o código existia até esse marco, sem determinar seu dia exato de escrita. As correções posteriores de incerteza e redesenho do formulário são relatadas em docs/validacao-mvp-clientes.md, datado de 26/10/2026, mas não têm commit individual. |
| Documentação | README da edição já em c66fb69 (26/10/2026); relatório de regressão e registro formal do escopo em 26/10/2026. |
| Validação | A suíte local de 49 testes é registrada em 26/10/2026, com regressões e falhas da edição, sem novo PUT real. Há divergência no próprio snapshot c66fb69: tasks.md marca 3.4 concluída, mas frontend/README.md declara sua validação integrada pendente. O documento atual informa conclusão anterior e não reexecução do PUT; não há evidência local conclusiva para atribuir uma data ao teste integrado específico da interface de edição. |
| Datas indeterminadas | Dia exato da implementação e das correções posteriores; data e comprovação individual da validação integrada da interface de edição. A conclusão histórica do checkbox é preservada como registro, não usada para inventar essa data. |

- `git show b153306:frontend/clientes_api.py` — ainda sem atualizar_cliente
- `git show c66fb69:frontend/clientes_api.py` e `git show c66fb69:frontend/app.py` — edição presente
- `git show c66fb69:frontend/README.md` versus `git show c66fb69:openspec/changes/mvp-assistencia-tecnica/tasks.md` — divergência de validação
- [docs/validacao-mvp-clientes.md](../../../docs/validacao-mvp-clientes.md) — regressão local, sem novo PUT

Rastreabilidade: tarefas **3.4** de [mvp-assistencia-tecnica](../mvp-assistencia-tecnica/tasks.md). A cronologia comum e o significado das datas estão em [histórico técnico](../../../docs/historico-clientes.md).
