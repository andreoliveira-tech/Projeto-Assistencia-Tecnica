# Design: Exclusão confirmada e tratamento de falhas no Streamlit

## Context

Concluir o fluxo de exclusão com confirmação explícita e preservar informação confiável diante de bloqueios, respostas ambíguas e falhas de comunicação nos fluxos do frontend. O contrato correspondente está em [specs/exclusao-falhas-clientes-ui/spec.md](specs/exclusao-falhas-clientes-ui/spec.md).

Dependências: [adicionar-consulta-clientes-api](../2026-10-26-adicionar-consulta-clientes-api/proposal.md), [adicionar-exclusao-clientes-api](../2026-10-26-adicionar-exclusao-clientes-api/proposal.md), [adicionar-cadastro-clientes-streamlit](../2026-10-26-adicionar-cadastro-clientes-streamlit/proposal.md), [adicionar-consulta-clientes-streamlit](../2026-10-26-adicionar-consulta-clientes-streamlit/proposal.md), [adicionar-edicao-clientes-streamlit](../../adicionar-edicao-clientes-streamlit/proposal.md)

## Goals / Non-Goals

**Goals:** Carregamento e confirmação explícita antes de DELETE único. Validação do retorno e GET estrito de ausência, sem reenvio automático. Invalidação dos estados pertinentes e tratamento transversal de falhas. Rastreabilidade do contrato documentado dos cinco endpoints.

**Non-Goals:** ampliar o modelo de domínio ou alterar os contratos dos demais fluxos. Manter o comportamento dos recursos existentes.

## Decisions

Consumir a seleção antes de enviar DELETE e exigir nova leitura/confirmação para nova tentativa. Somente DELETE 200 com id_cliente inteiro igual e excluido exatamente true permite GET posterior automático. O GET deve retornar 404 com JSON objeto, code exatamente ERROR_CODE_NOT_FOUND e message exatamente Cliente não encontrado.; não presumir valor de payload. 408/timeout/5xx/contrato inesperado são incertos, sem retry. Bloqueio conhecido por equipamentos é diferente de erro genérico na verificação de vínculos.

Consumir a seleção antes da escrita impede que reruns repitam DELETE. A confirmação estrita evita confundir ausência do cliente com erro de rota ou infraestrutura.

### Código e contratos

- [frontend/app.py](../../../../frontend/app.py)
- [frontend/clientes_api.py](../../../../frontend/clientes_api.py)
- [frontend/tests/test_exclusao_clientes.py](../../../../frontend/tests/test_exclusao_clientes.py)
- [frontend/tests/test_fluxos_clientes.py](../../../../frontend/tests/test_fluxos_clientes.py)
- [frontend/verificar_integracao_clientes.py](../../../../frontend/verificar_integracao_clientes.py)
- [frontend/README.md](../../../../frontend/README.md)
- [docs/api-clientes.md](../../../../docs/api-clientes.md)
- [docs/validacao-mvp-clientes.md](../../../../docs/validacao-mvp-clientes.md)

## Verification

A suíte já executada aprovou 49 testes: 31 em test_exclusao_clientes.py e 18 em test_fluxos_clientes.py. O cenário integrado anterior via AppTest executou quatro GETs, um POST e um DELETE somente do descartável 13; sete clientes preexistentes permaneceram iguais nos campos retornados. O bloqueio na UI foi simulado e o backend já possuía evidência integrada da 2.5. Não foram executados novos testes nesta revisão documental.

Fontes de testes e resultados:

- frontend/tests/test_exclusao_clientes.py::ClienteHttpTests e InterfaceTests (31 testes)
- frontend/tests/test_fluxos_clientes.py (18 testes; inclui configuração, falhas e limites do script integrado)
- docs/validacao-mvp-clientes.md — cenário integrado e seus limites
- docs/api-clientes.md — contrato e origem das evidências



## Risks / Trade-offs

AppTest não é teste visual no navegador. A proteção de rede dos testes bloqueia o transporte HTTP e sockets/DNS em Python com exceção do socketpair loopback interno do Windows; não é firewall universal. Não se repetiu DELETE em clientes preexistentes nem se provocou falha integrada de consulta de vínculos. Integridade continua sequencial.

## Histórico e fontes

| Registro | Evidência |
| --- | --- |
| Implementação | O tratamento inicial de falhas de cadastro/listagem já está no snapshot de 18/10/2026 (`b153306`). A exclusão da interface ainda não existe em c66fb69 (26/10/2026 às 02:17:20 UTC−03); foi implementada na etapa local posterior de exclusão, seguida de correções de 408 e confirmação estrita. O relatório datado de 26/10/2026 comprova a validação desse estado posterior, mas não fornece uma data individual de implementação de cada alteração. Não se atribui a todo o tratamento de falhas a data da exclusão. |
| Documentação | README inicial de falhas em 18/10/2026; registro de exclusão ainda não implementada no README de c66fb69; contrato, relatório das correções/testes e registro formal do escopo em 26/10/2026. |
| Validação | A suíte completa de 49 testes e o cenário integrado de criação/exclusão somente do descartável 13 estão explicitamente registrados em 26/10/2026. Os 31 testes iniciais de exclusão são uma etapa anterior dessa suíte, sem data individual comprovada nos documentos locais. A validação estrutural das dez Changes ocorreu na sua organização formal, também em 26/10/2026, e não é teste funcional do produto. |
| Datas indeterminadas | Datas exatas de escrita da exclusão, das correções de 408/404 e da execução isolada dos 31 testes iniciais. A sequência funcional e a data do relatório consolidado são conhecidas. |

- `git show b153306:frontend/clientes_api.py` — tratamento inicial de falhas
- `git show c66fb69:frontend/README.md` — exclusão ainda não implementada; cliente Python sem excluir_cliente
- [docs/validacao-mvp-clientes.md](../../../../docs/validacao-mvp-clientes.md) — 49 testes e cenário integrado datados
- [docs/api-clientes.md](../../../../docs/api-clientes.md) — contrato conferido em 26/10/2026

Rastreabilidade: tarefas **3.5 e 3.6; consolidação da rastreabilidade da 2.6** de [mvp-assistencia-tecnica](../../mvp-assistencia-tecnica/tasks.md). A cronologia comum e o significado das datas estão em [histórico técnico](../../../../docs/historico-clientes.md).
