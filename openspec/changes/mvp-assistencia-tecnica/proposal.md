Proposal

Why

O Sistema de Assistência Técnica precisa registrar e gerenciar os dados dos clientes atendidos. O cadastro de clientes será a primeira funcionalidade do projeto, permitindo estabelecer uma base para o futuro relacionamento entre clientes e equipamentos.

What Changes

Implementar o cadastro de clientes com os campos id_cliente, nome, cpf, telefone e email, conforme o modelo de domínio.

Permitir cadastrar novos clientes.

Permitir consultar e listar clientes cadastrados.

Permitir atualizar os dados de clientes existentes.

Permitir excluir clientes, respeitando as regras de integridade dos relacionamentos.

Preparar a persistência mínima de Equipamento como dependência da tarefa 2.5: tabela `equipamento` com os campos previstos no modelo de domínio e relacionamento obrigatório de `id_cliente` com `cliente.id`, permitindo identificar vínculos antes da exclusão de clientes.

Disponibilizar as operações por meio de APIs no Xano.

Criar uma interface em Streamlit para consumir essas APIs.

Fora do escopo: cadastro de equipamentos, técnicos, ordens de serviço, serviços, autenticação e autorização.

A preparação da tabela `equipamento` e de seu relacionamento é a exceção técnica delimitada necessária à exclusão de clientes. O cadastro e gerenciamento de equipamentos por APIs e interface continuam fora do escopo, assim como a implementação de seu relacionamento com ordens de serviço nesta Change. A modelagem aprovada define `tipo` obrigatório e não nulo; `marca`, `modelo` e `numero_serie` opcionais e anuláveis; `numero_serie` como texto; e `id_cliente` obrigatório e não nulo, referenciando `cliente.id`.

A estratégia de backend prevê validar a existência do cliente antes de persistir vínculos e verificar equipamentos vinculados antes de excluir clientes. Conforme resposta do suporte Xano informada pelo responsável pelo projeto, XanoScript não oferece bloqueio explícito de registros, isolamento serializable ou restrição referencial nativa equivalente a `ON DELETE RESTRICT`. Essas verificações não eliminam completamente condições de corrida. A garantia de integridade em operações concorrentes permanece não atendida e pendente de solução; este registro não reduz os requisitos existentes nem autoriza implementação.

Capabilities

New Capabilities

cadastro-clientes: gerenciamento dos dados de clientes, incluindo cadastro, consulta, atualização e exclusão.

Modified Capabilities

Nenhuma. O projeto ainda não possui especificações existentes.

Impact

Backend: criação dos recursos necessários para gerenciar clientes no Xano, utilizando XanoScript quando aplicável.

APIs: disponibilização das operações de cadastro, consulta, atualização e exclusão de clientes.

Frontend: implementação das interfaces correspondentes em Python com Streamlit.

Dados: utilização da entidade Cliente definida em docs/domain-model.md.

Dados de apoio: preparação da entidade Equipamento já prevista em `docs/domain-model.md`, sem novos atributos de domínio nem alterações na tabela `cliente`. A estrutura e o vínculo deverão ser implementados e verificados antes da API de exclusão.

OpenSpec: criação da especificação da capacidade cadastro-clientes.

Git/GitHub: versionamento dos arquivos e das alterações produzidas.
