# Contrato proposto da API de Equipamentos

## Estado da implementação

Grupo, endpoints e helper abaixo são **definições locais, não publicadas**. Não há URL de execução ou IDs remotos desses novos recursos confirmados. Nenhum CRUD de Equipamentos foi executado no Xano nesta etapa. A implementação Streamlit é verificada somente com HTTP simulado.

Inventário anterior autorizado em `149143/v1`: sete tabelas, quatro grupos, 22 endpoints e sete funções; tabela `equipamento` 908125 e função `equipamentos/validar_cliente` 355571 existentes, sem APIs de Equipamentos ou tabela de OS. Nesta etapa foram feitos apenas dois GETs técnicos adicionais:

- `/api:meta/workspace/149143/table/908125?branch=v1&include_draft=false&include_xanoscript=true`
- `/api:meta/workspace/149143/function/355571?branch=v1&include_draft=false&include_xanoscript=true`

Ambos retornaram HTTP 200 e XanoScript `status: ok`. Não houve consulta a registros. A tabela corresponde à definição versionada: `id` nativo; tipo textual obrigatório não nulo; marca/modelo/numero_serie opcionais e anuláveis; id_cliente inteiro obrigatório não nulo e índice não exclusivo. A função exige cliente positivo existente e retorna o objeto Cliente com `id` físico; apenas esse ID é usado pelo endpoint, sem expor dados pessoais.

## Rotas propostas

| Método | Rota | Entrada | Retorno esperado |
| --- | --- | --- | --- |
| POST | `/equipamentos` | Cinco campos do corpo | Equipamento com ID gerado |
| GET | `/equipamentos` | Nenhuma | Array de equipamentos, incluindo `[]` |
| GET | `/equipamentos/{id_equipamento}` | ID inteiro no caminho | Equipamento ou erro de ausência |
| PUT | `/equipamentos/{id_equipamento}` | ID e cinco campos do corpo | Equipamento atualizado |
| DELETE | `/equipamentos/{id_equipamento}` | ID, sem corpo | `{id_equipamento, excluido: true}` |

Grupo/canonical propostos: `Equipamentos` / `assistencia-tecnica-equipamentos`. A URL real deve ser conferida após publicação autorizada, inclusive branch live; não derivá-la automaticamente de Clientes.

POST/PUT recebem `tipo` como texto e `id_cliente` como inteiro de cliente existente. Não há regra aprovada de texto mínimo para tipo: texto vazio não é rejeitado localmente. `marca`, `modelo` e `numero_serie` aceitam texto ou null; campos opcionais omitidos na entrada XanoScript devem ser conferidos no runtime. O cliente HTTP envia os três campos explicitamente para não depender de defaults ainda não verificados. Série permanece texto, sem máscara ou unicidade adicional. PUT é completo e não altera o identificador.

Exemplo fictício de corpo:

```json
{"tipo":"Notebook","marca":null,"modelo":"","numero_serie":"000ABC","id_cliente":1001}
```

Exemplo fictício de resposta:

```json
{"id_equipamento":2001,"tipo":"Notebook","marca":null,"modelo":"","numero_serie":"000ABC","id_cliente":1001}
```

Sucesso esperado: HTTP 200. Erro de ausência proposto: HTTP 404, JSON objeto com `code: ERROR_CODE_NOT_FOUND` e `message: Equipamento nao encontrado.`. Bloqueio proposto: HTTP 400, `code: ERROR_CODE_INPUT_ERROR`, `message: Equipamento possui ordens de servico vinculadas. Exclusao bloqueada.`. Esses status/envelopes são **contrato para publicação e simulação**, não execuções observadas dos novos endpoints. Declarações XanoScript `notfound` e `inputerror` precisam de confirmação no runtime; não se inventa um valor de `payload`.

## Exclusão e dependência de OS

Decisão atual aprovada pelo usuário: bloquear equipamento com OS, sem cascata. O DELETE confirma existência, chama `equipamentos/consultar_dependencias`, confere ID e flag de dependência e só depois executa um `db.del equipamento`. Falha da função ou resultado inválido interrompe o procedimento.

