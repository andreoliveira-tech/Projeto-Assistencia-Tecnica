# Design

## Context

O projeto é um Sistema de Assistência Técnica desenvolvido para fins acadêmicos.

Conforme definido em `proposal.md`, a primeira Change implementará exclusivamente o gerenciamento de clientes.

O modelo de domínio está documentado em `docs/domain-model.md`, e os comportamentos esperados estão especificados em `specs/cadastro-clientes/spec.md`.

A arquitetura estabelecida utiliza Xano como backend, APIs para comunicação e Python com Streamlit como frontend exclusivo.

## Goals / Non-Goals

**Goals:**

- Implementar a persistência dos dados de clientes no Xano.
- Disponibilizar operações de cadastro, consulta, atualização e exclusão por APIs.
- Desenvolver uma interface Streamlit para executar essas operações.
- Manter a separação entre frontend e backend.
- Preservar a integridade dos relacionamentos definidos no modelo de domínio.
- Permitir a verificação individual das funcionalidades implementadas.
- Preparar a estrutura mínima de Equipamento e seu vínculo obrigatório com Cliente como dependência da tarefa 2.5, sem implementar o gerenciamento de equipamentos.

**Non-Goals:**

- Implementar o gerenciamento de equipamentos, técnicos, ordens de serviço ou serviços.
- Desenvolver autenticação ou diferentes perfis de usuários.
- Utilizar frameworks de frontend diferentes do Streamlit.
- Implementar antecipadamente funcionalidades previstas para outras Changes.

A preparação da persistência de Equipamento descrita na decisão 7 é limitada ao suporte da integridade na exclusão de clientes; suas APIs e interface permanecem fora do escopo.

## Decisions

### 1. Persistência de dados no Xano

**Decisão:** utilizar o banco de dados do Xano para armazenar os registros de clientes.

A entidade Cliente seguirá os atributos definidos no modelo de domínio: `id_cliente`, `nome`, `cpf`, `telefone` e `email`.

**Justificativa:** o Xano é a tecnologia de backend estabelecida para o projeto.

**Alternativa considerada:** utilizar um banco de dados local na aplicação Python. Essa alternativa foi descartada por contrariar a arquitetura definida.

### 2. Comunicação por APIs

**Decisão:** disponibilizar as operações de clientes por meio de APIs REST do Xano.

As operações contemplarão criação, listagem, consulta individual, atualização e exclusão de clientes.

**Justificativa:** permitir que o frontend acesse os dados sem realizar operações diretamente no banco.

**Alternativa considerada:** conectar o Streamlit diretamente ao banco de dados. Essa alternativa foi descartada para preservar a separação entre frontend e backend.

### 3. Interface desenvolvida em Streamlit

**Decisão:** implementar a interface de gerenciamento de clientes exclusivamente em Python com Streamlit.

A interface permitirá executar as operações previstas nas especificações e apresentar os resultados retornados pelas APIs.

**Justificativa:** o Streamlit é a tecnologia obrigatória de frontend definida para o projeto acadêmico.

**Alternativa considerada:** desenvolver interfaces em outros frameworks. Essa alternativa foi descartada por estar fora das restrições do projeto.

### 4. Integridade dos relacionamentos

**Decisão:** impedir a exclusão de clientes que possuam equipamentos vinculados.

A verificação será realizada no backend, para que a regra seja respeitada independentemente da interface utilizada, com garantia delimitada às operações sequenciais conforme a decisão 7.

**Justificativa:** preservar o relacionamento entre Cliente e Equipamento definido no modelo de domínio.

**Alternativa considerada:** excluir automaticamente os equipamentos associados. Essa alternativa foi descartada para evitar perda de dados relacionados.

### 5. Validação e normalização dos dados de Cliente

**Decisão:** validar os dados no backend Xano antes de qualquer criação ou atualização de Cliente, independentemente da interface utilizada.

As regras aprovadas para a tarefa 1.3 são:

