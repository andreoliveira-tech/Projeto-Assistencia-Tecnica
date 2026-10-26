# Tasks

## 1. Configuração e formulário de cadastro

- [x] 1.1 Preparar Streamlit e configurar `XANO_CLIENTES_API_BASE_URL` externamente, sem credenciais no código. Critério: validação de configuração em `frontend/config.py`, orientação no README e inicialização/consulta registradas para a 3.1.
- [x] 1.2 Enviar POST somente na submissão explícita do formulário com quatro campos preenchidos, validando a resposta antes de confirmar sucesso. Critério: `frontend/app.py`, `cadastrar_cliente` e testes de campos vazios/rejeições.
- [x] 1.3 Verificar configuração, falhas e cadastro válido pela interface. Evidência: testes locais referenciados no design e criação do descartável 13 por AppTest com API real, registrada em `docs/validacao-mvp-clientes.md`.

## Evidências

As marcações se baseiam na implementação e nas verificações registradas em [design.md](design.md#verification), com rastreabilidade às tarefas **3.1 e 3.2; parcela de 2.6 relativa à configuração de consumo** de [mvp-assistencia-tecnica](../../mvp-assistencia-tecnica/tasks.md).

Datas comprovadas e limites estão no [histórico do design](design.md#histórico-e-fontes). Este checklist não registra novas execuções.
