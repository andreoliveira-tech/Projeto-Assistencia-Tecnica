query "equipamentos/{id_equipamento}" verb=GET {
  api_group = "Equipamentos"
  input {
    int id_equipamento
  }
  stack {
    db.get equipamento {
      field_name = "id"
      field_value = $input.id_equipamento
    } as $equipamento

    precondition ($equipamento != null) {
      error_type = "notfound"
      error = "Equipamento nao encontrado."
    }
  }
  response = {
    id_equipamento: $equipamento.id
    tipo: $equipamento.tipo
    marca: $equipamento.marca
    modelo: $equipamento.modelo
    numero_serie: $equipamento.numero_serie
    id_cliente: $equipamento.id_cliente
  }
}

