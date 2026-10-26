# API de clientes

Documentação da tarefa 2.6 da Change `mvp-assistencia-tecnica`.

## Ambiente e alcance das evidências

Conferência do contrato da tarefa 2.6 realizada em **26/10/2026**, exclusivamente por leitura de metadados e definições. As confirmações posteriores de URL, envelope de erro e o teste integrado da interface estão identificados separadamente neste documento e em `docs/validacao-mvp-clientes.md`.

| Identificação | Valor |
| --- | --- |
| Instância | `x8ki-letl-twmt.n7.xano.io` |
| Workspace | `149143` |
| Branch | `v1` |
| Grupo | `Clientes`, ID `436987` |
| Canonical local e posteriormente confirmado por metadados | `assistencia-tecnica-clientes` |

A associação do grupo ao workspace e à branch foi confirmada pela listagem de grupos com `branch=v1`, que retornou o ID `436987`, nome `Clientes` e branch `v1`. A listagem de endpoints desse grupo retornou os cinco endpoints abaixo, sem próxima página. Cada definição individual foi consultada com `include_draft=false&include_xanoscript=true`; todos os XanoScripts retornaram `status: "ok"`.

### URL base de consumo

A URL base confirmada é:

```text
https://x8ki-letl-twmt.n7.xano.io/api:assistencia-tecnica-clientes
```

**Evidência funcional anterior informada pelo responsável pelo projeto:** durante a preparação do ambiente no computador da empresa, o frontend Streamlit consumiu com sucesso `https://x8ki-letl-twmt.n7.xano.io/api:assistencia-tecnica-clientes` e apresentou uma listagem de sete clientes. Esse resultado anterior não foi reproduzido na conferência da tarefa 2.6.

**Confirmação formal posterior:** GETs de metadados do grupo `436987` e da branch `v1` no workspace `149143` retornaram `canonical: "assistencia-tecnica-clientes"`, `branch: "v1"` e `label: "v1", live: true`. Conforme a regra oficial do Xano, a URL sem sufixo de branch atende à branch live; portanto, a URL acima atendia a `v1` no momento da conferência. Essa associação pode mudar se outra branch for colocada live. As rotas deste documento são relativas à URL base do grupo.

Não usar a URL da Metadata API (`/api:meta`), de documentação (`apispec`) ou o caminho final `/clientes` como URL base do frontend.

## Endpoints

| Operação | Método | Rota relativa | ID no Xano |
| --- | --- | --- | --- |
| Cadastro | POST | `/clientes` | `4099966` |
| Listagem | GET | `/clientes` | `4100486` |
| Consulta individual | GET | `/clientes/{id_cliente}` | `4100487` |
| Atualização | PUT | `/clientes/{id_cliente}` | `4100488` |
| Exclusão | DELETE | `/clientes/{id_cliente}` | `4107955` |

Os cinco endpoints retornaram `auth: false`. Não exigem autenticação de usuário segundo os metadados consultados. O Bearer token usado na conferência pertence à Metadata API e não deve ser enviado pelo frontend às APIs de clientes.

## Entradas e formato comum de Cliente

| Campo de entrada | Tipo Xano | Uso | Obrigatório | Aceita null |
| --- | --- | --- | --- | --- |
| `id_cliente` | `int` | Caminho do GET individual, PUT e DELETE | Sim | Não |
| `nome` | `text` | Corpo do POST e PUT | Sim | Não |
| `cpf` | `text` | Corpo do POST e PUT | Sim | Não |
| `telefone` | `text` | Corpo do POST e PUT | Sim | Não |
| `email` | `email` | Corpo do POST e PUT | Sim | Não |

O cadastro não recebe identificador. O campo físico `cliente.id` é apresentado como `id_cliente`. O PUT utiliza esse identificador para localizar o cliente e não o altera. Enviar os quatro campos no PUT; não se trata de atualização parcial.

Os retornos de cadastro, consulta individual e atualização são objetos com os campos abaixo. A listagem retorna uma lista desses objetos.

| Campo de resposta | Representação |
| --- | --- |
| `id_cliente` | Identificador inteiro gerado pelo Xano |
| `nome` | Texto |
| `cpf` | Texto; não converter em número |
| `telefone` | Texto; não converter em número |
| `email` | Texto de e-mail |

Os exemplos seguintes são fictícios e ilustrativos, não resultados de chamadas. O CPF foi escolhido apenas para demonstração sintática e matemática; não indica consulta ou comprovação de identidade.