- `nome`: obrigatório; aplicar `trim` e rejeitar valor vazio após essa operação.
- `cpf`: obrigatório; aceitar com ou sem máscara, normalizar para somente números, exigir exatamente 11 dígitos e validar matematicamente os dois dígitos verificadores.
- `telefone`: obrigatório; aceitar com ou sem máscara, normalizar para somente números e exigir DDD e um total de 10 ou 11 dígitos.
- `email`: obrigatório e com formato válido; utilizar a validação nativa do tipo `email` do Xano, preservando os filtros existentes `trim` e `lower`.

CPF e telefone serão armazenados como texto contendo somente números, para preservar zeros à esquerda. A normalização removerá a máscara antes da validação; ela não substituirá a verificação de validade dos dados.

As APIs de cadastro e atualização deverão aplicar as mesmas regras, utilizando os filtros declarativos do Xano e verificações adicionais para o cálculo dos dígitos verificadores do CPF. Todas as verificações deverão terminar antes da operação de persistência. Uma solicitação inválida deverá retornar um erro compreensível sem criar registros ou alterar qualquer campo de um registro existente, mesmo que outros campos enviados sejam válidos.

**Justificativa:** garantir consistência dos dados e cumprir a rejeição sem persistência prevista na tarefa 1.3, mantendo uma implementação simples no backend definido para o projeto.

**Verificação:** cobrir campos obrigatórios ausentes ou nulos no cadastro, valores vazios, nome composto apenas por espaços, CPF com quantidade de dígitos ou dígitos verificadores inválidos, telefone sem DDD ou com quantidade de dígitos inválida e e-mail com formato inválido. Verificar também cadastro e atualização válidos com e sem máscara, incluindo preservação de zeros à esquerda. Para cada cadastro rejeitado, confirmar que nenhum registro foi criado; para cada atualização rejeitada, confirmar que todos os dados anteriores permaneceram inalterados.

Essas decisões não acrescentam unicidade de CPF ou e-mail, consultas externas de CPF, confirmação de e-mail, autenticação ou novas entidades ao escopo da Change.

### 6. Mapeamento do identificador de Cliente

**Decisão:** utilizar o campo físico `id`, gerado pelo Xano, para representar o atributo conceitual `id_cliente` nas APIs.

O cadastro não exigirá que o usuário forneça o identificador. As APIs apresentarão esse identificador como `id_cliente` e o utilizarão para identificar o cliente nas operações correspondentes. A atualização dos dados não alterará o identificador. Não será criado um segundo campo de identificação na tabela apenas para reproduzir o nome conceitual.

**Justificativa:** manter a identificação nativa do Xano e a correspondência com o modelo de domínio sem duplicação de atributos.

### 7. Preparação mínima de Equipamento para a exclusão de clientes

**Decisão:** preparar a tabela física `equipamento`, com os atributos já previstos no modelo de domínio, antes de implementar a tarefa 2.5. Na análise inicial do workspace 149143, branch `v1`, foi identificada a ausência dessa tabela, motivando sua preparação na tarefa 1.5. Conforme registrado em `tasks.md`, a preparação estrutural, a decisão técnica da 1.4 e a verificação da 1.6 foram concluídas em seus respectivos escopos. As dependências da 2.5 foram atendidas; sua implementação e verificações foram concluídas posteriormente, conforme evidências e limitações registradas na seção da tarefa 2.5. A existência da estrutura não substitui a verificação real de vínculos antes da exclusão.

| Atributo conceitual | Campo físico | Tipo e representação |
| --- | --- | --- |
| `id_equipamento` | `id` | Inteiro gerado pelo Xano, chave primária; sem segundo identificador |
| `tipo` | `tipo` | Texto obrigatório e não nulo |
| `marca` | `marca` | Texto opcional e anulável |
| `modelo` | `modelo` | Texto opcional e anulável |
| `numero_serie` | `numero_serie` | Texto opcional e anulável, preservando letras e zeros à esquerda |
| `id_cliente` | `id_cliente` | Referência inteira obrigatória e não nula a `cliente.id` |

