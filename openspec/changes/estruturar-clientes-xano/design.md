# Design: Persistência e identidade de clientes

## Context

Manter os dados de Cliente no Xano com correspondência explícita entre o modelo conceitual e a identidade física, sem duplicar identificadores. O contrato correspondente está em [specs/persistencia-clientes/spec.md](specs/persistencia-clientes/spec.md).

Dependências: Nenhuma outra Change.

## Goals / Non-Goals

**Goals:** Estrutura Cliente com nome, CPF, telefone e e-mail. Mapeamento do id gerado pelo Xano para id_cliente nas APIs.

**Non-Goals:** ampliar o modelo de domínio ou alterar os contratos dos demais fluxos. Manter o comportamento dos recursos existentes.

## Decisions

Reutilizar cliente.id inteiro nativo; CPF e telefone permanecem textuais. A representação pública usa id_cliente, e nenhum campo duplicado de identidade é criado.

O identificador nativo evita manter duas chaves para o mesmo cliente.

### Código e contratos

- [xano/table/cliente.xs](../../../xano/table/cliente.xs)
- [docs/domain-model.md](../../../docs/domain-model.md)
- [docs/api-clientes.md](../../../docs/api-clientes.md)

## Verification

A estrutura local e a conferência registrada nas tarefas 1.1/1.2 sustentam o modelo. O cenário integrado já documentado criou o cliente descartável 13, recebeu seu identificador gerado e conferiu os quatro campos por GET antes de removê-lo. Não houve nova inspeção remota nesta revisão documental.

Fontes de testes e resultados:

- docs/validacao-mvp-clientes.md — cenário integrado, etapas 2 e 3
- frontend/tests/test_exclusao_clientes.py::ClienteHttpTests.test_sucesso_uma_tentativa_sem_corpo_e_sem_redirecionamento (contrato de identidade, simulado)



## Risks / Trade-offs

A conferência de persistência não comprova toda a validação matemática nem a rejeição sem escrita. Esses critérios pertencem exclusivamente à Change `adicionar-cadastro-clientes-api`.

## Histórico e fontes

| Registro | Evidência |
| --- | --- |
| Implementação | Data exata de criação da tabela e do mapeamento indeterminada. As tarefas 1.1/1.2 já estavam registradas como concluídas em 25/10/2026 no commit `6cec2f6`. O XanoScript de Cliente entrou no Git em 26/10/2026 (`c66fb69`), o que data sua captura no repositório, não a criação remota. |
| Documentação | Modelo conceitual registrado em 05/10/2026 (`743f189`); tarefas da estrutura no registro de 25/10/2026 (`6cec2f6`); registro formal do escopo em 26/10/2026. |
| Validação | O checklist de 25/10/2026 declara a conferência da estrutura concluída, mas não informa a data exata da inspeção original. Criação e leitura do descartável foram novamente evidenciadas no relatório de validação de 26/10/2026. |
| Datas indeterminadas | Dia exato da implementação remota inicial e da inspeção original de Cliente. |

- `git show 6cec2f6:openspec/changes/mvp-assistencia-tecnica/tasks.md` — 1.1/1.2 marcadas
- `git show c66fb69:xano/table/cliente.xs` — primeira versão do arquivo no histórico disponível
- [docs/validacao-mvp-clientes.md](../../../docs/validacao-mvp-clientes.md) — validação datada de 26/10/2026

Rastreabilidade: tarefas **1.1 e 1.2** de [mvp-assistencia-tecnica](../mvp-assistencia-tecnica/tasks.md). A cronologia comum e o significado das datas estão em [histórico técnico](../../../docs/historico-clientes.md).