## Cadastro — POST /clientes

Enviar corpo JSON com os quatro campos obrigatórios e `Content-Type: application/json`:

```json
{
  "nome": "Cliente Fictício de Documentação",
  "cpf": "529.982.247-25",
  "telefone": "(11) 90000-0000",
  "email": "cliente@example.invalid"
}
```

O XanoScript confirmado chama `clientes/validar_dados` antes de `db.add cliente` e utiliza os dados retornados pela função. Exemplo de estrutura de sucesso, considerando a normalização descrita no código local da função:

```json
{
  "id_cliente": 1001,
  "nome": "Cliente Fictício de Documentação",
  "cpf": "52998224725",
  "telefone": "11900000000",
  "email": "cliente@example.invalid"
}
```

Na conferência de contrato da 2.6 não houve execução do POST. Posteriormente, o teste integrado autorizado da interface retornou HTTP 200 ao criar exclusivamente o cliente descartável 13. O envelope completo de rejeição de cadastro não foi verificado por esse teste válido.

## Listagem — GET /clientes

Não possui parâmetros de entrada declarados ou corpo de requisição. O XanoScript consulta a tabela e mapeia os cinco campos de Cliente. Não declara paginação ou ordenação para o consumidor; não assumir uma ordem estável.

Exemplo de estrutura de resposta:

```json
[
  {
    "id_cliente": 1001,
    "nome": "Cliente Fictício de Documentação",
    "cpf": "52998224725",
    "telefone": "11900000000",
    "email": "cliente@example.invalid"
  }
]
```

A representação de uma lista sem registros é `[]`, conforme a estrutura de lista definida; esse cenário foi simulado localmente, sem esvaziar o banco. A listagem retornou HTTP 200 no teste integrado posterior da interface. Não foi provocado um erro real de listagem.

## Consulta individual — GET /clientes/{id_cliente}

Exemplo de rota: `/clientes/1001`. Enviar o identificador no caminho, sem corpo de requisição.

A definição consulta `cliente.id` e retorna o objeto Cliente apresentado no exemplo de cadastro. Se não encontrar o registro, declara erro `notfound` com a mensagem `Cliente não encontrado.`.

Posteriormente, um GET de leitura ao cliente inexistente 2 confirmou HTTP 404 e os campos JSON `code`, `message` e `payload`, com `code: "ERROR_CODE_NOT_FOUND"` e `message: "Cliente não encontrado."`. O valor de `payload` não foi exibido nem é presumido aqui. No teste integrado de exclusão do cliente descartável 13, o GET inicial retornou 200 e o GET posterior retornou 404 reconhecido pela validação estrita do frontend.

O parâmetro é inteiro, obrigatório e não nulo. O XanoScript deste endpoint não contém a precondição explícita `id_cliente > 0` presente no DELETE. A interface pode exigir inteiro positivo, mas essa validação local não deve ser atribuída a esta definição de backend.

## Atualização — PUT /clientes/{id_cliente}

Exemplo de rota: `/clientes/1001`. Enviar `Content-Type: application/json` e os quatro campos obrigatórios:

```json
{
  "nome": "Cliente Fictício Atualizado",
  "cpf": "52998224725",
  "telefone": "11900000000",
  "email": "atualizado@example.invalid"
}
```

A definição verifica a existência do cliente, chama `clientes/validar_dados` e somente depois executa `db.edit`. Retorna o objeto Cliente com os dados atualizados:

```json
{
  "id_cliente": 1001,
  "nome": "Cliente Fictício Atualizado",
  "cpf": "52998224725",
  "telefone": "11900000000",
  "email": "atualizado@example.invalid"
}
```

Cliente ausente gera declaração `notfound` com `Cliente não encontrado.`. Assim como no GET individual, não há precondição explícita de identificador positivo. Não foram testados nesta etapa persistência, códigos HTTP ou respostas de falha do PUT.

## Exclusão — DELETE /clientes/{id_cliente}

Exemplo de rota: `/clientes/1001`. O identificador é passado no caminho; não há corpo de requisição declarado.

A sequência confirmada no XanoScript é:

1. Exigir `id_cliente > 0`.
2. Consultar a existência do cliente.
3. Chamar `clientes/consultar_dependencias` com o identificador encontrado.
4. Exigir retorno não nulo e correspondente ao mesmo cliente.
5. Exigir simultaneamente `bloqueia_exclusao == false` e `possui_equipamentos == false`.
6. Executar o único `db.del cliente` e, depois, retornar sucesso.

