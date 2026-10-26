# Spec Delta

## Purpose

Permitir o gerenciamento dos clientes de uma assistência técnica, incluindo cadastro, consulta, atualização e exclusão, respeitando o modelo de domínio do projeto.

## ADDED Requirements

### Requirement: Cadastro de clientes

O sistema SHALL permitir cadastrar clientes com os campos `id_cliente`, `nome`, `cpf`, `telefone` e `email`.

#### Scenario: Cadastro realizado com sucesso
- **WHEN** o usuário informar os dados de um novo cliente e solicitar o cadastro
- **THEN** o sistema deverá registrar o cliente e disponibilizá-lo para consulta

### Requirement: Identificador de Cliente

O sistema SHALL utilizar o campo `id`, gerado pelo Xano, como identificador de Cliente e representá-lo como `id_cliente` nas APIs. O identificador SHALL ser gerado no cadastro e permanecer inalterado na atualização.

#### Scenario: Identificador gerado pelo backend
- **WHEN** o usuário cadastrar um cliente com dados válidos sem fornecer um identificador
- **THEN** o Xano deverá gerar `id` e a API deverá apresentá-lo como `id_cliente`

### Requirement: Validação de dados de clientes no backend

O sistema SHALL validar os dados de Cliente no backend Xano antes de criar ou atualizar registros, aplicando as seguintes regras:

- `nome` obrigatório e não vazio após `trim`;
- `cpf` obrigatório, com exatamente 11 dígitos após a normalização e validação matemática dos dois dígitos verificadores;
- `telefone` obrigatório, incluindo DDD e totalizando 10 ou 11 dígitos após a normalização;
- `email` obrigatório e com formato válido.

O sistema SHALL rejeitar dados inválidos, informar o erro e não criar nem alterar registros, inclusive quando a requisição contiver outros campos válidos.

#### Scenario: Campo obrigatório ausente ou nulo no cadastro
- **WHEN** o usuário solicitar o cadastro sem informar `nome`, `cpf`, `telefone` ou `email`, ou informar `null` em qualquer desses campos
- **THEN** o backend deverá rejeitar a solicitação, informar o erro e não criar nenhum registro de Cliente

#### Scenario: Nome vazio após trim
- **WHEN** o usuário solicitar o cadastro com `nome` vazio ou composto apenas por espaços
- **THEN** o backend deverá rejeitar a solicitação, informar o erro e não criar nenhum registro de Cliente

#### Scenario: CPF com quantidade de dígitos inválida
- **WHEN** o usuário solicitar o cadastro com `cpf` vazio ou que não tenha exatamente 11 dígitos após a normalização
- **THEN** o backend deverá rejeitar a solicitação, informar o erro e não criar nenhum registro de Cliente

#### Scenario: CPF com dígitos verificadores inválidos
- **WHEN** o usuário solicitar o cadastro com `cpf` de 11 dígitos que não passe na validação matemática dos dígitos verificadores
- **THEN** o backend deverá rejeitar a solicitação, informar o erro e não criar nenhum registro de Cliente

#### Scenario: Telefone inválido
- **WHEN** o usuário solicitar o cadastro com `telefone` vazio, sem DDD ou que não tenha 10 ou 11 dígitos após a normalização
- **THEN** o backend deverá rejeitar a solicitação, informar o erro e não criar nenhum registro de Cliente

#### Scenario: E-mail inválido
- **WHEN** o usuário solicitar o cadastro com `email` vazio ou com formato inválido
- **THEN** o backend deverá rejeitar a solicitação, informar o erro e não criar nenhum registro de Cliente

#### Scenario: Atualização com dados inválidos
- **WHEN** o usuário solicitar a atualização de um cliente existente com qualquer campo que viole as regras de validação, mesmo enviando outros campos válidos
- **THEN** o backend deverá rejeitar toda a solicitação e informar o erro
- **AND** todos os dados anteriormente persistidos do cliente deverão permanecer inalterados

### Requirement: Normalização de CPF e telefone

O sistema SHALL aceitar CPF e telefone com ou sem máscara e armazená-los como texto contendo somente números, preservando zeros à esquerda. A normalização SHALL ocorrer no backend antes da validação e da persistência, tanto no cadastro quanto na atualização.

