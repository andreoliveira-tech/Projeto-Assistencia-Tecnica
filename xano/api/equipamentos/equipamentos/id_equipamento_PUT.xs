// PUT completo; validar o cliente antes de qualquer alteracao.
query "equipamentos/{id_equipamento}" verb=PUT {
  api_group = "Equipamentos"
  input {
    int id_equipamento
    text tipo
    text? marca?
    text? modelo?
    text? numero_serie?
    int id_cliente
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
    function.run "equipamentos/validar_cliente" {
      input = {id_cliente: $input.id_cliente}
    } as $cliente_validado

    precondition ($cliente_validado != null && $cliente_validado.id == $input.id_cliente) {
      error_type = "inputerror"
      error = "Nao foi possivel confirmar o cliente do equipamento."
    }
    db.edit equipamento {
      field_name = "id"
      field_value = $equipamento.id
      data = {
        tipo: $input.tipo
        marca: $input.marca
        modelo: $input.modelo
        numero_serie: $input.numero_serie
        id_cliente: $cliente_validado.id
      }
    } as $equipamento_atualizado
  }
  response = {
    id_equipamento: $equipamento_atualizado.id
    tipo: $equipamento_atualizado.tipo
    marca: $equipamento_atualizado.marca
    modelo: $equipamento_atualizado.modelo
    numero_serie: $equipamento_atualizado.numero_serie
    id_cliente: $equipamento_atualizado.id_cliente
  }
}

