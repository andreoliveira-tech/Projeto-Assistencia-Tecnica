# Project Overview — Sistema de Assistência Técnica

## 1. Visão geral

O projeto consiste no desenvolvimento de um sistema acadêmico para gerenciamento de uma assistência técnica.

A aplicação permitirá organizar clientes, equipamentos, técnicos, ordens de serviço e serviços realizados, possibilitando o acompanhamento do atendimento desde o registro do equipamento até a conclusão e entrega da ordem de serviço.

## 2. Problema

Assistências técnicas precisam controlar informações relacionadas aos clientes, equipamentos recebidos, técnicos responsáveis, problemas relatados, serviços executados e andamento das ordens de serviço.

O projeto busca centralizar essas informações em uma aplicação simples, permitindo registrar e consultar os dados necessários para acompanhar os atendimentos.

## 3. Objetivo

Desenvolver uma aplicação funcional para gerenciamento básico de uma assistência técnica, utilizando as tecnologias e práticas definidas na disciplina.

O sistema deverá permitir o cadastro e gerenciamento das principais informações do domínio e o acompanhamento das ordens de serviço.

## 4. Usuários

O sistema será utilizado no contexto operacional de uma assistência técnica.

Nesta versão acadêmica inicial, não serão definidos diferentes perfis de acesso ou mecanismos de autenticação, salvo se esse requisito for posteriormente estabelecido por uma mudança aprovada no projeto.

## 5. Escopo inicial

O escopo do projeto compreende o gerenciamento de:

- clientes;
- equipamentos;
- técnicos;
- ordens de serviço;
- serviços realizados.

O sistema deverá manter os relacionamentos necessários entre esses conceitos para permitir o acompanhamento adequado dos atendimentos.

## 6. Principais funcionalidades

A aplicação deverá permitir:

- cadastrar, consultar, atualizar e excluir clientes;
- cadastrar, consultar, atualizar e excluir equipamentos;
- cadastrar, consultar, atualizar e excluir técnicos;
- cadastrar, consultar, atualizar e excluir ordens de serviço;
- cadastrar, consultar, atualizar e excluir serviços;
- relacionar equipamentos aos respectivos clientes;
- relacionar ordens de serviço aos equipamentos e técnicos responsáveis;
- relacionar serviços às respectivas ordens de serviço;
- consultar ordens de serviço cadastradas;
- alterar e acompanhar o status das ordens de serviço;
- acompanhar os serviços associados a uma ordem de serviço.

## 7. Status das ordens de serviço

O acompanhamento das ordens de serviço deverá considerar os seguintes estados previstos para o projeto:

- Aguardando avaliação;
- Em manutenção;
- Aguardando peça;
- Concluído;
- Entregue.

## 8. Arquitetura tecnológica

O projeto utilizará:

- **Xano** como plataforma de backend, persistência de dados e disponibilização das APIs;
- **XanoScript** para desenvolvimento e representação versionável dos recursos do backend quando aplicável;
- **Streamlit** como tecnologia exclusiva para implementação do frontend;
- **Python** para desenvolvimento da aplicação Streamlit e integração com as APIs;
- **Git** para controle de versão;
- **GitHub** como repositório remoto;
- **OpenSpec** para especificação e condução incremental das mudanças;
- ferramentas de Inteligência Artificial compatíveis com o processo definido pela disciplina.

A comunicação entre o frontend e o backend deverá ocorrer por meio das APIs disponibilizadas pelo Xano.

## 9. Princípios de desenvolvimento

O desenvolvimento deverá ocorrer de forma incremental.

As funcionalidades deverão ser planejadas e implementadas através do fluxo definido pelo OpenSpec, evitando implementar antecipadamente funcionalidades que ainda não tenham sido especificadas.

As decisões arquiteturais e o modelo global do domínio deverão ser respeitados durante a evolução do projeto.

## 10. Restrições

O projeto deverá permanecer dentro do escopo acadêmico definido.

O modelo de domínio deverá utilizar os conceitos previstos para Cliente, Equipamento, Ordem de Serviço, Técnico e Serviço.

O frontend deverá ser implementado exclusivamente com Streamlit.

Novas entidades, funcionalidades ou tecnologias não deverão ser introduzidas sem necessidade identificada e decisão explícita no processo de desenvolvimento.

## 11. Versionamento e documentação

O código-fonte, os artefatos OpenSpec, a documentação do projeto e os recursos versionáveis relacionados ao desenvolvimento deverão ser mantidos sob controle de versão com Git e GitHub.

Alterações relevantes deverão ser documentadas e realizadas de forma compatível com o processo incremental definido para o projeto.

## 12. Fonte de verdade

Os requisitos fornecidos para o trabalho acadêmico constituem a referência principal para o escopo funcional.

Os documentos de contexto descrevem a visão global e as decisões estáveis do projeto.

O OpenSpec será utilizado para especificar e acompanhar as mudanças incrementais realizadas durante o desenvolvimento.