#### Scenario: Cadastro com CPF e telefone com máscara
- **WHEN** o usuário cadastrar um cliente com dados válidos e CPF e telefone com máscara
- **THEN** o backend deverá remover a máscara, validar os dados e armazenar CPF e telefone somente com números

#### Scenario: Cadastro com CPF e telefone sem máscara
- **WHEN** o usuário cadastrar um cliente com dados válidos e CPF e telefone somente com números
- **THEN** o backend deverá validar e armazenar esses valores preservando seus dígitos, inclusive zeros à esquerda

#### Scenario: Atualização com CPF e telefone com máscara
- **WHEN** o usuário atualizar um cliente com dados válidos e CPF e telefone com máscara
- **THEN** o backend deverá remover a máscara, validar os dados e persistir CPF e telefone somente com números

### Requirement: Consulta de clientes

O sistema SHALL permitir listar os clientes cadastrados e consultar um cliente específico.

#### Scenario: Listagem de clientes
- **WHEN** o usuário solicitar a listagem de clientes
- **THEN** o sistema deverá apresentar os clientes cadastrados

#### Scenario: Consulta de cliente existente
- **WHEN** o usuário solicitar os dados de um cliente cadastrado
- **THEN** o sistema deverá apresentar os dados desse cliente

#### Scenario: Consulta de cliente inexistente
- **WHEN** o usuário solicitar um cliente inexistente
- **THEN** o sistema deverá informar que o cliente não foi encontrado

### Requirement: Atualização de clientes

O sistema SHALL permitir atualizar os dados de um cliente existente.

#### Scenario: Atualização realizada com sucesso
- **WHEN** o usuário alterar os dados de um cliente cadastrado e confirmar a atualização
- **THEN** o sistema deverá salvar e apresentar os dados atualizados

### Requirement: Exclusão de clientes

O sistema SHALL permitir excluir clientes, respeitando a integridade dos relacionamentos definidos no modelo de domínio no escopo de operações sequenciais desta Change, conforme o requisito de relacionamento obrigatório entre Equipamento e Cliente.

#### Scenario: Exclusão de cliente sem equipamentos vinculados
- **WHEN** o usuário solicitar a exclusão de um cliente sem equipamentos vinculados
- **THEN** o sistema deverá excluir o cadastro

#### Scenario: Exclusão de cliente com equipamentos vinculados
- **WHEN** o usuário solicitar a exclusão de um cliente com equipamentos vinculados
- **THEN** o sistema deverá impedir a exclusão para preservar a integridade dos relacionamentos

### Requirement: Estrutura mínima de Equipamento para integridade de clientes

O sistema SHALL disponibilizar, como dependência da exclusão de clientes, a tabela `equipamento` com os atributos `id_equipamento`, `tipo`, `marca`, `modelo`, `numero_serie` e `id_cliente` previstos no modelo de domínio. O atributo conceitual `id_equipamento` SHALL ser representado pelo campo físico `id`, inteiro gerado pelo Xano, sem duplicação de identificadores. Os campos `tipo`, `marca`, `modelo` e `numero_serie` SHALL utilizar representação textual.

A preparação é limitada à persistência e ao relacionamento com Cliente, sem acrescentar APIs ou interface de gerenciamento de equipamentos. Conforme decisão aprovada, `tipo` SHALL ser obrigatório e não nulo; `marca`, `modelo` e `numero_serie` SHALL ser opcionais e anuláveis, mantendo `numero_serie` textual. Este requisito não estabelece conteúdo mínimo, formatos, tamanhos ou unicidade desses campos.

#### Scenario: Conferência da estrutura de apoio à exclusão
- **WHEN** a estrutura mínima de Equipamento for preparada para a tarefa 2.5
- **THEN** a tabela deverá conter o identificador físico `id` e os campos `tipo`, `marca`, `modelo`, `numero_serie` e `id_cliente`
- **AND** não deverá ser criado um segundo identificador para reproduzir `id_equipamento`
- **AND** a tabela `cliente` e os dados existentes deverão ser preservados

