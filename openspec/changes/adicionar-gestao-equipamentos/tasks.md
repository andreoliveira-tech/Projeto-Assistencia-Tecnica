# Tasks

## 1. Contexto e contratos

- [x] 1.1 Conferir inventário e schema da tabela 908125 e contrato publicado da função 355571 por GET de metadados, sem registros; evidência e limites no design.
- [x] 1.2 Revisar os seis atributos, operações, vínculo obrigatório e decisão atual de bloqueio com OS; verificar coerência entre proposta, design e cenários.

## 2. Preparação local do backend

- [x] 2.1 Preparar grupo e cinco endpoints XanoScript locais, sem duplicar tabela/função existentes; revisar mapeamentos e ordem de validação antes da escrita. Sete definições locais passaram pelo validador de sintaxe, sem execução remota.
- [x] 2.2 Preparar consulta de dependências e DELETE que interrompe a operação em falha; documentar a referência provisória à tabela de OS e a impossibilidade de publicação atual. Ver `docs/api-equipamentos.md`; a tarefa 4.1 continua aberta.
- [x] 2.3 Documentar contratos HTTP propostos e recursos remotos necessários, distinguindo preparação de validação no runtime em `docs/api-equipamentos.md` e no README do frontend.

## 3. Frontend e testes locais

- [x] 3.1 Implementar configuração externa e cliente HTTP de CRUD, com contratos estritos, uma tentativa por ação, timeout e redirecionamentos desativados; verificar com HTTP simulado. Coberto na suíte local aprovada.
- [x] 3.2 Implementar página Streamlit com campos nullable, carregamento para edição/exclusão, confirmação explícita, recuperação de resultados incertos e controles de DELETE desabilitados até validação explícita; verificar por AppTest. Coberto na suíte local aprovada.
- [x] 3.3 Executar suíte local com rede bloqueada, corrigir falhas e conferir regressão de Clientes; registrar resultados reais na documentação. Execução inicial: 77 testes. Após incluir o gate explícito de DELETE: 79 testes aprovados (30 de Equipamentos e 49 de Clientes), sem HTTP real.
- [x] 3.4 Validar estrutura OpenSpec e referências locais; conferir preservação das onze Changes anteriores e ausência de alterações remotas. Doze Changes válidas; comparação SHA-256 dos arquivos anteriores e conferência de links sem divergências fora dos dois arquivos locais previstos.

## 4. Publicação e verificação remota — requer autorização específica

- [ ] 4.1 Resolver e verificar a consulta real de OS contra o schema aprovado, sem criar OS antecipadamente; validar XanoScript no contexto do workspace.
- [ ] 4.2 Reconferir inventário e publicar apenas grupo/endpoints/helper necessários, reutilizando 908125/355571; confirmar definições publicadas e URL real.
- [ ] 4.3 Testar CRUD, rejeição sem escrita, bloqueio com OS e ausência sem dependências com fixtures autorizadas; conferir persistência e não cascata.
- [ ] 4.4 Revisar os contratos publicados e as evidências integradas para encerramento; nenhuma tarefa remota pode ser encerrada com mocks. Somente após esse critério, executar o procedimento Archive do OpenSpec.
