// Armazena os dados dos clientes da assistência técnica
table cliente {
  auth = false

  schema {
    int id

    text nome filters=trim

    text cpf filters=trim

    text telefone filters=trim

    email email filters=trim|lower
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
  ]
  guid = "9Si-aFA7kf0UeTWXnaTPCT_p3rU"
}