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

A verificação será realizada no backend, para que a regra seja respeitada independentemente da interface utilizada.

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

**Decisão:** preparar a tabela física `equipamento`, com os atributos já previstos no modelo de domínio, antes de implementar a tarefa 2.5. A análise do workspace 149143, branch `v1`, identificou que essa tabela ainda não existe; sua criação não será presumida nem substituída por uma verificação que sempre permita excluir.

| Atributo conceitual | Campo físico | Tipo e representação |
| --- | --- | --- |
| `id_equipamento` | `id` | Inteiro gerado pelo Xano, chave primária; sem segundo identificador |
| `tipo` | `tipo` | Texto obrigatório e não nulo |
| `marca` | `marca` | Texto opcional e anulável |
| `modelo` | `modelo` | Texto opcional e anulável |
| `numero_serie` | `numero_serie` | Texto opcional e anulável, preservando letras e zeros à esquerda |
| `id_cliente` | `id_cliente` | Referência inteira obrigatória e não nula a `cliente.id` |

O relacionamento será Cliente 1:N Equipamento: cada equipamento pertence a exatamente um cliente existente, e um cliente pode possuir vários equipamentos. Não será adicionado campo ou lista de equipamentos à tabela `cliente`. Um índice não exclusivo em `equipamento.id_cliente` apoiará a consulta de vínculos; ele não representa unicidade do proprietário entre equipamentos.

A exclusão consultará a existência de equipamentos com `equipamento.id_cliente` igual ao `id` físico do cliente solicitado. Havendo qualquer vínculo, deverá interromper a operação antes da exclusão e informar o bloqueio, preservando cliente e equipamentos. A exclusão em cascata permanece descartada conforme a decisão 4. Uma falha na verificação de vínculos não deverá ser interpretada como ausência de equipamentos.

**Decisões de campos aprovadas:** a obrigatoriedade e a nulabilidade da tabela acima foram aprovadas pelo responsável pelo projeto. Não acrescentam exigência de conteúdo não vazio após `trim`, formatos, tamanhos ou unicidade de número de série.

**Separação da preparação estrutural:** a tarefa 1.5 pode preparar somente a estrutura mínima aprovada, incluindo a referência a `cliente.id` e o índice não exclusivo, antes da conclusão integral da 1.4. Essa preparação não depende da solução ainda pendente de integridade concorrente e não a implementa nem a comprova. A tarefa 1.4 permanece pendente, a verificação integral da 1.6 continua exigida e a implementação da 2.5 permanece condicionada à conclusão das tarefas 1.4, 1.5 e 1.6. A permissão de sequência não autoriza iniciar implementação ou publicação sem autorização específica.

**Resposta do suporte e limites técnicos:** conforme resposta do suporte oficial Xano relatada pelo responsável pelo projeto, XanoScript não oferece bloqueio explícito de registros, isolamento serializable ou restrição referencial nativa equivalente a `ON DELETE RESTRICT`. A validação sintática em memória também rejeitou `isolation = "serializable"`; essa propriedade não deverá ser usada. A opção visual de bloqueio descrita em materiais anteriores não será presumida como disponível em XanoScript. A declaração `table = "cliente"` representa o relacionamento, sem comprovar por si só sua imposição como restrição física.

**Estratégia suportada a implementar somente após autorização:**

1. Antes de criar um equipamento ou alterar seu proprietário, exigir `id_cliente` não nulo e consultar `cliente.id`. Rejeitar a solicitação se o cliente não existir ou se a verificação falhar, antes de qualquer gravação. O registro dessa estratégia não amplia o escopo para APIs de equipamentos.
2. Antes da exclusão, consultar o cliente e verificar a existência de registros em `equipamento` cujo `id_cliente` corresponda a seu `id`. Bloquear se houver qualquer vínculo ou se a consulta falhar. Somente permitir a exclusão após uma verificação bem-sucedida sem vínculos.
3. Não atribuir à transação comum garantia de serialização ou de integridade referencial concorrente. As verificações de existência e a operação posterior não constituem, por si só, uma operação indivisível frente a outros fluxos.

**Limitação de concorrência ainda aberta:** um fluxo pode confirmar que o cliente existe, outro confirmar que não há equipamentos, e as gravações subsequentes criarem um equipamento e excluírem o cliente, produzindo vínculo órfão. A verificação prévia é suportada, mas não elimina essa condição de corrida. Não foi identificada uma solução suportada que demonstre a garantia absoluta exigida para operações concorrentes; não se considera a limitação resolvida ou aceita como exceção aos requisitos.

