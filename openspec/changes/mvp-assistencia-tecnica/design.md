# Design

## Context

O projeto utiliza o fluxo `spec-driven` do OpenSpec e ainda não possui implementação. Ver `proposal.md` para a motivação e `specs/gestao-assistencia-tecnica/spec.md` para o contrato funcional, integralmente preservado nesta revisão. A arquitetura será Xano para backend, persistência e APIs REST; Streamlit com Python para frontend web; Git/GitHub para versionamento. OpenSpec e Codex continuam sendo utilizados para especificação e desenvolvimento assistido.

## Goals / Non-Goals

**Goals:**

- Orientar a implementação preservando todas as entidades, atributos, PKs, FKs, cardinalidades e regras existentes.
- Separar configuração manual no Xano de implementação Python no projeto Streamlit.
- Integrar a interface ao backend exclusivamente pelas APIs REST do Xano.

**Non-Goals:**

- Implementar código ou executar configurações nesta revisão.
- Acrescentar entidades, atributos, funcionalidades ou regras de negócio.
- Automatizar valor_total, data_saida ou impor transições de status não especificadas.

## Decisions

### Backend e persistência no Xano

Configurar manualmente uma tabela para cada uma das cinco entidades da especificação, com todos os atributos e chaves existentes. O Xano será responsável pela persistência e pelas operações e validações do backend. Banco local e backend Python próprio foram descartados em favor da arquitetura solicitada. Uma modelagem documental também foi descartada, pois o modelo relacional corresponde às PKs, FKs e cardinalidades existentes; não são necessárias tabelas associativas.

| Referência | Destino | Relacionamento |
| --- | --- | --- |
| Equipamento.id_cliente | Cliente.id_cliente | Cliente 1:N Equipamento |
| Ordem de Serviço.id_equipamento | Equipamento.id_equipamento | Equipamento 1:N Ordem de Serviço |
| Ordem de Serviço.id_tecnico | Técnico.id_tecnico | Ordem de Serviço N:1 Técnico |
| Serviço.id_os | Ordem de Serviço.id_os | Ordem de Serviço 1:N Serviço |

Eventuais identificadores técnicos exigidos pelo Xano devem ser mapeados à PK correspondente, preservando os nomes de chaves da especificação no contrato REST, sem novos atributos de domínio. Tipos e serialização serão documentados na configuração e não devem criar obrigatoriedade de campos ou regras não especificadas.

### APIs REST configuradas manualmente no Xano

Configurar endpoints de cadastro (POST), listagem e consulta individual (GET), atualização (PATCH) e exclusão (DELETE) das cinco entidades. A consulta de ordens utiliza os endpoints da própria entidade; a alteração de status utiliza sua atualização; o acompanhamento consulta os registros de Serviço por id_os. Não criar histórico ou catálogo de serviços, que acrescentariam entidades não solicitadas.

Documentar no repositório métodos, rotas concretas, entradas, saídas, PKs/FKs, serialização e respostas de erro após a configuração manual. Os endpoints devem preservar todos os atributos e os cenários já especificados, incluindo a exclusão sem dependentes; esta revisão não define política adicional de exclusão com dependentes ou validação específica de CPF.

### Status, valores e datas preservados

Validar no Xano, em toda operação que grave status, somente os cinco valores: Aguardando avaliação, Em manutenção, Aguardando peça, Concluído e Entregue. O Streamlit apresenta esse mesmo domínio para seleção. Não criar entidade Status, máquina de estados ou sequência obrigatória de transições.

Preservar valor_total, valor, data_entrada e data_saida como dados das respectivas entidades. Não derivar valor_total dos serviços nem associar automaticamente datas às mudanças de status.

### Frontend Streamlit com Python e integração REST

Implementar no projeto Streamlit formulários e visualizações para os CRUDs das cinco entidades, consulta de ordens, alteração de status e acompanhamento dos serviços. Um módulo Python concentra o consumo HTTP e o tratamento das respostas. O fluxo será navegador → aplicação Streamlit/Python → APIs REST do Xano → persistência no Xano. A interface não acessa diretamente o banco nem cria persistência paralela; consultas posteriores devem refletir os dados do Xano. Outro framework web foi descartado em favor do Streamlit solicitado.

Configurar a URL base externamente ao código. Credenciais técnicas, caso necessárias para consumir a API configurada, ficam em configuração local ou secrets do ambiente e fora do Git; isso não acrescenta autenticação de usuários ao escopo funcional. Tratar falhas HTTP, indisponibilidade e respostas inválidas, exibindo o resultado na interface sem apresentar operações malsucedidas como concluídas.

### Git/GitHub, OpenSpec e Codex

Versionar com Git e GitHub código Python, dependências, documentação de configuração manual do Xano, contrato REST e artefatos OpenSpec. Como a configuração do Xano ocorre fora do projeto Streamlit, registrar suas definições e procedimentos de reprodução no repositório para manter a correspondência entre backend e frontend. OpenSpec permanece como referência de escopo e planejamento; Codex auxilia o desenvolvimento e a documentação. Nenhuma tarefa será executada nesta revisão.

## Risks / Trade-offs

- [Regras não fornecidas serem assumidas como requisitos] → Restringir critérios de aceite à especificação existente, sem novos atributos, entidades ou regras.
- [Confusão entre serviço realizado e catálogo] → Manter Serviço associado diretamente à ordem por id_os.
- [Divergência entre configuração manual do Xano e projeto versionado] → Documentar tabelas, mapeamentos e contrato REST no Git/GitHub e conferir sua correspondência.
- [Dependência da disponibilidade do Xano] → Centralizar chamadas no cliente Python e verificar o tratamento de falhas e os fluxos integrados.
- [Campos técnicos da plataforma alterarem o modelo acadêmico] → Mapear identificadores às PKs especificadas e conferir os atributos do domínio na persistência e no contrato REST.

## Migration Plan

Não há código ou dados existentes a migrar. Na implementação futura, configurar manualmente no Xano primeiro Cliente e Técnico, depois Equipamento, Ordem de Serviço e Serviço, respeitando as FKs. Configurar e verificar as APIs REST e documentar o contrato antes de implementar o projeto Streamlit/Python. Verificar os fluxos integrados contra a especificação e versionar código e artefatos no Git/GitHub, mantendo OpenSpec e Codex no processo. Esta revisão altera apenas documentos e não requer implantação ou rollback de aplicação.
