// Armazena a estrutura mínima de equipamentos vinculados a clientes.
table equipamento {
  auth = false

  schema {
    int id

    text tipo

    text? marca?

    text? modelo?

    text? numero_serie?

    int id_cliente {
      table = "cliente"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "id_cliente"}]}
  ]
}
