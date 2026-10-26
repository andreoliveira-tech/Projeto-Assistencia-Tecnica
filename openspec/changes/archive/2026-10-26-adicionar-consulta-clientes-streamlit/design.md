# Design: Listagem e consulta individual no Streamlit

## Context

Exibir clientes e permitir consulta por identificador sem disparar chamadas em reruns e sem conservar um resultado anterior como se fosse a consulta atual. O contrato correspondente está em [specs/consulta-clientes-ui/spec.md](specs/consulta-clientes-ui/spec.md).

Dependências: [adicionar-consulta-clientes-api](../2026-10-26-adicionar-consulta-clientes-api/proposal.md), [adicionar-cadastro-clientes-streamlit](../2026-10-26-adicionar-cadastro-clientes-streamlit/proposal.md)

## Goals / Non-Goals

**Goals:** Listagem sob ação Atualizar lista. Consulta individual por inteiro positivo e mensagem de cliente inexistente. Estados independentes e descarte de resultados anteriores em falhas ou troca da URL.

**Non-Goals:** ampliar o modelo de domínio ou alterar os contratos dos demais fluxos. Manter o comportamento dos recursos existentes.

## Decisions

Usar session_state para últimas consultas independentes. Listar somente no botão correspondente e consultar somente na submissão do formulário. Validar tipo dos cinco campos e o ID retornado. Preservar CPF e telefone como texto e limpar o resultado anterior antes de cada nova tentativa.

Manter resultados como últimas consultas evita afirmar que uma listagem em sessão está sincronizada com o backend.

### Código e contratos

- [frontend/app.py](../../../../frontend/app.py)
- [frontend/clientes_api.py](../../../../frontend/clientes_api.py)
- [frontend/README.md](../../../../frontend/README.md)

## Verification

Os testes locais exercitam lista vazia, falhas, consulta inválida/inexistente e regressão dos fluxos. O cenário integrado existente consultou lista inicial/final e carregou o cliente descartável, com resultados 200; o GET posterior retornou o 404 conhecido. O erro 404 genérico da consulta comum é distinto do modo estrito de confirmação de exclusão.

Fontes de testes e resultados:

- frontend/tests/test_exclusao_clientes.py::InterfaceTests.test_regressao_cadastro_listagem_consulta_e_edicao
- frontend/tests/test_fluxos_clientes.py::FalhasInterfaceTests.test_listagem_vazia_e_falha_descartam_resultado_anterior
- frontend/tests/test_fluxos_clientes.py::FalhasInterfaceTests.test_consulta_com_falha_limpa_resultado_anterior
- frontend/tests/test_exclusao_clientes.py::ClienteHttpTests.test_regressao_404_dos_fluxos_existentes



## Risks / Trade-offs

Dados em sessão são a última consulta e podem ficar desatualizados; não há atualização automática após cadastro ou edição. O modo comum apresenta não encontrado para HTTP 404; a confirmação estrita de ausência é exclusiva da Change `adicionar-exclusao-clientes-streamlit`.

## Histórico e fontes

| Registro | Evidência |
| --- | --- |
| Implementação | Listagem já implementada no snapshot de 18/10/2026 (`b153306`). A consulta individual não existe nesse snapshot e aparece em c66fb69, de 26/10/2026 às 02:17:20 UTC−03, tanto no cliente Python quanto na interface. Trata-se de dois incrementos distintos. O Git não determina o dia exato em que a consulta individual foi escrita entre esses registros. |
| Documentação | README da listagem em 18/10/2026; descrição de consulta individual e conclusão da 3.3 no registro de 26/10/2026 (`c66fb69`); registro formal do escopo em 26/10/2026. |
| Validação | c66fb69 já registra a 3.3 concluída e seu README relata listagem integrada, consulta existente e mensagem de inexistente, sem datar individualmente essas execuções. Os testes de regressão e os GETs do cenário do descartável constam do relatório de 26/10/2026; não datam a implementação inicial da listagem. |
| Datas indeterminadas | Dia exato de implementação da consulta individual e das primeiras validações de cada consulta; há limites de presença no histórico, não uma data única de desenvolvimento. |

- `git show b153306:frontend/app.py` — somente cadastro e listagem
- `git show c66fb69:frontend/clientes_api.py` e `git show c66fb69:frontend/app.py` — consulta individual implementada
- `git show c66fb69:frontend/README.md` e `git show c66fb69:openspec/changes/mvp-assistencia-tecnica/tasks.md` — registro da 3.3
- [docs/validacao-mvp-clientes.md](../../../../docs/validacao-mvp-clientes.md)

Rastreabilidade: tarefas **3.3** de [mvp-assistencia-tecnica](../../mvp-assistencia-tecnica/tasks.md). A cronologia comum e o significado das datas estão em [histórico técnico](../../../../docs/historico-clientes.md).