O relacionamento será Cliente 1:N Equipamento: cada equipamento pertence a exatamente um cliente existente, e um cliente pode possuir vários equipamentos. A garantia técnica desta Change aplica-se às operações sequenciais, exigindo cliente existente antes de criar ou alterar vínculos; a limitação concorrente aceita está registrada abaixo. Não será adicionado campo ou lista de equipamentos à tabela `cliente`. Um índice não exclusivo em `equipamento.id_cliente` apoiará a consulta de vínculos; ele não representa unicidade do proprietário entre equipamentos.

A exclusão consultará a existência de equipamentos com `equipamento.id_cliente` igual ao `id` físico do cliente solicitado. Havendo qualquer vínculo, deverá interromper a operação antes da exclusão e informar o bloqueio, preservando cliente e equipamentos. A exclusão em cascata permanece descartada conforme a decisão 4. Uma falha na verificação de vínculos não deverá ser interpretada como ausência de equipamentos.

**Decisões de campos aprovadas:** a obrigatoriedade e a nulabilidade da tabela acima foram aprovadas pelo responsável pelo projeto. Não acrescentam exigência de conteúdo não vazio após `trim`, formatos, tamanhos ou unicidade de número de série.

**Separação da preparação estrutural:** a tarefa 1.5 pôde preparar somente a estrutura mínima aprovada, incluindo a referência a `cliente.id` e o índice não exclusivo, antes da conclusão integral da 1.4. Essa preparação, isoladamente, não implementou nem comprovou as verificações de integridade sequencial. A tarefa 1.4 está concluída documentalmente, e as verificações da 1.6 foram concluídas nos cenários sequenciais registrados abaixo. A implementação da 2.5 mantém suas dependências de 1.4, 1.5 e 1.6, agora atendidas. Isso não autoriza iniciar implementação ou publicação sem autorização específica.

**Resposta do suporte e limites técnicos:** conforme resposta do suporte oficial Xano relatada pelo responsável pelo projeto, XanoScript não oferece bloqueio explícito de registros, isolamento serializable ou restrição referencial nativa equivalente a `ON DELETE RESTRICT`. A validação sintática em memória também rejeitou `isolation = "serializable"`; essa propriedade não deverá ser usada. A opção visual de bloqueio descrita em materiais anteriores não será presumida como disponível em XanoScript. A declaração `table = "cliente"` representa o relacionamento, sem comprovar por si só sua imposição como restrição física.

**Estratégia suportada:** as funções internas foram implementadas e verificadas mediante autorizações específicas na tarefa 1.6; a aplicação ao endpoint de exclusão foi implementada e verificada posteriormente na 2.5, conforme evidências e limitações registradas abaixo.

1. Antes de criar um equipamento ou alterar seu proprietário, exigir `id_cliente` não nulo e consultar `cliente.id`. Rejeitar a solicitação se o cliente não existir ou se a verificação falhar, antes de qualquer gravação. O registro dessa estratégia não amplia o escopo para APIs de equipamentos.
2. Antes da exclusão, consultar o cliente e verificar a existência de registros em `equipamento` cujo `id_cliente` corresponda a seu `id`. Bloquear se houver qualquer vínculo ou se a consulta falhar. Somente permitir a exclusão após uma verificação bem-sucedida sem vínculos.
3. Não atribuir à transação comum garantia de serialização ou de integridade referencial concorrente. As verificações de existência e a operação posterior não constituem, por si só, uma operação indivisível frente a outros fluxos.

