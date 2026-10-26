// Atualiza os dados de um cliente somente após validar todos os campos.
query "clientes/{id_cliente}" verb=PUT {
  api_group = "Clientes"

  input {
    int id_cliente
    text nome
    text cpf
    text telefone
    email email
  }

  stack {
    db.get cliente {
      field_name = "id"
      field_value = $input.id_cliente
      output = ["id"]
    } as $cliente

    precondition ($cliente != null) {
      error_type = "notfound"
      error = "Cliente não encontrado."
    }

    function.run "clientes/validar_dados" {
      input = {
        nome: $input.nome
        cpf: $input.cpf
        telefone: $input.telefone
        email: $input.email
      }
    } as $dados_validados

    db.edit cliente {
      field_name = "id"
      field_value = $cliente.id
      data = {
        nome: $dados_validados.nome
        cpf: $dados_validados.cpf
        telefone: $dados_validados.telefone
        email: $dados_validados.email
      }
    } as $cliente_atualizado
  }

  response = {
    id_cliente: $cliente_atualizado.id
    nome: $cliente_atualizado.nome
    cpf: $cliente_atualizado.cpf
    telefone: $cliente_atualizado.telefone
    email: $cliente_atualizado.email
  }
}