**Requisito ainda não atendido:** a garantia de que cada Equipamento sempre referencia um Cliente existente, inclusive durante criação de vínculo concorrente à exclusão, continua pendente no requisito de relacionamento obrigatório da especificação. A tarefa 1.4 permanece incompleta quanto ao mecanismo de integridade concorrente, e a tarefa 1.6 não poderá comprovar essa garantia apenas com testes sequenciais. Qualquer solução ou proposta futura de revisão dessa exigência deverá ser analisada e autorizada explicitamente antes de implementar ou alterar o escopo.

**Limites:** não criar APIs ou interface de equipamentos, novas entidades, atributos adicionais, nem antecipar o relacionamento físico com Ordem de Serviço. Esse relacionamento continua previsto no modelo global para evolução futura. A preparação não altera as regras existentes de Cliente nem exige mudanças em `docs/domain-model.md`.

**Verificação planejada:** conferir os campos e o relacionamento no workspace, comprovar a obrigatoriedade do vínculo com cliente existente e verificar o mecanismo de integridade escolhido. Depois, verificar a exclusão de cliente sem vínculos e o bloqueio de cliente com equipamentos, preservando todos os registros envolvidos no bloqueio. A tarefa 2.5 depende dessa preparação e permanece pendente até verificar ambos os cenários.

## Risks / Trade-offs

- **[Indisponibilidade do Xano]** → Apresentar mensagens de erro na interface e permitir nova tentativa.
- **[Falhas de comunicação entre Streamlit e Xano]** → Tratar respostas de erro das APIs e informar o usuário.
- **[Dados inválidos]** → Validar as entradas no backend antes de persistir alterações.
- **[Exclusão de clientes com equipamentos associados]** → Aplicar a verificação de integridade no backend.
- **[Criação de vínculo concorrente à exclusão]** → As verificações prévias não eliminam a condição de corrida; garantia concorrente ainda não atendida, sem solução aprovada. Manter a pendência da decisão 7 e não declarar conclusão das tarefas dependentes com base apenas em verificações sequenciais.
- **[Complexidade excessiva para o projeto acadêmico]** → Manter a implementação limitada ao cadastro de clientes.

## Migration Plan

1. Configurar a estrutura de dados da entidade Cliente no Xano.
   Antes da etapa 2, especificamente da API de exclusão, resolver as decisões pendentes da decisão 7 e preparar e verificar a tabela `equipamento` e sua referência obrigatória a `cliente.id`, preservando os recursos e dados existentes.
2. Criar e verificar as APIs de gerenciamento de clientes.
3. Implementar a interface Streamlit que consome essas APIs.
4. Testar os cenários descritos nas especificações.
5. Versionar os arquivos correspondentes no Git/GitHub.

**Antecipação limitada da interface para demonstração acadêmica:** a etapa 3 pode iniciar parcialmente após a disponibilização das APIs de cadastro e listagem, antes da conclusão integral das etapas anteriores. A entrega antecipada compreende a estrutura e configuração da tarefa 3.1, o formulário de cadastro da 3.2, somente a listagem da 3.3 e o tratamento de falhas desses fluxos da 3.6. A tela será desenvolvida exclusivamente em Python com Streamlit, consumindo `POST /clientes` e `GET /clientes` existentes, sem acesso direto ao banco ou uso da Metadata API. As validações e a normalização de Cliente permanecem no backend conforme a decisão 5.

A consulta individual continua necessária para concluir a tarefa 3.3; o tratamento de falhas dos demais fluxos continua exigido pela 3.6. A edição e a exclusão da interface permanecem fora dessa entrega antecipada. As tarefas 1.3, 1.4, 1.6 e 2.5 continuam pendentes, sem dispensa de requisitos, verificações ou dependências. A limitação concorrente descrita na decisão 7 permanece não resolvida; a implementação da 2.5 continua condicionada à conclusão de 1.4, 1.5 e 1.6, e a 3.5 depende da API de exclusão e de suas verificações.

A antecipação é uma mudança de sequência para uma entrega parcial, sem reduzir o escopo final da Change ou os critérios das tarefas. Este registro autoriza somente o ajuste documental; a implementação da interface requer autorização específica. As verificações locais poderão utilizar respostas simuladas, sem substituir a verificação integrada exigida pelas tarefas; qualquer consulta ou gravação nas APIs do Xano durante testes também depende de autorização específica.

**Rollback:** caso a implementação apresente problemas, utilizar o histórico do Git para recuperar os arquivos versionados e reverter separadamente as alterações necessárias no Xano, preservando os dados existentes.