**Limitação concorrente aceita para o escopo atual:** um fluxo pode confirmar que o cliente existe, outro confirmar que não há equipamentos, e as gravações subsequentes criarem um equipamento e excluírem o cliente, produzindo vínculo órfão. As verificações prévias não garantem integridade sob operações concorrentes. O responsável pelo projeto aprovou delimitar a garantia desta Change às operações sequenciais, aceitando expressamente essa limitação; ela não foi tecnicamente resolvida. Não foi encontrada evidência documental de exigência expressa de proteção concorrente pelo professor. Caso apareça requisito acadêmico contrário, esta decisão deverá ser reavaliada.

**Estado de atendimento:** permanecem obrigatórias, em operações sequenciais, a exigência de `id_cliente` válido e cliente existente antes de criar ou alterar vínculos, a cardinalidade 1:N, a exclusão permitida sem vínculos, o bloqueio com vínculos, a interrupção em falhas de consulta e a proibição de cascata. A tarefa 1.4 está concluída documentalmente. A implementação interna e os cenários da 1.6 foram autorizados, executados e aprovados separadamente, conforme registro abaixo. A garantia concorrente não é critério de conclusão desta Change. O endpoint DELETE foi concluído na 2.5: bloqueio e exclusão permitida foram verificados no Xano; a falha de consulta foi verificada por inspeção do XanoScript e simulação Python local, sem teste integrado dessa falha no runtime Xano. Novas implementações exigem autorização específica.

**Limites:** não criar APIs ou interface de equipamentos, novas entidades, atributos adicionais, nem antecipar o relacionamento físico com Ordem de Serviço. Esse relacionamento continua previsto no modelo global para evolução futura. A preparação não altera as regras existentes de Cliente nem exige mudanças em `docs/domain-model.md`.

**Verificação:** a conferência estrutural e os cenários sequenciais da tarefa 1.6 foram concluídos e registrados abaixo. A tarefa 2.5 também foi concluída, com comprovação integrada da exclusão sem vínculos e do bloqueio com equipamentos, preservando os registros envolvidos no bloqueio; a interrupção em falha de consulta possui evidência por inspeção e simulação local, com os limites explicitados na seção da 2.5.

### Evidências da tarefa 1.6 — conclusão em 26/10/2026

Registro consolidado das execuções autorizadas e aprovadas nesta conversa, no workspace **149143**, branch **v1**, datasource **live**, rodada `T16-dcd98500-df59-4dfd-ac7e-1fb7e781f633`. Esta consolidação documental não executou novamente os testes.

**Inspeções estruturais:** os GETs de metadados confirmaram `cliente` (tabela 906835) e `equipamento` (908125), chave primária `id`, tipos e nulabilidade da tabela acima, referência obrigatória e não nula `equipamento.id_cliente` a `cliente.id` e índice não exclusivo no vínculo. A referência declarada não é apresentada como prova de restrição física ou de integridade concorrente. As persistências e consultas dos cenários A/B confirmaram campos e tipos dos registros, inclusive os campos opcionais nulos, sem identificador duplicado.

**Funções publicadas e inspecionadas:** `equipamentos/validar_cliente` (355571), `clientes/consultar_dependencias` (355572, versão `2026-10-26 03:22:11+0000`) e `investigacao/tarefa_1_6_equipamento` (353784, versão `2026-10-26 03:27:53+0000`). As definições foram conferidas por GET, sem draft; as funções de validação e dependências estavam com cache desativado. Todos os caminhos de persistência do procedimento controlado chamam a validação antes de gravar. Não foram criados endpoints públicos nem interface de equipamentos.

**Resultados funcionais:** cada cenário abaixo utilizou uma única chamada ao executor com trace, precedida de GETs de pré-condições e seguida das consultas de persistência autorizadas. O HTTP 200 do executor foi distinguido do resultado funcional.

