# Aplicação Streamlit

Estrutura inicial da tarefa 3.1 e formulário local da tarefa 3.2. A página carrega
a configuração externa e permite preencher nome, CPF, telefone e e-mail.
Somente o botão Cadastrar envia uma tentativa ao `POST /clientes` existente.
A parte antecipada da tarefa 3.3 apresenta ID, nome, CPF, telefone e e-mail pelo
`GET /clientes`. Somente o botão Atualizar lista consulta a API. A listagem trata
lista vazia, falhas de comunicação e respostas inválidas. O resultado permanece
na sessão como última consulta; um cadastro não atualiza essa lista automaticamente.

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
gravar no backend, nem Atualizar lista sem autorização para consultar registros.
Campos vazios são identificados localmente; validações de CPF,
telefone e e-mail e normalização permanecem no backend. Erros preservam os campos.

Não há repetição automática do POST. Em timeout, falha de comunicação ou resposta
inesperada, confirme a persistência por um meio autorizado antes de reenviar.

A tarefa 3.1 permanece pendente: a consulta integrada ao backend exige autorização
específica e ainda não foi realizada. A tarefa 3.2 também permanece pendente de
verificação integrada autorizada e aprovação. A listagem foi preparada localmente;
a consulta individual, edição e exclusão não estão implementadas nesta interface.
A tarefa 3.3 permanece pendente, inclusive pela consulta individual ainda exigida.
