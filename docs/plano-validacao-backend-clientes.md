# Verificação pendente da tarefa 1.3

Este plano não autoriza chamadas reais. A execução exige autorização adicional do
responsável pelo projeto, pois ultrapassa o POST e DELETE do cenário descartável
aprovado para a tarefa 3.5. Não modifica estrutura, código ou publicações do Xano.

## Ambiente e proteção de dados

- Workspace `149143`, grupo Clientes `436987`, branch `v1` confirmada como live.
- URL base `https://x8ki-letl-twmt.n7.xano.io/api:assistencia-tecnica-clientes`.
- Criar um cliente fictício novo com nome `T13-VALIDACAO-20261026-01`, CPF
  demonstrativo `52998224725`, telefone `11900000000` e e-mail
  `t13-validacao-20261026-01@example.invalid`.
- Registrar o ID gerado, exigindo que esteja ausente no baseline anterior.
- Nenhum PUT ou DELETE poderá apontar para um registro do baseline.
- Não criar equipamentos nem vincular registros preexistentes.

## Lote proposto

1. GET da listagem como baseline em memória; não exibir dados pessoais.
2. Um POST válido para criar o cliente fictício acima e GET para conferir os campos.
3. Vinte e três POSTs inválidos, com marcador fictício exclusivo por caso, esperando
   rejeição e confirmando por GET que nenhum registro foi criado.
4. Vinte e três PUTs inválidos, exclusivamente no cliente novo, conferindo por GET
   que todos os campos e tipos anteriores permaneceram inalterados.
5. Dois PUTs válidos no cliente novo: um com máscaras e outro sem máscaras,
   utilizando dados fictícios e CPF matematicamente válido com zero inicial,
   calculado localmente antes da execução. Conferir normalização, preservação de
   zeros à esquerda e identificador estável por GET após cada atualização.
6. Um DELETE no cliente novo, após confirmar ausência de equipamentos, e GET
   posterior para verificar o erro conhecido de cliente inexistente.
7. GET da listagem e comparação integral em memória com o baseline inicial.

São previstas **50 tentativas de escrita**: 24 POSTs (um válido e 23 que devem ser
rejeitados), 25 PUTs (23 que devem ser rejeitados e dois válidos) e um DELETE.
Cada requisição será enviada uma vez, sem repetição ou redirecionamento. As demais
operações serão GETs de verificação. Mensagens, campos e tipos serão conferidos,
sem atribuir aos testes locais execução de XanoScript.

## Matriz dos 23 casos inválidos, aplicada a POST e PUT

| Casos | Mutação em relação ao corpo válido |
| --- | --- |
| 1–4 | Omitir um dos campos: nome, CPF, telefone, e-mail |
| 5–8 | Enviar null em cada um desses quatro campos |
| 9–12 | Enviar texto vazio em cada um desses quatro campos |
| 13 | Nome composto apenas por espaços |
| 14–15 | CPF com 10 e com 12 dígitos |
| 16 | CPF com todos os dígitos iguais |
| 17 | CPF com primeiro verificador alterado (`52998224735`) |
| 18 | CPF com segundo verificador alterado (`52998224724`) |
| 19 | CPF contendo letra (`5299822472A`) |
| 20–22 | Telefone com 9 dígitos, com 12 dígitos e contendo letra |
| 23 | E-mail com formato inválido (`invalido`) |

## Interrupção

Qualquer resposta inesperada, falha de comunicação ou alteração divergente encerra
o lote sem reenvio ou correção automática. Se um POST inválido criar registro,
registrar somente seu identificador fictício e interromper. A remoção desses
registros inesperados precisará ser explicitamente autorizada; não está incluída
no DELETE único planejado. Se o cenário interromper antes da limpeza, informar o
ID descartável remanescente. Nenhum dado preexistente será corrigido ou excluído.

A tarefa 1.3 deve permanecer pendente até que haja evidência suficiente de rejeição
sem persistência e de normalização no backend. Testes de interface com respostas
simuladas não substituem essa comprovação.
