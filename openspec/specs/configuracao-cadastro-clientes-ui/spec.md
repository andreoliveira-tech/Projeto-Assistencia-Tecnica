# configuracao-cadastro-clientes-ui Specification

## Purpose
Permitir operar o cadastro pelo Streamlit com configuração externa do grupo de APIs e confirmação de resposta compatível, sem incluir segredos no código.

## Requirements

### Requirement: Configuração externa da API

A interface SHALL usar Streamlit/Python e obter XANO_CLIENTES_API_BASE_URL do ambiente, aceitar apenas URL HTTPS sem credenciais, query ou fragmento e informar configuração ausente ou inválida sem consultar a rede.

#### Scenario: Configuração inválida

- **WHEN** a variável estiver ausente ou contiver URL inválida
- **THEN** a interface deverá orientar a configuração sem realizar HTTP nem expor credenciais

### Requirement: Cadastro pelo formulário

A interface SHALL exigir nome, cpf, telefone e email e enviar uma tentativa de POST /clientes somente quando o usuário acionar Cadastrar, validando a estrutura da resposta antes de apresentar sucesso.

#### Scenario: Cadastro aceito

- **WHEN** o formulário válido for enviado e o serviço retornar cliente no contrato
- **THEN** a interface deverá apresentar o resultado do cadastro

#### Scenario: Campos vazios

- **WHEN** qualquer campo obrigatório estiver vazio
- **THEN** a interface deverá informar o preenchimento necessário sem enviar POST

#### Scenario: Falha ou resultado incerto

- **WHEN** houver rejeição, timeout, HTTP 408 ou resposta inesperada
- **THEN** a interface deverá informar a falha ou incerteza, preservar os campos e não repetir a escrita em rerun
