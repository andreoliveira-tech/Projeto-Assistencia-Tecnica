# Histórico técnico do gerenciamento de clientes

## Escopo dos registros

Este documento relaciona os marcos do código, dos contratos e das verificações do gerenciamento de clientes. As fontes são o histórico Git local, os documentos de contrato e os resultados previamente registrados; datas de modificação de arquivos não foram utilizadas como evidência de implementação.

As Changes por funcionalidade foram formalizadas retrospectivamente em 26/10/2026 a partir do trabalho registrado em [mvp-assistencia-tecnica](../openspec/changes/mvp-assistencia-tecnica/proposal.md), preservado como referência. O campo `created` dos seus metadados identifica a criação documental, não o início da implementação. Seus nomes e dependências descrevem escopos técnicos, sem representar ciclos históricos independentes. O histórico específico de cada recurso está no respectivo design.

## Marcos do repositório

| Registro | Conteúdo comprovado | Limite da evidência |
| --- | --- | --- |
| 04/10/2026 — `c37c9c2` | Estrutura inicial OpenSpec e Change inicial mais ampla. | Essa Change foi removida em `b355b54`, em 05/10; não equivale à implementação do MVP atual. |
| 05/10/2026 — `743f189` | Documentos de contexto e modelo de domínio. | Definição de domínio não comprova criação de tabelas ou APIs. |
| 12/10/2026 — `fa47a58` | Importação geral de recursos XanoScript do workspace. | O snapshot ainda não contém os arquivos de Cliente/Equipamento; não data sua criação remota. |
| 18/10/2026, 20:50:42 UTC−03 — `b153306` | Configuração externa, cadastro, listagem e tratamento inicial de falhas no Streamlit, com README. | Consulta individual, edição e exclusão ainda ausentes; o README declara as verificações integradas pendentes. |
| 25/10/2026, 16:35:57 UTC−03 — `6cec2f6` | Registro da Change atual de cadastro. Tarefas 1.1/1.2/1.5 e 2.1–2.4 já declaradas concluídas. | Não informa o dia individual da criação dos recursos remotos nem dos testes originais. |
| 26/10/2026, 02:17:20 UTC−03 — `c66fb69` | Captura dos XanoScripts de Cliente, Equipamento, POST, GETs, PUT e validador; consulta individual e edição já presentes no frontend; evidências sequenciais e do DELETE do backend. | A captura no Git não é data de criação remota. A exclusão da interface ainda não está implementada nesse snapshot. |

Datas de autor e committer coincidem nos três últimos commits citados. Um snapshot comprova que o código existia naquele registro, sem identificar necessariamente o dia de sua escrita. A ausência no snapshot anterior e presença no posterior delimita marcos conhecidos, sem justificar uma data exata intermediária.

O metadado original `created: 2026-10-12` é preservado como declaração existente. A Change atual foi adicionada ao histórico disponível em 25/10/2026, em `6cec2f6`; não há prova suficiente para usar 12/10 como data de criação dessa versão da Change ou de implementação dos seus recursos.

## Versões publicadas e conferência de contratos

O [design original](../openspec/changes/mvp-assistencia-tecnica/design.md), já presente em `c66fb69`, registra:

- `clientes/consultar_dependencias`: versão `2026-10-26 03:22:11+0000`.
- Procedimento de investigação da tarefa 1.6: versão `2026-10-26 03:27:53+0000`.
- DELETE de clientes, endpoint `4107955`: versão `2026-10-26 04:30:46+0000`.

Esses horários identificam versões publicadas e permanecem em 26/10 ao converter de UTC para UTC−03; não identificam o início da codificação.

O [contrato das APIs](api-clientes.md) registra a conferência de metadados e definições publicadas dos cinco endpoints em 26/10/2026, com `include_draft=false` e `include_xanoscript=true`. A conferência não executou APIs de negócio. As chamadas dos endpoints às funções auxiliares não comprovam seu interior publicado atual; as inspeções anteriores da 1.6 têm alcance próprio, registrado no design.

Ambiente das evidências: workspace `149143`, branch `v1` live, grupo `436987`, instância `x8ki-letl-twmt.n7.xano.io`. A base `https://x8ki-letl-twmt.n7.xano.io/api:assistencia-tecnica-clientes` foi associada à branch live por metadados na conferência registrada. Essa associação depende da configuração live e não foi reconsultada nesta revisão. Os endpoints constam sem autenticação de usuário nos metadados; isso não acrescenta autenticação ao MVP.

## Verificações funcionais registradas

- **Integridade sequencial, 26/10/2026:** inspeções e cenários da tarefa 1.6 documentados no design original. A garantia não se estende a operações concorrentes.
- **DELETE do backend, 26/10/2026:** bloqueio com equipamentos, inexistência e exclusão permitida registrados na 2.5. A falha da consulta de vínculos foi verificada por inspeção e simulação, sem provocar indisponibilidade no runtime Xano.
- **Frontend, 26/10/2026:** o [relatório de validação](validacao-mvp-clientes.md) registra 49 testes locais aprovados: 31 em `frontend/tests/test_exclusao_clientes.py` e 18 em `frontend/tests/test_fluxos_clientes.py`. A cobertura é compartilhada entre os recursos e não deve ser somada por Change. A execução isolada dos 31 iniciais não possui data individual documentada.
- **Integração posterior, 26/10/2026:** AppTest com APIs reais criou e excluiu somente o descartável 13. Foram quatro GETs, um POST e um DELETE, com os sete clientes preexistentes preservados nos campos retornados pela API. Esse cenário é posterior ao estado de `c66fb69`, não um teste visual em navegador nem um novo PUT real.

Os testes locais simulam HTTP e bloqueiam transporte, sockets e DNS em Python, com exceção do socketpair loopback interno do Windows. Isso não equivale a um firewall universal nem comprova a validação de entradas no backend. A comparação do baseline abrange os campos expostos pela API, não todas as tabelas e colunas do workspace.

As datas exatas da criação inicial das tabelas/APIs, da escrita da consulta individual e edição, da implementação da exclusão no frontend e das correções individuais de 408/404 permanecem indeterminadas quando não há registro específico. O relatório consolidado data a verificação, não cada alteração de código.

### Divergência no registro da edição

Em `c66fb69`, o checklist original marca 3.4 concluída, enquanto o README do frontend ainda declara validação integrada pendente. O documento atual preserva a conclusão anterior e registra regressão local sem novo PUT real. O status histórico é mantido com essa ressalva; data e comprovação individual do teste integrado específico da interface de edição não podem ser deduzidas desses registros.

## Validação pendente do backend

A tarefa original 1.3 permanece aberta em [adicionar-cadastro-clientes-api](../openspec/changes/adicionar-cadastro-clientes-api/tasks.md): comprovar rejeição integral de entradas inválidas sem criar ou alterar registros e normalização completa em POST/PUT. Há regras no validador local e chamadas compartilhadas nas definições dos endpoints, mas a prova funcional completa continua pendente.

O [plano existente](plano-validacao-backend-clientes.md) descreve 50 requisições. O lote não foi executado e não está autorizado nesta refatoração documental. Uma execução futura e eventuais alterações do backend exigem autorização própria.

A limitação concorrente, a ausência de cópias locais de alguns recursos publicados e os limites dos testes são restrições declaradas, não garantias resolvidas. O gerenciamento de equipamentos, técnicos, ordens de serviço e serviços permanece fora do MVP de clientes.