O helper local usa o nome físico **provisório** `ordem_servico` e sua referência `id_equipamento`. Essa tabela não está no inventário. Portanto, helper e DELETE **não estão prontos para publicação**, ainda que a sintaxe seja válida. Resolver a vinculação com o schema real é tarefa remota pendente, sem criar OS neste incremento. Não há retorno artificial de `possui_os: false` quando a dependência é desconhecida. A garantia é sequencial e não elimina condições de corrida.

## Interface e configuração

A página `frontend/pages/1_Equipamentos.py` é descoberta pelo Streamlit ao iniciar `frontend/app.py`. Também pode ser iniciada diretamente:

```powershell
.venv/Scripts/python.exe -m streamlit run frontend/pages/1_Equipamentos.py
```

Sem `XANO_EQUIPAMENTOS_API_BASE_URL`, a página informa configuração pendente e não faz HTTP. Após publicação autorizada, configurar essa variável com a URL HTTPS real do grupo, sem credenciais, query ou fragmento. Clientes mantém sua configuração independente. Não executar botões contra um ambiente real sem autorização para a operação correspondente.

Abertura, navegação e reruns não fazem HTTP. Cadastro ocorre apenas no formulário; listar e carregar são explícitos. Edição requer carregamento e compara GET posterior com o PUT. Exclusão requer carregamento e confirmação desmarcada a cada mudança de contexto; consome a seleção antes da tentativa e só confirma sucesso após DELETE válido e GET com o erro exato conhecido do contrato proposto. Um 404 genérico, JSON inválido, presença posterior ou falha não confirma exclusão. 408, timeout e falhas ambíguas de escrita não causam retry. Nova tentativa de edição/exclusão exige novo carregamento; cadastro incerto orienta conferência antes de envio manual. Cancelar não faz HTTP.

Os seletores “Sem valor” distinguem null de texto vazio. O cliente é informado por ID; não se acrescentam consulta de dados pessoais ou filtro por cliente. Estados do módulo de Clientes são preservados.

Os controles de exclusão permanecem indisponíveis por padrão, inclusive com a URL do grupo configurada. `XANO_EQUIPAMENTOS_DELETE_VALIDATED` deve permanecer ausente até que o endpoint DELETE seja publicado e sua validação integrada de bloqueio por OS esteja concluída. Só então poderá ser configurada como `true`. Essa chave operacional não substitui a confirmação e a verificação de integridade no backend.

## Validação e limites

Sete arquivos XanoScript locais passaram pelo validador de sintaxe do Developer MCP, com zero erros/avisos. Isso não verifica existência de tabelas, vínculo de funções no workspace ou execução. A função 355571 e a tabela 908125 não foram alteradas ou duplicadas. Testes locais usam URLs `.invalid`, respostas simuladas e a proteção de sockets/DNS existente; essa proteção em Python não é um firewall universal. Não houve API de negócio real.

Execução anterior: **77 testes locais aprovados**, sendo **28 de Equipamentos** e os **49 anteriores de Clientes**. Após a inclusão do gate explícito de exclusão, a suíte completa passou com **79 testes**: **30 de Equipamentos** e **49 de Clientes**, usando HTTP simulado e rede externa bloqueada. Comando: `.venv/Scripts/python.exe -B -m unittest discover -s frontend/tests -p 'test_*.py' -q`. AppTest verifica o código Streamlit sem navegador ou servidor web real. A primeira implementação detectou que corpo None no POST podia ultrapassar a validação local; isso foi corrigido. A revisão também corrigiu mensagem antiga de sucesso ao trocar de seleção, com teste de regressão específico.

As doze Changes passaram pela validação estrutural estrita do OpenSpec. As onze anteriores, os XanoScripts preexistentes e os testes de Clientes foram preservados por comparação SHA-256. Foram alterados apenas `frontend/config.py` e `frontend/README.md` entre os arquivos anteriores; os demais arquivos deste incremento são novos. Não houve commit, push, publicação ou criação/alteração de recursos do Xano.

As decisões futuras de técnico obrigatório, data de saída manual e valores em reais não pertencem a este módulo e não foram implementadas. O manual externo e seu Apêndice A não foram localizados; sua conformidade não é declarada verificada.

Ver [Change e tarefas](../openspec/changes/adicionar-gestao-equipamentos/tasks.md). Publicação, testes integrados e arquivamento permanecem pendentes.
