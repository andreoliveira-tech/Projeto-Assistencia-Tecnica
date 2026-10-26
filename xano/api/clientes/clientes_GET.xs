// Lista os clientes cadastrados, apresentando o id físico como id_cliente.
query clientes verb=GET {
  api_group = "Clientes"

  input {
  }

  stack {
    db.query cliente {
      return = {type: "list"}
      output = ["id", "nome", "cpf", "telefone", "email"]
    } as $clientes
  }

  response = $clientes|map:{
    id_cliente: $$.id
    nome: $$.nome
    cpf: $$.cpf
    telefone: $$.telefone
    email: $$.email
  }
}
