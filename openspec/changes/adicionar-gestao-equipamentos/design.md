# Design: Gestão de equipamentos

## Context

Dependências: [estrutura e integridade existentes](../garantir-integridade-cliente-equipamento/design.md), [modelo de domínio](../../../docs/domain-model.md) e contrato de Clientes. O inventário GET autorizado encontrou a tabela 908125 e a função 355571, mas nenhum grupo/endpoint de Equipamentos nem tabela de OS.

Dois GETs adicionais em `/api:meta/workspace/149143/table/908125` e `/api:meta/workspace/149143/function/355571`, com `branch=v1`, `include_draft=false` e `include_xanoscript=true`, retornaram 200 e XanoScript `status: ok`. Nenhum registro foi consultado. A tabela corresponde ao arquivo local existente e não será recriada.

## Goals / Non-Goals

**Goals:** CRUD com seis atributos; validação de cliente; confirmação das escritas; preparação local de backend e testes simulados.

**Non-Goals:** publicação, alterações na tabela ou função existentes, implementação de OS/Técnicos/Serviços, filtros por cliente, autenticação nova e regras de unicidade ou formato de série.

## Decisions

### Contrato reutilizado

`equipamentos/validar_cliente` (355571) recebe `int id_cliente` obrigatório, exige valor positivo, faz `db.get cliente` e rejeita cliente inexistente com `inputerror`. Retorna o objeto `$cliente`, com identificador físico `id`, não `id_cliente`. Os endpoints usarão somente esse identificador, sem expor os demais dados pessoais da função. Não haverá uma cópia nova ou alteração da função remota.

### Contrato HTTP proposto

Grupo novo proposto: `Equipamentos`, canonical `assistencia-tecnica-equipamentos`. Rotas: POST/GET `/equipamentos`, GET/PUT/DELETE `/equipamentos/{id_equipamento}`. PUT completo para consistência com Clientes; opcionais omitidos são representados como null, e a interface permite distinguir null de texto vazio. Corpo POST/PUT: tipo, marca, modelo, numero_serie, id_cliente; resposta: os mesmos campos mais id_equipamento. DELETE sem corpo, resposta `{id_equipamento, excluido: true}`.

Sucesso esperado 200. Ausência proposta: 404 com objeto JSON `code: ERROR_CODE_NOT_FOUND`, `message: Equipamento nao encontrado.`. Bloqueio proposto: 400 com `code: ERROR_CODE_INPUT_ERROR`, `message: Equipamento possui ordens de servico vinculadas. Exclusao bloqueada.`. São contratos locais propostos, não status/envelopes observados desses endpoints, ainda inexistentes. A interface não interpreta outros 400 como prova de vínculos.

### Dependências da exclusão

Decisão atual aprovada pelo usuário: equipamento com OS não pode ser excluído e não haverá cascata. Preparar `equipamentos/consultar_dependencias` com saída técnica `{id_equipamento, possui_os}`. A definição local referencia provisoriamente `ordem_servico.id_equipamento`; esse nome físico ainda não existe nem foi confirmado. O helper e DELETE **não podem ser publicados** até resolver e verificar essa dependência em incremento/autorização próprios. Função ausente, falha ou retorno incompatível interrompem o DELETE antes de `db.del`; não haverá stub que declare ausência de OS. Não criar tabela de OS neste incremento. A preparação local não comprova execução no runtime nem proteção concorrente.

### Frontend

Página Streamlit separada em `frontend/pages/1_Equipamentos.py`, sem alterar o fluxo de Clientes. `XANO_EQUIPAMENTOS_API_BASE_URL` explícita, validada com o mesmo mecanismo de URL de Clientes; nenhuma URL real é presumida nem HTTP executado na abertura. IDs são informados pelo usuário; o backend verifica existência do cliente. O carregamento de equipamento fixa o ID usado por edição/exclusão. Campos nullable têm seleção explícita de null. Erros incertos de edição/exclusão exigem novo carregamento; não há retry. PUT requer GET correspondente; DELETE requer resposta válida e GET estrito de ausência. Nenhum 404 genérico confirma exclusão.

Os controles de DELETE permanecem indisponíveis por padrão. A interface só os apresenta quando `XANO_EQUIPAMENTOS_DELETE_VALIDATED=true`, configuração operacional que deverá ser definida após a publicação e validação integrada do endpoint e do bloqueio de OS. A presença da URL base não habilita exclusão. O código HTTP de DELETE permanece preservado enquanto essa configuração estiver ausente ou diferente de `true`.

## Review

Os seis atributos coincidem com o domínio; não há filtro novo, catálogo, campo técnico persistido adicional ou regra de série. A validação de cliente é anterior a db.add/db.edit e usa o contrato publicado verificado. A verificação de OS fica anterior a db.del. A falta da tabela de OS permanece uma dependência real, sem marcar publicação ou validação remota como concluídas. As decisões de técnico obrigatório, data de saída e valores em reais não são implementadas aqui, por pertencerem a incrementos futuros.

## Verification

Testes locais de cliente HTTP e AppTest, com transporte HTTP simulado e bloqueio de sockets/DNS reutilizado da suíte de Clientes. Dados e URLs fictícios. Revisão das definições locais não substitui compilação/publicação e testes no Xano. O manual externo e Apêndice A não foram localizados no repositório; a conformidade com esses documentos não é declarada comprovada.

## Risks / Trade-offs

- Tabela de OS ausente → manter helper/DELETE não publicáveis e validação remota aberta.
- Contrato novo sem execução remota → documentar como proposto e conferir após publicação autorizada.
- Corridas de vínculos → garantia sequencial; não ampliar garantias do mecanismo existente.
- Inventário pode mudar → reconferir antes de qualquer criação remota futura para evitar duplicação.

## Migration Plan

Nenhuma migração ou publicação nesta execução. Após autorização: reconferir inventário; reutilizar tabela/função; criar grupo e endpoints não existentes; resolver a consulta de dependências contra o schema real de OS; testar com fixtures autorizadas. A Change só poderá ser arquivada após os critérios remotos pendentes serem atendidos.
