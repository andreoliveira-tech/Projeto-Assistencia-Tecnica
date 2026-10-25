# Tasks

## 1. Estrutura de dados no Xano

- [x] 1.1 Verificar se a entidade Cliente já existe no Xano e conferir os campos `id_cliente`, `nome`, `cpf`, `telefone` e `email` com `docs/domain-model.md`. Confirmar a estrutura no painel do Xano.
- [x] 1.2 Criar ou ajustar a estrutura de Cliente no Xano, caso necessário. Verificar se os campos correspondem ao modelo de domínio.
- [ ] 1.3 Configurar as validações dos dados de clientes no backend. Verificar que dados inválidos sejam rejeitados sem criar ou alterar registros.
- [ ] 1.4 Resolver e registrar as decisões pendentes da preparação de Equipamento: obrigatoriedade e nulabilidade dos campos descritivos e mecanismo de integridade no Xano, inclusive em operações concorrentes. Obter aprovação antes de implementar essas decisões.
- [x] 1.5 Preparar a tabela `equipamento` com `id` representando `id_equipamento`, `tipo`, `marca`, `modelo`, `numero_serie` e referência obrigatória e não nula `id_cliente` a `cliente.id`, conforme as decisões aprovadas. Preparar o índice não exclusivo do vínculo, preservando a tabela Cliente, os dados existentes e as APIs atuais.
- [ ] 1.6 Verificar no Xano os campos e a cardinalidade Cliente 1:N Equipamento, a rejeição de vínculos ausentes, nulos ou com cliente inexistente e a garantia de integridade pelo mecanismo escolhido. Registrar os resultados antes de implementar a tarefa 2.5, sem criar APIs ou interface de equipamentos.

Estado da tarefa 1.4: decisões de campos aprovadas e registradas no design e na especificação (`tipo` obrigatório e não nulo; `marca`, `modelo` e `numero_serie` opcionais e anuláveis; número de série textual; `id_cliente` obrigatório e não nulo, referenciando `cliente.id`). A resposta do suporte e a estratégia de verificações prévias estão documentadas. O mecanismo capaz de garantir integridade em operações concorrentes permanece sem solução; a tarefa 1.4 continua pendente. Sua conclusão exige demonstrar o atendimento desse critério e obter aprovação antes de implementar o mecanismo. A garantia prevista na tarefa 1.6 também não está comprovada. Nenhum checkbox foi dispensado por esse registro.

Execução limitada da tarefa 1.5: a preparação da estrutura mínima aprovada pode avançar antes da conclusão integral da tarefa 1.4, pois os campos, tipos, obrigatoriedade, nulabilidade, referência a `cliente.id` e índice não exclusivo já estão definidos. Essa independência limita-se à estrutura da tabela; não inclui APIs, persistência de equipamentos, implementação das validações de vínculo ou exclusão de clientes. A referência declarada não comprova a existência do cliente nem garante integridade concorrente. A tarefa 1.4 permanece pendente, e a tarefa 1.6 deverá distinguir a conferência estrutural das garantias ainda não atendidas. Todos os requisitos da especificação e as dependências da tarefa 2.5 permanecem vigentes. Este ajuste documental não autoriza implementação ou publicação; o início da tarefa 1.5 exige autorização específica.

## 2. APIs de clientes no Xano

A implementação da tarefa 2.5 depende da conclusão das tarefas 1.4, 1.5 e 1.6. O bloqueio de exclusão deverá consultar o vínculo real em `equipamento.id_cliente`; a tarefa 2.5 permanecerá pendente até a verificação dos cenários com e sem equipamentos vinculados.

- [x] 2.1 Criar a API de cadastro de clientes. Verificar que um cliente válido seja registrado e possa ser consultado.
- [x] 2.2 Criar a API de listagem de clientes. Verificar que os registros cadastrados sejam retornados.
- [x] 2.3 Criar a API de consulta individual. Verificar o retorno de um cliente existente e a resposta para um cliente inexistente.
- [x] 2.4 Criar a API de atualização de clientes. Verificar que as alterações sejam persistidas e retornadas em nova consulta.
- [ ] 2.5 Criar a API de exclusão de clientes. Verificar a exclusão de clientes sem equipamentos vinculados e o bloqueio da exclusão quando houver vínculos.
- [ ] 2.6 Registrar os endpoints e os dados necessários para consumi-los. Verificar se as informações documentadas correspondem às APIs disponíveis no Xano.

## 3. Interface de clientes em Streamlit

Antecipação limitada aprovada para demonstração acadêmica: preparar a tarefa 3.1, o cadastro da 3.2, somente a listagem da 3.3 e o tratamento de falhas desses fluxos previsto na 3.6, consumindo exclusivamente as APIs existentes `POST /clientes` e `GET /clientes`. Essa preparação pode avançar antes da conclusão integral das etapas anteriores, sem dispensar qualquer dependência, requisito ou critério de verificação. A consulta individual continua necessária para concluir a 3.3, e a 3.6 continua exigindo o tratamento dos demais fluxos previstos. A edição da 3.4 e a exclusão da 3.5 não integram essa antecipação.

As tarefas 1.3, 1.4, 1.6 e 2.5 permanecem pendentes. A limitação de integridade concorrente continua não resolvida, e a tarefa 2.5 mantém suas dependências das tarefas 1.4, 1.5 e 1.6. A interface não implementará exclusão nem gerenciamento de equipamentos nesta entrega parcial. Nenhum checkbox, descrição ou critério de conclusão é dispensado; preparar a interface não comprova o atendimento das pendências de backend nem a conclusão da Change. A implementação da interface e os testes integrados com consultas ou gravações no Xano exigem autorização específica; este ajuste é exclusivamente documental.

- [ ] 3.1 Preparar a estrutura da aplicação Python com Streamlit e a configuração de acesso às APIs do Xano. Verificar que a aplicação inicia e consegue consultar o backend.
- [ ] 3.2 Implementar o formulário de cadastro de clientes. Verificar que o envio de dados válidos cria um registro no Xano.
- [ ] 3.3 Implementar a listagem e a consulta individual de clientes. Verificar a exibição dos dados e da mensagem para cliente inexistente.
- [ ] 3.4 Implementar a edição de clientes. Verificar que os dados alterados são apresentados corretamente após nova consulta.
- [ ] 3.5 Implementar a exclusão de clientes. Verificar a exclusão permitida e a apresentação da mensagem de bloqueio quando houver equipamentos vinculados.
- [ ] 3.6 Tratar falhas de comunicação e respostas de erro das APIs. Verificar que a interface informa o problema sem apresentar uma confirmação