Exemplo fictício de resposta:

```json
{
  "id_cliente": 1001,
  "excluido": true
}
```

O endpoint não contém exclusão de equipamentos nem cascata. A função auxiliar é responsável por consultar os vínculos reais em `equipamento.id_cliente`, conforme o design e as evidências anteriores; seu conteúdo remoto não foi consultado nesta etapa. Não há captura de exceção que permita continuar após falha da função. Isso é evidência de inspeção, não teste de falha no runtime.

A regra de negócio impede excluir cliente com equipamentos vinculados e permite excluir aquele sem vínculos após verificação bem-sucedida. A garantia aprovada limita-se a operações sequenciais: verificações prévias não eliminam condições de corrida com criação ou alteração simultânea de equipamentos.

## Validações e erros: origem das evidências

### Confirmados nas definições remotas dos endpoints

Além dos tipos, obrigatoriedade e nulabilidade da tabela de entradas, foram confirmadas estas declarações:

| Endpoint | Tipo declarado | Mensagem exata |
| --- | --- | --- |
| GET individual e PUT | `notfound` | `Cliente não encontrado.` |
| DELETE | `inputerror` | `Informe um identificador inteiro positivo.` |
| DELETE | `notfound` | `Cliente nao encontrado.` |
| DELETE | `inputerror` | `Nao foi possivel confirmar os vinculos do cliente.` |
| DELETE | `inputerror` | `Cliente possui equipamentos vinculados. Exclusao bloqueada.` |

As diferenças de acentuação acima correspondem às definições consultadas. Essas declarações não constituem, por si só, verificação dos status HTTP e do JSON completo de erro produzidos pelo runtime.

### Regras presentes no código local e nas decisões do projeto

O arquivo local `xano/function/clientes/validar_dados.xs` e o design descrevem:

- Nome com `trim` e mínimo de um caractere.
- CPF textual com remoção de espaços, pontos e hífens de máscara; exigência de 11 dígitos, rejeição de dígitos todos iguais e cálculo dos dois verificadores.
- Telefone textual com remoção de espaços, parênteses e hífens; exigência de 10 ou 11 dígitos. O design descreve esses valores como incluindo DDD; o código local não consulta validade ou atribuição de DDD.
- E-mail com tipo nativo `email` e filtros `trim` e `lower`.
- Validação antes da persistência, preservando zeros à esquerda em CPF e telefone.

Não se acrescentam unicidade de CPF/e-mail, consulta externa de CPF, confirmação de e-mail ou formatos adicionais. O conteúdo remoto dessa função não foi inspecionado; a chamada a ela foi confirmada nos endpoints POST e PUT. Não se pode afirmar, com esta conferência, que sua versão remota é idêntica à local ou que todos os cenários foram testados. A tarefa 1.3 permanece pendente nos artefatos da Change.

O código local declara erros `inputerror` para quantidade de dígitos de CPF/telefone, CPF com todos os dígitos iguais e verificadores incorretos. Mensagens nativas de obrigatoriedade e do tipo `email`, seus envelopes e códigos HTTP não foram capturados nesta etapa.

### Códigos HTTP comprovados em testes anteriores

O design da Change, seção de evidências da tarefa 2.5 em 26/10/2026, registra os seguintes testes integrados anteriores do DELETE:

| Cenário | HTTP registrado | Resultado registrado |
| --- | --- | --- |
| Cliente com equipamento vinculado | 400 | `ERROR_CODE_INPUT_ERROR`; mensagem de bloqueio da tabela acima |
| Cliente inexistente | 404 | `ERROR_CODE_NOT_FOUND`; `Cliente nao encontrado.` |
| Cliente sem equipamentos | 200 | Objeto com `id_cliente` e `excluido: true`; GET posterior confirmou ausência |

Os testes anteriores da 2.5 não foram repetidos sobre seus registros. Posteriormente, a interface criou e excluiu exclusivamente o cliente descartável 13, com POST 200, GET 200, DELETE 200 e GET posterior 404; a listagem inicial e final retornou 200 e preservou os sete clientes preexistentes nos campos expostos pela API. A apresentação do bloqueio no frontend foi testada localmente com HTTP simulado. A falha de consulta de vínculos mantém evidência anterior por inspeção e simulação Python local, sem teste integrado de indisponibilidade. Não extrapolar esses status para todos os erros dos demais endpoints.

