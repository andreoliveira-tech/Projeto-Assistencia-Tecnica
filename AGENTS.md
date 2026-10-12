# AGENTS.md — Sistema de Assistência Técnica

## Contexto do projeto

Antes de realizar alterações significativas, consulte os documentos de contexto do projeto:

- `docs/project-overview.md`;
- `docs/domain-model.md`;
- `openspec/config.yaml`;
- especificações e Changes relevantes existentes em `openspec/`.

As decisões e restrições registradas nesses documentos devem ser respeitadas.

## Arquitetura

Respeite as tecnologias e decisões arquiteturais definidas para o projeto.

A arquitetura utiliza:

- Xano como backend, persistência de dados e disponibilização de APIs;
- XanoScript para desenvolvimento e representação versionável dos recursos do backend quando aplicável;
- Streamlit como frontend;
- Python para a aplicação Streamlit e integração com as APIs;
- Git e GitHub para controle de versão;
- OpenSpec para condução incremental das mudanças.

Não introduza tecnologias alternativas sem justificativa e sem uma mudança arquitetural explicitamente aprovada.

## Frontend

O frontend do projeto deve ser implementado exclusivamente com Streamlit.

Não introduza React, Vue, Angular, Next.js ou outra tecnologia de frontend para substituir ou complementar o Streamlit, salvo quando houver uma alteração arquitetural explicitamente aprovada para o projeto.

## Modelo de domínio

Respeite o modelo global registrado em `docs/domain-model.md`.

Não introduza novas entidades, atributos de domínio, relacionamentos ou regras de negócio sem que a necessidade tenha sido identificada e analisada através do processo de desenvolvimento do projeto.

## Desenvolvimento com OpenSpec

Mudanças funcionais ou técnicas relevantes devem utilizar OpenSpec.

O desenvolvimento deve ocorrer incrementalmente, através de Changes com escopo delimitado e verificável.

Antes de implementar uma Change:

1. compreender o contexto relevante;
2. revisar os artefatos da Change;
3. identificar dependências e impactos;
4. implementar somente o escopo aprovado.

Não implemente funcionalidades futuras apenas porque elas estão previstas no escopo global do projeto.

## Código

Reutilize código existente quando apropriado.

Evite duplicação desnecessária.

Não modifique funcionalidades ou arquivos não relacionados à mudança atual sem justificativa.

Mantenha a implementação simples e compatível com o escopo acadêmico do projeto.

## Backend e Xano

Alterações relacionadas ao backend devem respeitar a arquitetura definida para Xano.

Quando aplicável ao fluxo de desenvolvimento, utilize as ferramentas previstas para XanoScript, validação e sincronização com o workspace.

Não conceda a agentes de IA acesso operacional desnecessário ao workspace.

## Segurança

Não armazene tokens, credenciais, chaves de API ou outros segredos diretamente em arquivos versionados.

Caso sejam necessárias credenciais técnicas, utilize mecanismos apropriados de configuração fora do controle de versão.

Regras de segurança e autorização, quando aplicáveis, devem ser tratadas no backend e não depender exclusivamente do frontend.

## Testes e verificação

Mudanças funcionais devem possuir estratégia de verificação.

Antes de considerar uma Change concluída, verifique se o comportamento implementado corresponde à especificação e se não foram introduzidas funcionalidades fora do escopo.

## Git

Revise as alterações antes de realizar commits.

Não versione arquivos locais de ambiente, credenciais ou outros artefatos que não pertençam ao repositório.

Utilize mensagens de commit que descrevam adequadamente a alteração realizada.

## Documentação

Mantenha a documentação coerente com as decisões e alterações efetivamente realizadas.

Não transforme os documentos de contexto em documentação excessivamente detalhada de implementação.

Quando uma decisão estrutural ou arquitetural mudar, atualize a documentação correspondente de forma consciente.