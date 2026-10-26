// Listagem simples; sem filtros adicionais ou dados de Cliente.
query equipamentos verb=GET {
  api_group = "Equipamentos"
  input {
  }
  stack {
    db.query equipamento {
      return = {type: "list"}
      output = ["id", "tipo", "marca", "modelo", "numero_serie", "id_cliente"]
    } as $equipamentos
  }
  response = $equipamentos|map:{
    id_equipamento: $$.id
    tipo: $$.tipo
    marca: $$.marca
    modelo: $$.modelo
    numero_serie: $$.numero_serie
    id_cliente: $$.id_cliente
  }
}

