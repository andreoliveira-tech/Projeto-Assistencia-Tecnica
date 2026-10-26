// Preparacao local. Reutiliza tabela 908125 e funcao 355571; nao publicar sem autorizacao.
query equipamentos verb=POST {
  api_group = "Equipamentos"
  input {
    text tipo
    text? marca?
    text? modelo?
    text? numero_serie?
    int id_cliente
  }
  stack {
    function.run "equipamentos/validar_cliente" {
      input = {id_cliente: $input.id_cliente}
    } as $cliente_validado

    precondition ($cliente_validado != null && $cliente_validado.id == $input.id_cliente) {
      error_type = "inputerror"
      error = "Nao foi possivel confirmar o cliente do equipamento."
    }
    db.add equipamento {
      data = {
        tipo: $input.tipo
        marca: $input.marca
        modelo: $input.modelo
        numero_serie: $input.numero_serie
        id_cliente: $cliente_validado.id
      }
    } as $equipamento
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