| Cenário | Resultado funcional e evidência | Conferência de persistência |
| --- | --- | --- |
| OMITIDO | HTTP 200, `status: exception`, `ERROR_CODE_INPUT_ERROR`, `Param: id_cliente - Missing param: id_cliente`. Trace: chamada da validação sem parâmetro, antes de `db.add`. | Zero equipamentos antes/depois; marcador `-OMITIDO` ausente. |
| NULO | HTTP 200, `status: exception`, mesma mensagem de parâmetro ausente. Trace: `id_cliente = null` rejeitado na entrada da validação, sem executar seu stack ou persistir. | Zero equipamentos antes/depois; marcador `-NULO` ausente. |
| INEXISTENTE | ID 2 previamente confirmado por HTTP 404. Executor HTTP 200, `status: exception`, `Param:  - Cliente nao encontrado para o vinculo.` Trace: consulta do ID 2 retornou nulo e a precondição de existência rejeitou antes de `db.add`. | Zero equipamentos antes/depois; marcador `-INEXISTENTE` ausente. |
| A | HTTP 200, `status: ok`; duas validações do cliente 11 antes do único `db.add`. Equipamento ID 1 criado com marcador `-A`, vinculado ao cliente 11. | GET individual e todas as páginas confirmaram exatamente um equipamento, campos/tipos esperados e cliente 11 preservado. |
| B | HTTP 200, `status: ok`; duas validações do cliente 11 antes do único `db.add`. Equipamento ID 2 criado com marcador `-B`, vinculado ao cliente 11. | Exatamente dois equipamentos, marcadores A/B únicos, ambos com `id_cliente = 11`; ID 1 e cliente 11 preservados. Comprovada a cardinalidade 1:N. |
| ALTERAR | HTTP 200, `status: ok`; destino 12 validado antes do único `db.edit` do equipamento 1, sem `db.add`. | Somente `id_cliente` do ID 1 mudou de 11 para 12; demais campos/tipos, equipamento 2 e clientes 11/12 preservados. Mesmos dois equipamentos. |

O Xano normalizou a chamada com `input = {}` no cenário OMITIDO para chamada sem bloco de entrada. A rejeição funcional comprovou a omissão do parâmetro; não foi necessária republicação. No cenário INEXISTENTE, o prefixo `Param:  -` fez uma comparação auxiliar estrita indicar inicialmente resultado inconclusivo; a análise do trace comprovou a rejeição de existência e o cenário foi aprovado, sem repetição.

**Consulta de dependências comprovada:** duas execuções individuais da função 355572 retornaram HTTP 200, `status: ok`, trace completo e sem exceções:

| Cliente | Pré-condição conferida por GET | Resposta |
| --- | --- | --- |
| 11, fictício ORIGEM | Equipamento 2 com `id_cliente = 11`. | `id_cliente: 11`, `possui_equipamentos: true`, `bloqueia_exclusao: true` |
| 9, fictício de teste | Cliente existente e nenhum vínculo, conferindo todas as páginas de equipamentos. | `id_cliente: 9`, `possui_equipamentos: false`, `bloqueia_exclusao: false` |

Os traces mostraram a validação de existência do cliente e `db.has equipamento` pelo vínculo real, sem operações de gravação ou exclusão. A resposta indica a decisão de bloqueio; não demonstra a aplicação dessa decisão por um endpoint DELETE.

**Limites da comprovação:** a integridade foi comprovada nos cenários sequenciais testados, sem garantia de concorrência. A interrupção diante de falha de consulta foi inspecionada no código, que propaga erros sem substituí-los por ausência de vínculos; não foi executado teste de indisponibilidade do banco. Na conclusão da 1.6, o bloqueio efetivo do DELETE, a exclusão sem vínculos e o tratamento de falha nesse endpoint foram reservados à tarefa 2.5, cujas evidências posteriores estão registradas abaixo. A conclusão da 1.6, isoladamente, não implementou nem concluiu a exclusão e não autorizou novas operações ou limpeza dos registros fictícios.

