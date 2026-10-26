# Aplicação Streamlit

Estrutura inicial da tarefa 3.1 e formulário local da tarefa 3.2. A página carrega
a configuração externa e permite preencher nome, CPF, telefone e e-mail.
Somente o botão Cadastrar envia uma tentativa ao `POST /clientes` existente.
A parte antecipada da tarefa 3.3 apresenta ID, nome, CPF, telefone e e-mail pelo
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
simultâneas podem sobrescrever dados. Testes integrados da tarefa 3.4 ainda estão
pendentes de autorização; verificações locais simuladas não os substituem.

## Iniciar no PowerShell

Na raiz do projeto, com Python 3.10 ou superior:

```powershell
.venv/Scripts/python.exe -m pip install -r frontend/requirements.txt
$env:XANO_CLIENTES_API_BASE_URL = "<URL HTTPS do grupo Clientes>"
.venv/Scripts/python.exe -m streamlit run frontend/app.py --server.address 127.0.0.1 --browser.gatherUsageStats false
```

Os comandos reutilizam o ambiente `.venv` existente na raiz do projeto.
Substitua o marcador pela URL base de execução do grupo Clientes no Xano, incluindo
a identificação da branch quando aplicável. Não use a URL de documentação
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

A tarefa 3.1 permanece pendente: a consulta integrada ao backend exige autorização
específica e ainda não foi realizada. A tarefa 3.2 também permanece pendente de
verificação integrada autorizada e aprovação. A listagem e a consulta individual
estão implementadas localmente; edição também está implementada, com comprovação
integrada pendente. Exclusão ainda não está implementada.
A tarefa 3.3 foi comprovada por listagem integrada, consulta de cliente existente
e mensagem para cliente inexistente, e seu checkbox foi concluído em etapa anterior.
A tarefa 3.4 permanece pendente de comprovação integrada e não foi marcada como
concluída. Verificações locais com respostas simuladas não substituem esses testes no Xano.
