# Roteiro da apresentação — 5 minutos

Roteiro baseado no código, testes locais e evidências já registradas em
`docs/validacao-mvp-clientes.md` e `docs/api-equipamentos.md`. Não pressupõe
publicação das APIs de Equipamentos nem propõe criar ou alterar registros durante
uma demonstração sem autorização operacional.

## Antes de começar

No PowerShell, na raiz do projeto:

```powershell
$env:XANO_CLIENTES_API_BASE_URL = "https://x8ki-letl-twmt.n7.xano.io/api:assistencia-tecnica-clientes"
.venv\Scripts\python.exe -m streamlit run frontend/Clientes.py --server.address 127.0.0.1 --browser.gatherUsageStats false
```

A URL é a base documentada do grupo Clientes e foi confirmada atendendo `v1`
(live) na conferência registrada. A configuração vale somente para a sessão
atual do terminal. O Streamlit abre no endereço local mostrado no terminal;
encerre com `Ctrl+C`.

## Roteiro cronometrado

| Tempo | Demonstração | Evidência e limite |
|---|---|---|
| 0:00–0:35 | Apresente o objetivo: acompanhar clientes e equipamentos no contexto do sistema de assistência técnica. Mostre a navegação Clientes/Equipamentos. | Os cinco conceitos previstos no projeto são Clientes, Equipamentos, Técnicos, Ordens de Serviço e Serviços. Nesta entrega, estão disponíveis localmente as interfaces de Clientes e Equipamentos. |
| 0:35–2:15 | Em Clientes, percorra cadastro, listagem, consulta, edição e exclusão com confirmação explícita. Explique que cada ação só chama a API quando o usuário a submete. | O CRUD de Clientes está implementado. A evidência integrada registrada cobre POST de um cliente descartável, GET de consulta/listagem e DELETE seguido de confirmação; a suíte local cobre também edição e os fluxos de falha. Não crie, edite ou exclua registros durante a apresentação sem autorização e sem um registro fictício previamente separado para esse fim. |
| 2:15–3:10 | Abra Equipamentos e mostre os campos do domínio, o vínculo obrigatório por ID de cliente e os controles de cadastro, listagem e consulta/edição. | A interface e o cliente HTTP estão implementados e cobertos por testes simulados. O grupo/endpoints de Equipamentos não estão publicados; sem `XANO_EQUIPAMENTOS_API_BASE_URL`, a página informa a configuração pendente e não acessa o Xano. Portanto, apresente esta parte como interface local, sem executar ações. |
| 3:10–4:20 | Mostre `openspec/changes/mvp-assistencia-tecnica` e `openspec/changes/adicionar-gestao-equipamentos`, destacando proposta, especificação, design e tarefas verificáveis. | OpenSpec registra escopo, decisões e evidências. A Change de Equipamentos segue aberta: tarefas locais concluídas, publicação e validação remota pendentes. Não apresente o trabalho como cinco módulos concluídos. |
| 4:20–5:00 | Feche com arquitetura e próximos passos. | Backend Xano, frontend Streamlit/Python e evolução incremental por OpenSpec. Próximos incrementos previstos são Técnicos, Ordens de Serviço e Serviços, seguidos da integração do fluxo; não fazem parte desta demonstração implementada. |

## Verificações locais

Para executar os testes sem chamadas reais ao Xano:

```powershell
.venv\Scripts\python.exe -B -m unittest discover -s frontend/tests -p 'test_*.py' -q
```

Os testes usam respostas HTTP simuladas e bloqueiam conexões externas. A suíte
não substitui validação funcional dos endpoints de Equipamentos no Xano.
