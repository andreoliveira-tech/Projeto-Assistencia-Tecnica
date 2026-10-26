# exclusao-falhas-clientes-ui Specification

## Purpose
Concluir o fluxo de exclusão com confirmação explícita e preservar informação confiável diante de bloqueios, respostas ambíguas e falhas de comunicação nos fluxos do frontend.

## Requirements

### Requirement: Confirmação explícita de exclusão

A interface SHALL exigir carregamento do cliente por GET e confirmação inicialmente desmarcada antes da ação direta Excluir definitivamente; somente essa ação SHALL enviar um DELETE, sem repetições automáticas.

#### Scenario: Rerun ou cancelamento

- **WHEN** a página abrir, ocorrer rerun, a confirmação for marcada ou a seleção for cancelada sem o botão de exclusão
- **THEN** nenhum DELETE deverá ser enviado

#### Scenario: Troca de contexto

- **WHEN** o identificador, o cliente carregado ou a URL base mudar
- **THEN** a seleção e confirmação anteriores deverão ser invalidadas

### Requirement: Confirmação estrita de ausência

A interface SHALL validar DELETE HTTP 200 com id_cliente inteiro igual ao solicitado e excluido exatamente true e então confirmar ausência por GET HTTP 404 com objeto JSON, code ERROR_CODE_NOT_FOUND e message Cliente não encontrado. antes de declarar exclusão confirmada.

#### Scenario: Exclusão confirmada

- **WHEN** DELETE e GET posterior atenderem aos contratos conhecidos
- **THEN** a interface deverá confirmar a exclusão

#### Scenario: Ausência ambígua

- **WHEN** o GET retornar 404 com código ou mensagem divergente, JSON inválido, erro de infraestrutura ou resposta inesperada
- **THEN** a interface deverá informar falha de confirmação e nunca declarar exclusão confirmada

### Requirement: Tratamento de bloqueio e incerteza

A interface SHALL distinguir bloqueio conhecido por equipamentos, cliente inexistente, rejeição e resultado incerto; SHALL tratar timeout, comunicação interrompida, HTTP 408, 5xx e retorno inesperado sem repetir DELETE automaticamente.

#### Scenario: Bloqueio por equipamentos

- **WHEN** o serviço retornar HTTP 400 com a mensagem conhecida Cliente possui equipamentos vinculados. Exclusao bloqueada.
- **THEN** a interface deverá informar bloqueio por equipamentos e preservar estados

#### Scenario: Falha de verificação de vínculos

- **WHEN** o serviço retornar outro erro na exclusão
- **THEN** a interface não deverá atribuir automaticamente equipamentos ao cliente nem confirmar sucesso

#### Scenario: Conferência após incerteza

- **WHEN** o usuário solicitar Conferir estado atual da exclusão
- **THEN** a interface deverá executar somente GET e informar o estado atual sem atribuir ausência à tentativa anterior

### Requirement: Invalidação dos estados pertinentes

A interface SHALL invalidar a listagem e os estados de consulta e edição do mesmo cliente quando a ausência for constatada pelo contrato estrito, preservando estados de outros clientes.

#### Scenario: Ausência comprovada

- **WHEN** a ausência do cliente for confirmada
- **THEN** a lista em sessão e consulta/edição desse cliente deverão ser descartadas sem atualização automática da lista

### Requirement: Falhas sem falso sucesso nos fluxos

A interface SHALL informar erros de configuração, comunicação, HTTP e contratos inválidos em cadastro, listagem, consulta, edição e exclusão sem declarar sucesso indevido ou reenviar escritas em reruns.

#### Scenario: Resposta incompatível

- **WHEN** um fluxo receber resposta fora de seu contrato
- **THEN** a interface deverá apresentar a falha ou incerteza correspondente sem uma confirmação falsa
