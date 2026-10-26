# Design: Configuração e cadastro na interface Streamlit

## Context

Permitir operar o cadastro pelo Streamlit com configuração externa do grupo de APIs e confirmação de resposta compatível, sem incluir segredos no código. O contrato correspondente está em [specs/configuracao-cadastro-clientes-ui/spec.md](specs/configuracao-cadastro-clientes-ui/spec.md).

Dependências: [adicionar-cadastro-clientes-api](../../adicionar-cadastro-clientes-api/proposal.md), [adicionar-consulta-clientes-api](../2026-10-26-adicionar-consulta-clientes-api/proposal.md)

## Goals / Non-Goals

**Goals:** Aplicação Streamlit/Python e XANO_CLIENTES_API_BASE_URL. Formulário de cadastro com quatro campos e envio por ação explícita. Erros de configuração e de cadastro sem falsa confirmação.

**Non-Goals:** ampliar o modelo de domínio ou alterar os contratos dos demais fluxos. Manter o comportamento dos recursos existentes.

## Decisions

Configurar a URL por variável de ambiente, validar HTTPS e ausência de credenciais/query/fragmento e normalizar barra final. Usar requests com timeout (5,20), allow_redirects=false e sem retry automático. Somente o botão Cadastrar faz POST. O frontend não substitui validação do backend.

Configuração externa evita acoplar a aplicação a uma instância ou armazenar credenciais no repositório.

### Código e contratos

- [frontend/config.py](../../../../frontend/config.py)
- [frontend/app.py](../../../../frontend/app.py)
- [frontend/clientes_api.py](../../../../frontend/clientes_api.py)
- [frontend/requirements.txt](../../../../frontend/requirements.txt)
- [frontend/README.md](../../../../frontend/README.md)
- [docs/api-clientes.md](../../../../docs/api-clientes.md)

## Verification

O cenário integrado já documentado iniciou a aplicação real por AppTest, consultou a lista e criou o descartável 13 pelo formulário, conferido por GET. Os 49 testes locais existentes incluem configuração ausente/inválida, cadastro sem campos, rejeições e resultados incertos. A ligação da URL ao workspace 149143, grupo 436987 e v1 live foi confirmada anteriormente por metadados.

Fontes de testes e resultados:

- frontend/tests/test_fluxos_clientes.py::ConfiguracaoTests
- frontend/tests/test_fluxos_clientes.py::FalhasInterfaceTests.test_cadastro_falhas_preservam_campos_e_nao_reenviam_em_rerun
- frontend/tests/test_fluxos_clientes.py::FalhasInterfaceTests.test_campos_vazios_no_cadastro_nao_enviam
- docs/validacao-mvp-clientes.md — inicialização e POST pelo formulário

A validação integral do backend é acompanhada em [adicionar-cadastro-clientes-api](../../adicionar-cadastro-clientes-api/tasks.md); a cobertura simulada não substitui esse critério.

## Risks / Trade-offs

O teste integrado foi AppTest com API real, não navegador nem instalação em computador novo. A associação live é a registrada em 26/10/2026 e pode mudar por configuração externa. A validação integral do backend permanece na Change `adicionar-cadastro-clientes-api`.

## Histórico e fontes

| Registro | Evidência |
| --- | --- |
| Implementação | A primeira implementação versionada da configuração, aplicação e cadastro Streamlit é de 18/10/2026, no commit b153306 (20:50:42 UTC−03). O conteúdo desse commit já possui configuração externa, quatro campos, envio explícito e tratamento inicial de falhas. Isso comprova código existente naquela data, não o dia de início de sua escrita. Ajustes posteriores, como tratamento específico de HTTP 408, aparecem no código atual e no relatório de 26/10/2026, sem commit individual que date sua implementação. |
| Documentação | README do frontend incluído em 18/10/2026 (`b153306`); planejamento consolidado em 25/10/2026 e atualizado em 26/10/2026; relatório de validação e registro formal do escopo em 26/10/2026. |
| Validação | O README de b153306 ainda declarava a integração das tarefas 3.1/3.2 pendente. Em c66fb69 essa pendência continuava expressa. A comprovação de início da aplicação, consulta real e cadastro real por AppTest é registrada no relatório de 26/10/2026, junto à suíte local de 49 testes. Não se atribui esse teste integrado a 18/10. |
| Datas indeterminadas | Dia exato do início da codificação e dos ajustes posteriores sem commit individual; esses limites não apagam o marco versionado de 18/10. |

- `git show b153306:frontend/app.py`, `git show b153306:frontend/clientes_api.py` e `git show b153306:frontend/config.py`
- `git show b153306:frontend/README.md` e `git show c66fb69:frontend/README.md` — validação integrada ainda pendente nesses snapshots
- [docs/validacao-mvp-clientes.md](../../../../docs/validacao-mvp-clientes.md) — comprovação posterior de 3.1/3.2

Rastreabilidade: tarefas **3.1 e 3.2; parcela de 2.6 relativa à configuração de consumo** de [mvp-assistencia-tecnica](../../mvp-assistencia-tecnica/tasks.md). A cronologia comum e o significado das datas estão em [histórico técnico](../../../../docs/historico-clientes.md).