**Estado ao final dos testes:** clientes fictícios ORIGEM 11 e DESTINO 12 preservados; equipamento 1 (`-A`) vinculado ao cliente 12 e equipamento 2 (`-B`) vinculado ao cliente 11. O cliente fictício 9 permaneceu sem equipamentos. Os registros não foram removidos; eventual limpeza exige autorização própria.

### Evidências da tarefa 2.5 — conclusão em 26/10/2026

Consolidação das operações e verificações previamente autorizadas e aprovadas nesta conversa; esta revisão documental não executou novos testes ou chamadas de rede. Ambiente: workspace **149143**, grupo **Clientes 436987**, branch **v1**, datasource **live**.

**Implementação e inspeção do publicado:** endpoint **4107955**, `DELETE /clientes/{id_cliente}`, versão `2026-10-26 04:30:46+0000`, cache desativado e sem draft. A sintaxe foi validada antes da criação. Os GETs confirmaram entrada `id_cliente` inteira, obrigatória e não nula, validação de identificador positivo, consulta de existência com erro `notfound`, chamada de `clientes/consultar_dependencias`, conferência do retorno e bloqueio por equipamentos antes do único `db.del cliente`. Não há operações diretas sobre Equipamento nem cascata; a resposta de sucesso vem após a exclusão. As quatro APIs anteriores permaneceram integralmente inalteradas. O Xano apenas normalizou espaços e o objeto `response` para uma linha com vírgula, mantendo o conteúdo aprovado.

**Testes integrados aprovados:** cada cenário utilizou uma única tentativa de DELETE, sem repetição, correção ou recuperação automática. Os GETs posteriores compararam identificadores, campos, valores e tipos com o baseline; todas as páginas de equipamentos foram conferidas.

| Cenário | HTTP e resposta | Evidências posteriores |
| --- | --- | --- |
| Cliente fictício 11 com equipamento 2 vinculado | HTTP 400; `ERROR_CODE_INPUT_ERROR`; `Cliente possui equipamentos vinculados. Exclusao bloqueada.` | Oito clientes e dois equipamentos integralmente preservados. Equipamento 2 permaneceu com cliente 11; equipamento 1 com cliente 12. |
| Cliente inexistente 2, previamente confirmado ausente | HTTP 404; `ERROR_CODE_NOT_FOUND`; `Cliente nao encontrado.` | Mesmos oito clientes e dois equipamentos, sem divergência em campos, valores ou tipos. |
| Cliente fictício 9 sem equipamentos, previamente conferido | HTTP 200; `{"id_cliente":9,"excluido":true}` | GET individual retornou HTTP 404. Restaram sete clientes, IDs 1, 3, 7, 8, 10, 11 e 12, integralmente preservados. Equipamentos 1 e 2 inalterados, sem cascata. |

**Falha de consulta — inspeção e simulação local, não teste integrado no runtime Xano:** a inspeção do XanoScript confirmou que a consulta de dependências antecede o único `db.del cliente`, sem captura de exceção, continuação em erro ou resposta de sucesso anterior à exclusão. Um modelo restrito dessa sequência em Python, executado somente em memória com rede bloqueada, substituiu a consulta por uma exceção controlada e a exclusão por um registrador sem capacidade de gravação. A consulta foi chamada uma vez, a exceção foi propagada, o registrador de exclusão teve **zero chamadas**, nenhuma resposta de sucesso foi produzida e os dados em memória foram preservados. Houve zero tentativas de rede e nenhum arquivo de teste foi criado.

Essa simulação não interpretou XanoScript, não executou o endpoint e não comprovou a semântica dessa falha no runtime Xano. A evidência aceita para esse critério combina inspeção do código publicado com simulação local; não se registra um teste integrado de indisponibilidade ou falha do banco. Respostas inconsistentes da função são protegidas pelas precondições inspecionadas, sem atribuir a elas teste integrado específico.

**Conclusão e limites:** a tarefa 2.5 está concluída com implementação, três testes integrados e evidência local de interrupção em falha de consulta, nos alcances acima discriminados. A proteção de exclusão permanece limitada às operações sequenciais; não oferece garantia concorrente. A tarefa 3.5 (exclusão na interface) e a cobertura restante da 3.6 não são concluídas por este registro.

