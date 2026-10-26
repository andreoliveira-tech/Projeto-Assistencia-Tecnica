# Aplicação Streamlit

## Módulo de Equipamentos

A página `pages/1_Equipamentos.py` oferece CRUD com os seis atributos do domínio,
carregamento para edição/exclusão, confirmação explícita e tratamento de incerteza.
É descoberta pela navegação multipágina do Streamlit. Configure separadamente
`XANO_EQUIPAMENTOS_API_BASE_URL` somente após conferir a URL real do grupo publicado.
Sem essa variável, a página não realiza HTTP. Não há backend novo publicado nesta
etapa: as definições XanoScript são locais, e DELETE depende da consulta real de OS.
Os controles de exclusão ficam indisponíveis por padrão. Defina
`XANO_EQUIPAMENTOS_DELETE_VALIDATED=true` somente depois que o endpoint DELETE e
sua validação integrada de dependências forem publicados e confirmados. A URL base
não habilita exclusão.
Consulte o [contrato proposto e suas limitações](../docs/api-equipamentos.md).

Os testes de Equipamentos estão em `tests/test_equipamentos.py` e usam HTTP
simulado e rede externa bloqueada. Eles integram a descoberta da suíte abaixo,
sem executar o script de integração real de Clientes.
Resultado atual: **79 testes locais aprovados**, sendo 30 de Equipamentos e
49 de Clientes. A validação de sintaxe aprovou sete arquivos XanoScript novos;
publicação e verificação funcional no backend continuam pendentes.

## Módulo de Clientes

Interface de clientes com cadastro, listagem, consulta individual, edição e
exclusão confirmada. A página carrega a configuração externa e permite preencher
nome, CPF, telefone e e-mail.
Somente o botão Cadastrar envia uma tentativa ao `POST /clientes` existente.
A listagem apresenta ID, nome, CPF, telefone e e-mail pelo
`GET /clientes`. Somente o botão Atualizar lista consulta a API. A listagem trata
lista vazia, falhas de comunicação e respostas inválidas. O resultado permanece
na sessão como última consulta; um cadastro não atualiza essa lista automaticamente.

A consulta individual da tarefa 3.3 utiliza `GET /clientes/{id_cliente}` somente
ao submeter o formulário Consultar cliente. Identificadores vazios ou que não
representem inteiros positivos são rejeitados localmente. O resultado apresenta
ID, nome, CPF, telefone e e-mail, mantendo CPF e telefone como texto. HTTP 404
informa Cliente não encontrado; timeout, falhas de comunicação, erros HTTP e
respostas fora do contrato apresentam mensagens de erro. Não há repetição automática.
O estado da consulta é independente do cadastro e da listagem; cada tentativa
limpa o resultado anterior, inclusive quando o identificador é inválido. A troca
da URL base também limpa o estado. O resultado é identificado como última consulta.

## Edição de clientes — tarefa 3.4

Informe um identificador inteiro positivo e clique em Carregar para edição.
O GET individual preenche nome, CPF, telefone e e-mail como texto. O identificador
carregado não é editável e é usado na rota, independentemente do conteúdo do campo
de seleção. Somente Salvar alterações envia um PUT, com os quatro campos obrigatórios.
Os dados são validados e normalizados pelo backend.

Após um PUT com resposta válida, um novo GET do mesmo identificador confirma os
cinco campos contra a resposta do PUT, já normalizada. Somente a correspondência
confirma sucesso e apresenta os dados consultados. Rejeições preservam os valores
digitados; cliente inexistente invalida a edição. Não há repetição automática.
Timeout, comunicação interrompida, resposta inesperada ou confirmação divergente
não comprovam ausência de gravação: não reenvie antes de conferir o estado atual.
A ação Conferir estado atual executa somente GET e recarrega o formulário; ela
não declara a tentativa anterior aprovada. Nenhuma restauração é automática.