### Requirement: Relacionamento obrigatório entre Equipamento e Cliente

No escopo de operações sequenciais desta Change, o sistema SHALL relacionar cada Equipamento a exatamente um Cliente existente por meio de `equipamento.id_cliente`, referência inteira obrigatória e não nula a `cliente.id`, permitindo vários equipamentos para um mesmo cliente. Antes de criar ou alterar vínculos, o backend SHALL exigir `id_cliente` válido e confirmar a existência do cliente, rejeitando a operação se a referência for ausente, nula, inexistente ou se a consulta falhar. O backend SHALL identificar os equipamentos vinculados por essa referência antes de excluir um cliente e impedir a exclusão quando houver qualquer vínculo, preservando cliente e equipamentos. O backend SHALL permitir a exclusão sem equipamentos vinculados após consulta bem-sucedida e SHALL interrompê-la se a consulta de vínculos falhar, sem realizar exclusão em cascata.

O mecanismo técnico de integridade no Xano é baseado nas verificações prévias de existência e de vínculos em operações sequenciais. As funções internas e os cenários da tarefa 1.6 foram implementados e comprovados conforme as evidências registradas no design; sua aplicação ao endpoint DELETE e o bloqueio efetivo foram implementados e verificados na tarefa 2.5. A falha de consulta possui evidência por inspeção do XanoScript e simulação Python local, não por teste integrado no runtime Xano, conforme registro no design. A simples declaração de referência não constitui comprovação dessa garantia.

**Estratégia documentada e estado de atendimento:** validar a existência do cliente antes de persistir um vínculo e consultar os equipamentos vinculados antes da exclusão são as verificações previstas no backend, rejeitando a operação se a consulta falhar. Conforme resposta do suporte oficial Xano relatada pelo responsável pelo projeto, XanoScript não oferece bloqueio explícito de registros, isolamento serializable ou restrição referencial nativa equivalente a `ON DELETE RESTRICT`. Essas verificações não eliminam completamente condições de corrida.

**Delimitação aprovada e limitação aceita:** os requisitos e cenários de integridade desta Change aplicam-se às operações sequenciais. As verificações prévias não garantem integridade sob operações concorrentes, inclusive criação ou alteração de vínculo simultânea à exclusão do cliente; essa limitação foi expressamente aceita para o escopo atual e não representa problema tecnicamente resolvido. Não foi encontrada evidência documental de exigência expressa de proteção concorrente pelo professor; caso apareça requisito acadêmico contrário, esta decisão deverá ser reavaliada. As tarefas 1.4 e 1.6 foram concluídas mediante aprovações específicas e evidências registradas no design. A tarefa 2.5 foi concluída posteriormente: bloqueio, cliente inexistente e exclusão permitida foram comprovados por testes integrados; a interrupção em falha de consulta foi verificada por inspeção do XanoScript e simulação Python local, não por teste integrado no runtime Xano. O alcance e as limitações dessas evidências estão registrados no design; esta conclusão documental não autoriza novas operações.

#### Scenario: Equipamentos associados ao mesmo cliente
- **WHEN** dois equipamentos estiverem associados ao mesmo cliente existente
- **THEN** ambos deverão referenciar o mesmo `cliente.id` por `id_cliente`, respeitando a cardinalidade Cliente 1:N Equipamento

#### Scenario: Equipamento sem cliente válido
- **WHEN** houver tentativa de persistir um equipamento sem `id_cliente`, com referência nula ou com referência a cliente inexistente
- **THEN** o backend deverá impedir a persistência do vínculo inválido e informar o erro

#### Scenario: Verificação de vínculos antes da exclusão
- **WHEN** o usuário solicitar a exclusão de um cliente e existir equipamento cujo `id_cliente` corresponda ao `id` desse cliente
- **THEN** o backend deverá informar o bloqueio e manter inalterados o cliente e seus equipamentos

#### Scenario: Falha ao verificar vínculos
- **WHEN** a verificação dos equipamentos vinculados falhar durante uma solicitação de exclusão
- **THEN** o backend deverá interromper a exclusão, preservar o cliente e informar o erro