**Estado final conhecido:** cliente fictício 9 excluído; sete clientes restantes; equipamento 1, marcador A da rodada T16, vinculado ao cliente 12; equipamento 2, marcador B, vinculado ao cliente 11. Nenhum equipamento foi excluído. Novas operações e eventual limpeza dependem de autorização específica.

## Risks / Trade-offs

- **[Indisponibilidade do Xano]** → Apresentar mensagens de erro na interface e permitir nova tentativa.
- **[Falhas de comunicação entre Streamlit e Xano]** → Tratar respostas de erro das APIs e informar o usuário.
- **[Dados inválidos]** → Validar as entradas no backend antes de persistir alterações.
- **[Exclusão de clientes com equipamentos associados]** → Aplicar a verificação de integridade no backend.
- **[Criação de vínculo concorrente à exclusão]** → As verificações prévias não eliminam a condição de corrida; limitação aceita para o escopo sequencial desta Change conforme a decisão 7. Não declarar garantia concorrente com base em verificações sequenciais; reavaliar a decisão se aparecer requisito acadêmico contrário.
- **[Complexidade excessiva para o projeto acadêmico]** → Manter a implementação limitada ao cadastro de clientes.

## Migration Plan

1. Configurar a estrutura de dados da entidade Cliente no Xano.
   Antes da etapa 2, especificamente da API de exclusão, resolver as decisões pendentes da decisão 7 e preparar e verificar a tabela `equipamento` e sua referência obrigatória a `cliente.id`, preservando os recursos e dados existentes.
2. Criar e verificar as APIs de gerenciamento de clientes.
3. Implementar a interface Streamlit que consome essas APIs.
4. Testar os cenários descritos nas especificações.
5. Versionar os arquivos correspondentes no Git/GitHub.

**Antecipação limitada da interface para demonstração acadêmica:** a etapa 3 pode iniciar parcialmente após a disponibilização das APIs de cadastro e listagem, antes da conclusão integral das etapas anteriores. A entrega antecipada compreende a estrutura e configuração da tarefa 3.1, o formulário de cadastro da 3.2, somente a listagem da 3.3 e o tratamento de falhas desses fluxos da 3.6. A tela será desenvolvida exclusivamente em Python com Streamlit, consumindo `POST /clientes` e `GET /clientes` existentes, sem acesso direto ao banco ou uso da Metadata API. As validações e a normalização de Cliente permanecem no backend conforme a decisão 5.

A consulta individual continua necessária para concluir a tarefa 3.3; o tratamento de falhas dos demais fluxos continua exigido pela 3.6. A edição e a exclusão da interface permanecem fora dessa entrega antecipada. As tarefas 1.4, 1.6 e 2.5 estão concluídas em seus respectivos escopos; a tarefa 1.3 continua pendente, sem dispensa dos requisitos sequenciais, verificações ou dependências. A limitação concorrente descrita na decisão 7 foi aceita para o escopo atual, sem solução técnica; as dependências e verificações da 2.5 foram atendidas no alcance registrado, e a 3.5 permanece pendente de implementação e verificação da exclusão na interface, mediante autorização específica.

A antecipação é uma mudança de sequência para uma entrega parcial, sem reduzir o escopo final da Change ou os critérios das tarefas. Este registro autoriza somente o ajuste documental; a implementação da interface requer autorização específica. As verificações locais poderão utilizar respostas simuladas, sem substituir a verificação integrada exigida pelas tarefas; qualquer consulta ou gravação nas APIs do Xano durante testes também depende de autorização específica.

**Rollback:** caso a implementação apresente problemas, utilizar o histórico do Git para recuperar os arquivos versionados e reverter separadamente as alterações necessárias no Xano, preservando os dados existentes.