O estado da edição é independente dos demais fluxos. A listagem e a consulta
individual continuam mostrando sua última consulta e não são atualizadas
automaticamente pela edição. A API não oferece controle de versão: alterações
simultâneas podem sobrescrever dados. A tarefa 3.4 já constava concluída no OpenSpec.
Nesta rodada a edição recebeu verificação local de regressão e falhas, sem novo
PUT real. A confirmação pendente bloqueia imediatamente o botão Salvar alterações,
inclusive quando o serviço retorna HTTP 408.

## Exclusão de clientes — tarefa 3.5

Informe um identificador inteiro positivo e clique em Carregar para exclusão.
Esse botão executa somente o GET individual. A interface apresenta ID e nome do
cliente, um aviso de exclusão definitiva e uma confirmação inicialmente desmarcada
que identifica o cliente. Somente marcar a confirmação e clicar em Excluir
definitivamente envia um único DELETE, sem corpo. Abrir a página, preencher o
identificador, marcar a confirmação, cancelar ou executar reruns não envia DELETE.

Trocar o identificador, recarregar o cliente ou mudar a URL base descarta a seleção
e a confirmação anteriores. O DELETE utiliza o identificador do cliente carregado.
Cancelar não chama o backend; para tentar novamente será necessário carregar e
confirmar o cliente outra vez. Cada tentativa consome a seleção, impedindo reenvio
automático. O cliente HTTP usa timeout de conexão/leitura `(5, 20)` e não segue
redirecionamentos.

O backend decide sobre equipamentos vinculados. O HTTP 400 com a mensagem conhecida
de equipamentos apresenta Exclusão bloqueada. Outros erros 400, inclusive falha
na verificação de vínculos, são apresentados como rejeição sem atribuir equipamentos
ao cliente. HTTP 404 informa Cliente não encontrado e não declara sucesso da tentativa.
A interface não consulta equipamentos nem realiza exclusão em cascata.

Somente HTTP 200 com `id_cliente` inteiro igual ao solicitado e `excluido: true`
permite a confirmação posterior automática por GET. O sucesso só é apresentado
quando esse GET retorna 404 com objeto JSON contendo `code: "ERROR_CODE_NOT_FOUND"`
e a mensagem conhecida `Cliente não encontrado.`. Um 404 genérico ou com JSON
inválido não confirma ausência. Se o GET falhar ou ainda retornar o cliente, a ausência
não está confirmada. Timeout, HTTP 408, falha de comunicação, 5xx ou resposta
fora do contrato também deixam o resultado incerto, sem repetição automática.

Nessas situações, Conferir estado atual da exclusão executa apenas GET. Se o cliente
existir, o resultado é recarregado com nova confirmação desmarcada. Um 404 na
conferência manual informa ausência atual sem atribuir a exclusão à tentativa
anterior. Se a conferência falhar, o reenvio continua indisponível. Cancelar e
recomeçar também exige novo carregamento por GET e nova confirmação.

Quando a ausência é constatada, a listagem em sessão é invalidada, sem consulta
automática. Consulta individual e edição desse mesmo cliente são invalidadas,
inclusive dados e confirmação de edição anteriores. Estados de consulta e edição
de outros clientes são preservados. Atualizar lista permanece uma ação explícita.

A garantia de integridade do backend permanece limitada a operações sequenciais.
A URL `https://x8ki-letl-twmt.n7.xano.io/api:assistencia-tecnica-clientes` foi associada
formalmente ao workspace `149143`, grupo `436987` e branch `v1` live por metadados.
Em 26/10/2026, o cenário integrado autorizado criou pelo formulário o cliente
descartável 13 e o excluiu pela interface, com GET posterior e comparação do
baseline. Os sete clientes preexistentes foram preservados nos campos retornados
pela API. O bloqueio por equipamentos foi apresentado em testes locais simulados;
não houve DELETE contra cliente preexistente nesta rodada. Consulte as
[evidências e limitações](../docs/validacao-mvp-clientes.md).

