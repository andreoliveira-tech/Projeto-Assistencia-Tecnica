# Validação do MVP de clientes — 26/10/2026

## Escopo

Change `mvp-assistencia-tecnica`: gerenciamento de clientes em Streamlit, consumindo
o grupo Clientes `436987`, workspace `149143`, instância
`x8ki-letl-twmt.n7.xano.io`. Equipamentos são apenas dependência da integridade da
exclusão; não foi implementado seu gerenciamento.

Dois GETs de metadados confirmaram o canonical `assistencia-tecnica-clientes`, a
branch do grupo `v1` e o retorno `label: "v1", live: true` da consulta da branch.
Conforme a regra oficial de URLs do Xano, a URL sem sufixo de branch atende à branch
live, portanto `v1` no momento da conferência:

```text
https://x8ki-letl-twmt.n7.xano.io/api:assistencia-tecnica-clientes
```

Essa associação pode mudar se a configuração live do workspace mudar. Os GETs de
metadados não alteraram recursos nem publicaram código.

## Testes locais

Comando executado:

```powershell
.venv/Scripts/python.exe -B -m unittest discover -s frontend/tests -p 'test_*.py' -q
```

**49 testes aprovados**, incluindo subcenários para configuração, contratos de
resposta, falhas de comunicação e HTTP, confirmação de exclusão, bloqueio por
equipamentos, resultados incertos, invalidação de estado e regressão de cadastro,
listagem, consulta e edição. Respostas HTTP são simuladas; conexões externas e
resolução DNS são bloqueadas pelos testes. No Windows há exceção para o socketpair
loopback interno do asyncio/AppTest. Essa proteção em Python não é um firewall do
processo e não demonstra isolamento universal de todas as primitivas de rede.

As verificações acrescentadas encontraram e corrigiram:

- HTTP 408 em cadastro e atualização tratado como resultado incerto, coerente com
  a exclusão; atualização exige consulta antes de novo envio.
- Atualização redesenha imediatamente seu formulário após a tentativa, exibindo
  o bloqueio do botão quando a confirmação estiver pendente.
- Confirmação de exclusão só aceita o erro 404 conhecido: objeto JSON com
  `code: "ERROR_CODE_NOT_FOUND"` e `message: "Cliente não encontrado."`.
  JSON inválido, código divergente ou mensagem genérica não confirmam ausência.

## Teste integrado autorizado

Executado com `frontend/verificar_integracao_clientes.py --executar`, usando
AppTest para operar o código real do Streamlit e as APIs reais. Não foi teste
visual em navegador nem teste de instalação em uma máquina nova.

O script restringe métodos, URL, corpo do cadastro e ID de exclusão, desabilita
redirecionamentos e repetições e recusa PUT ou DELETE de IDs preexistentes. Sem
`--executar`, ele apenas apresenta o plano, sem HTTP. A suíte local não executa
automaticamente esse cenário real e testa as restrições do script com transporte
simulado.

Cliente novo fictício: `T35-EXCLUSAO-20261026-01`, ID retornado **13**. Seus dados
demonstrativos foram os do plano aprovado. Nenhum cliente preexistente foi usado
como alvo de escrita.

| Ordem | Operação real | HTTP | Evidência |
| --- | --- | --- | --- |
| 1 | GET `/clientes` por Atualizar lista | 200 | Baseline de sete clientes guardado somente em memória |
| 2 | POST `/clientes` pelo formulário Cadastrar | 200 | Novo ID 13, ausente no baseline, com os quatro campos fictícios esperados |
| 3 | GET `/clientes/13` por Carregar para exclusão | 200 | Identidade e campos conferidos; botão Excluir desabilitado até confirmação |
| 4 | DELETE `/clientes/13` por Excluir definitivamente | 200 | Um único DELETE; resposta validada pela integração Python |
| 5 | GET `/clientes/13` posterior automático | 404 | Erro conhecido reconhecido pelo frontend; sucesso apresentado e listagem local invalidada |
| 6 | GET `/clientes` por Atualizar lista | 200 | Mesmos sete clientes do baseline, com igualdade dos IDs, campos, valores e tipos retornados pela API |

**Pseudonimização:** identificadores reais de clientes do baseline mencionados em evidências documentais foram substituídos por referências neutras (`CLIENTE_BASELINE_01` a `CLIENTE_BASELINE_07`). A correspondência preserva a rastreabilidade das comparações; nenhum registro do Xano foi alterado.

Abrir a aplicação, marcar a confirmação e executar um rerun depois da exclusão
não geraram chamadas adicionais. Total: **quatro GETs, um POST e um DELETE**.
O registro 13 foi removido no cenário. Não restou cliente descartável dessa rodada.

Não houve PUT real, escrita em equipamentos, alterações estruturais, publicação,
commit ou push. A comparação do baseline cobre os campos expostos pela API de
clientes; não representa auditoria de todas as tabelas ou colunas do workspace.

## Critérios concluídos e limites

| Tarefa | Resultado desta rodada |
| --- | --- |
| 3.1 | Aplicação iniciou no AppTest e consultou o backend real com sucesso |
| 3.2 | Formulário real criou o cliente 13; GET posterior conferiu os dados |
| 3.5 | Exclusão permitida comprovada pela interface e GET posterior; mensagem de bloqueio por equipamentos comprovada localmente com HTTP simulado |
| 3.6 | Falhas e contratos inesperados cobertos localmente nos quatro fluxos de escrita/consulta e na listagem, sem falsa confirmação de sucesso |
| 1.3 | Pendente de verificação integrada de rejeição sem persistência e normalização completa no backend |

O bloqueio do backend com equipamentos já possuía testes integrados registrados
na tarefa 2.5. Nesta rodada não se repetiu DELETE contra clientes preexistentes,
nem se criaram equipamentos para novo teste de bloqueio. A apresentação da mensagem
no frontend foi verificada pelos testes locais. A conclusão da 3.5 combina essas
evidências com o cenário real permitido, conforme a autorização atual.

A tarefa 3.4 já constava concluída no OpenSpec antes desta rodada. Sua implementação
e regressão local foram verificadas, mas não foi reexecutado PUT real nesta rodada.
As tarefas concluídas não implicam aprovação da pendência 1.3. A integridade da
exclusão permanece limitada a operações sequenciais, conforme decisão da Change.

O lote adicional para a 1.3 está em
[plano-validacao-backend-clientes.md](plano-validacao-backend-clientes.md). Não foi
executado sem autorização específica. Se revelar defeito que exija modificar ou
publicar recursos do Xano, essa correção também precisará de autorização própria.

## Referências

- [Contrato das APIs](api-clientes.md)
- [Tarefas OpenSpec](../openspec/changes/mvp-assistencia-tecnica/tasks.md)
- [Design e testes anteriores do backend](../openspec/changes/mvp-assistencia-tecnica/design.md)
- [Xano: branch live e resolução de URLs](https://docs.xano.com/team-collaboration/branching-and-merging)
