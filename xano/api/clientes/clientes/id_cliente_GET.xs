// Consulta um cliente pelo identificador e informa quando não for encontrado.
query "clientes/{id_cliente}" verb=GET {
  api_group = "Clientes"

  input {
    int id_cliente
  }

  stack {
    db.get cliente {
      field_name = "id"
      field_value = $input.id_cliente
      output = ["id", "nome", "cpf", "telefone", "email"]
    } as $cliente

    precondition ($cliente != null) {
      error_type = "notfound"
      error = "Cliente não encontrado."
    }
  }

  response = {
    id_cliente: $cliente.id
    nome: $cliente.nome
    cpf: $cliente.cpf
    telefone: $cliente.telefone
    email: $cliente.email
  }
}
