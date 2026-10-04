# Tasks

Todas as tarefas são futuras e permanecem pendentes. Esta revisão atualiza apenas o planejamento técnico.

## 1. Xano — configuração manual do modelo

- [ ] 1.1 Configurar manualmente Cliente e Técnico no Xano com todos os atributos e PKs da especificação; verificar a correspondência dos campos e documentar o mapeamento dos identificadores técnicos às PKs previstas.
- [ ] 1.2 Configurar manualmente Equipamento, Ordem de Serviço e Serviço no Xano com todos os atributos, PKs e FKs; verificar exatamente cinco entidades de domínio e os quatro relacionamentos especificados, sem atributos de domínio adicionais.
- [ ] 1.3 Verificar manualmente os relacionamentos com exemplos de vários equipamentos por cliente, várias ordens por equipamento e técnico e vários serviços por ordem; documentar os resultados e as instruções de reprodução do modelo.

## 2. Xano — configuração manual das APIs REST

- [ ] 2.1 Configurar manualmente endpoints de cadastro, listagem, consulta individual, atualização e exclusão de Cliente e Técnico; verificar os quatro cenários de CRUD para cada entidade, incluindo exclusão sem dependentes.
- [ ] 2.2 Configurar manualmente os endpoints de CRUD de Equipamento; verificar os quatro cenários de CRUD e a associação por id_cliente.
- [ ] 2.3 Configurar manualmente os endpoints de CRUD de Ordem de Serviço; verificar os quatro cenários de CRUD, as referências ao equipamento e ao técnico e os dois cenários de consulta de ordens com todos os atributos previstos.
- [ ] 2.4 Configurar manualmente os endpoints de CRUD de Serviço e sua consulta por id_os; verificar os quatro cenários de CRUD, a associação à ordem e os dois cenários de acompanhamento, sem retornar serviços de outras ordens.
- [ ] 2.5 Configurar manualmente a validação dos cinco status previstos em toda operação que grave status; verificar persistência de cada valor e rejeição de valores fora do domínio no cadastro e atualização, sem impor transições, calcular valor_total ou preencher datas automaticamente.
- [ ] 2.6 Documentar a configuração manual e o contrato REST do Xano com métodos POST/GET/PATCH/DELETE, rotas, entradas, saídas, mapeamento de PKs/FKs, serialização e respostas de erro; verificar que os exemplos reproduzem CRUDs, consultas, alteração de status e acompanhamento conforme a especificação.

## 3. Projeto Streamlit — estrutura Python e integração REST

- [ ] 3.1 Preparar o projeto Python com Streamlit e dependências HTTP; verificar a inicialização da aplicação e documentar instalação e execução.
- [ ] 3.2 Implementar o cliente Python das APIs REST do Xano com URL base externa ao código e credenciais técnicas fora do Git, caso necessárias; verificar métodos e payloads contra o contrato documentado e registrar as instruções de configuração.
- [ ] 3.3 Implementar tratamento de falhas HTTP, indisponibilidade e respostas inválidas; verificar com respostas simuladas que a interface informa falhas sem apresentar operações malsucedidas como concluídas e documentar como executar a verificação.

## 4. Projeto Streamlit — interface dos CRUDs

- [ ] 4.1 Implementar formulários e consultas de Cliente e Técnico consumindo as APIs REST do Xano; verificar os quatro cenários de CRUD para cada entidade e documentar seu uso.
- [ ] 4.2 Implementar formulários e consultas de Equipamento com referência ao cliente pelo cliente REST; verificar os quatro cenários de CRUD e a associação por id_cliente e documentar seu uso.
- [ ] 4.3 Implementar formulários e consultas de Ordem de Serviço com todos os atributos e referências ao equipamento e ao técnico pelo cliente REST; verificar os quatro cenários de CRUD e as associações e documentar seu uso.
- [ ] 4.4 Implementar formulários e consultas de Serviço com referência à ordem pelo cliente REST; verificar os quatro cenários de CRUD e a associação por id_os e documentar seu uso.

## 5. Projeto Streamlit — consulta e acompanhamento

- [ ] 5.1 Disponibilizar consulta das ordens cadastradas e dos dados de uma ordem pelas APIs do Xano; verificar os dois cenários do requisito de consulta e documentar como reproduzi-los na interface.
- [ ] 5.2 Implementar seleção dos cinco status previstos e gravação pela API de atualização da ordem; verificar que cada valor persiste no Xano e aparece em consulta posterior, sem sequência obrigatória de transições, e documentar o uso.
- [ ] 5.3 Disponibilizar acompanhamento dos serviços da ordem pela consulta REST por id_os; verificar os atributos previstos e o reflexo de cadastro, atualização e exclusão em consultas posteriores e documentar o uso.

## 6. Git/GitHub — versionamento e desenvolvimento assistido

- [ ] 6.1 Organizar o versionamento com Git e GitHub do código Streamlit/Python, dependências, documentação do Xano e artefatos OpenSpec, excluindo secrets e arquivos locais de ambiente; verificar arquivos rastreados e correspondência entre repositório local e remoto.
- [ ] 6.2 Documentar o fluxo de desenvolvimento assistido com OpenSpec e Codex e o registro das configurações manuais do Xano no Git/GitHub; verificar que as instruções permitem relacionar especificação, contrato REST e código versionado.

## 7. Integração do MVP

- [ ] 7.1 Executar pelo Streamlit integrado ao Xano um fluxo de cadastro de cliente, técnico, equipamento, ordem e serviços, seguido de consulta, alteração de status e acompanhamento; verificar vínculos, persistência no Xano e dados retornados em cada etapa.
- [ ] 7.2 Conferir configuração do Xano e implementação Streamlit contra todos os cenários da especificação, verificando exatamente cinco entidades, todos os atributos, quatro relacionamentos, CRUDs e cinco status, sem entidades, funcionalidades ou regras adicionais; registrar o resultado da conferência integrada.