## Configuração do frontend Streamlit

O frontend lê a variável `XANO_CLIENTES_API_BASE_URL` por `frontend/config.py`. No PowerShell, configurar na sessão que iniciará a aplicação:

```powershell
$env:XANO_CLIENTES_API_BASE_URL = "https://x8ki-letl-twmt.n7.xano.io/api:assistencia-tecnica-clientes"
```

A variável contém a URL base de execução, sem o sufixo `/clientes`. O cliente Python acrescenta as rotas. A variável não deve conter credenciais, query string ou fragmento. O carregador remove espaços nas extremidades e barras finais; arquivos `.env` não são carregados.

A evidência funcional anterior no computador da empresa foi complementada pela confirmação formal de `v1` live por metadados e pelo teste integrado posterior da interface. A aceitação do formato pelo carregador, isoladamente, não comprova conectividade nem seleção de ambiente.

O código atual em `frontend/clientes_api.py` implementa cadastro, listagem, consulta individual, atualização e exclusão. A interface exige carregamento e confirmação explícita para excluir, valida a resposta e confere ausência por GET com JSON válido, código exato `ERROR_CODE_NOT_FOUND` e mensagem conhecida `Cliente não encontrado.`. HTTP 408, falhas de comunicação e respostas ambíguas não geram reenvio automático ou falso sucesso. Consulte `docs/validacao-mvp-clientes.md` para o alcance dos testes locais e integrados.

## Limitações e diferenças encontradas

- POST, GET individual e PUT correspondem ao código local em entradas, sequência e resposta, com diferenças de formatação.
- No GET de listagem, o XanoScript remoto representa a expressão `map` em um bloco delimitado por três crases; o arquivo local apresenta a expressão diretamente. Campos e mapeamento coincidem; a equivalência em execução não foi testada nesta conferência.
- O arquivo XanoScript do DELETE não está presente em `xano/api/clientes/`. Sua definição foi confirmada remotamente e comparada com o design, sem criar cópia local.
- `clientes/validar_dados` e `clientes/consultar_dependencias` não foram consultadas remotamente. A existência das chamadas não comprova a implementação interna atual dessas funções.
- Foi utilizado `include_draft=false`; isso não demonstra ausência de drafts. A documentação pública consultada não detalha completamente a representação de versões publicadas e drafts no retorno.
- Os valores `default` dos metadados foram ocultados pelo filtro aprovado e não foram avaliados. O filtro também previa ocultação de possíveis segredos, exemplos e dados pessoais textuais.
- Na conferência de contrato da 2.6, as respostas de sucesso foram extraídas das expressões `response` dos XanoScripts. Os status observados em execuções posteriores estão discriminados acima. Não foram consultados os OpenAPIs individuais dos endpoints.
- Nenhum teste funcional, cadastro, atualização, exclusão ou consulta de registros foi realizado na conferência da tarefa 2.6. Os GETs executados foram somente da Metadata API.
- A evidência anterior do computador da empresa foi complementada pela confirmação formal de `v1` live e pelo teste integrado posterior. A confirmação vale para a configuração observada e não impede futura troca da branch live.

Este documento registra o contrato e suas limitações. A tarefa 2.6 foi aprovada e concluída em etapa anterior; a Change continua com a 1.3 pendente. A documentação não autoriza novas operações.

## Referências

- [Design e evidências da Change](../openspec/changes/mvp-assistencia-tecnica/design.md)
- [Validação posterior do MVP](validacao-mvp-clientes.md)
- [Especificação de cadastro de clientes](../openspec/changes/mvp-assistencia-tecnica/specs/cadastro-clientes/spec.md)
- [Tarefas da Change](../openspec/changes/mvp-assistencia-tecnica/tasks.md)
- [Modelo de domínio](domain-model.md)
- [Configuração e operação do frontend](../frontend/README.md)
- [Grupo Clientes no código local](../xano/api/clientes/clientes.xs)
- [Validação de dados no código local](../xano/function/clientes/validar_dados.xs)
- [Xano: consulta de endpoint por ID](https://docs.xano.com/api-reference/api-group-api/retrieve-a-specific-api-endpoint-by-id)
- [Xano: listagem de endpoints do grupo](https://docs.xano.com/api-reference/api-group-api/retrieve-all-api-endpoints-in-a-group)
- [Xano: listagem de grupos por branch](https://docs.xano.com/api-reference/api-group/retrieve-all-api-groups-in-a-workspace)