### Verificação local sem rede

Na raiz do projeto:

```powershell
.venv/Scripts/python.exe -B -m unittest discover -s frontend/tests -p 'test_*.py' -q
```

Os testes usam respostas HTTP simuladas, bloqueiam conexões externas e resolução
DNS e falham em qualquer HTTP não previsto. No Windows, somente a conexão loopback
interna de `socketpair`, necessária ao asyncio do AppTest, é permitida; ela não
executa HTTP. AppTest exercita a interface sem iniciar um servidor web.
São cobertos confirmação, cancelamento, troca de cliente/URL, respostas
de erro, resultados incertos, GET posterior, invalidação de estado, configuração e
regressões de todos os fluxos. Registro anterior de Clientes: **49 testes aprovados**;
a suíte atual, incluindo Equipamentos, tem **77 testes aprovados**.
Nenhuma configuração real ou credencial do Xano é necessária para a suíte local.

O script `frontend/verificar_integracao_clientes.py` é separado da suíte. Sem
argumentos apenas apresenta o plano; `--executar` faz chamadas reais e exige
autorização prévia para criar e excluir seu único cliente descartável. Ele recusa
PUT e exclusão de IDs do baseline. O cenário desta rodada já foi executado com
sucesso; não é necessário repeti-lo para iniciar o aplicativo.

## Iniciar no PowerShell

Na raiz do projeto, com Python 3.10 ou superior:

```powershell
.venv/Scripts/python.exe -m pip install -r frontend/requirements.txt
$env:XANO_CLIENTES_API_BASE_URL = "https://x8ki-letl-twmt.n7.xano.io/api:assistencia-tecnica-clientes"
.venv/Scripts/python.exe -m streamlit run frontend/Clientes.py --server.address 127.0.0.1 --browser.gatherUsageStats false
```

Use `Clientes.py` como ponto de entrada para identificar a página inicial como
“Clientes” na navegação multipágina do Streamlit, em vez do nome genérico “app”.

Os comandos reutilizam o ambiente `.venv` existente na raiz do projeto.
A URL acima atendia à branch `v1` live no momento da conferência. Se a configuração
live mudar, confirmar novamente o ambiente antes de operações de escrita.
Não use a URL de documentação
`apispec`, a Metadata API ou o caminho final `/clientes` como URL base do grupo.
Não inclua tokens administrativos ou credenciais. A variável vale para a sessão
atual do terminal e não é gravada em arquivo. Arquivos `.env` não são carregados.

Abra o endereço local informado pelo Streamlit. Sem a variável, a página abre e
exibe uma orientação de configuração. Com URL inválida, exibe uma mensagem sem
reproduzir seu conteúdo. Uma URL aceita indica somente formato válido, não
conectividade ou autorização de acesso.

Encerre o servidor com Ctrl+C. A instalação de dependências acessa o repositório
de pacotes. Abrir a página ou preencher campos não chama o Xano. Não pressione
Cadastrar durante uma conferência exclusivamente visual sem autorização para
gravar no backend, nem Atualizar lista ou Consultar cliente sem autorização para
consultar registros.
Campos vazios são identificados localmente; validações de CPF,
telefone e e-mail e normalização permanecem no backend. Erros preservam os campos.

Não há repetição automática do POST. Em timeout, falha de comunicação ou resposta
inesperada, confirme a persistência por um meio autorizado antes de reenviar.

As tarefas 3.1, 3.2, 3.5 e 3.6 foram concluídas no alcance discriminado nas evidências.
As tarefas 3.3 e 3.4 já constavam concluídas. A pendência da Change é a 1.3:
comprovar no backend rejeição de dados inválidos sem criar ou alterar registros e
cobrir a normalização prevista. O código de validação local não substitui esses
testes. O [lote adicional proposto](../docs/plano-validacao-backend-clientes.md)
depende de autorização e não integra o cenário real de exclusão já executado.
