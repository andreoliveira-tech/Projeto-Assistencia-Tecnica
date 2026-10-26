// NAO PUBLICAR: depende de consulta de OS contra schema ainda ausente.
query "equipamentos/{id_equipamento}" verb=DELETE {
  api_group = "Equipamentos"
  input {
    int id_equipamento
  }
  stack {
    precondition ($input.id_equipamento > 0) {
      error_type = "inputerror"
      error = "id_equipamento deve ser um inteiro positivo."
    }
    db.get equipamento {
      field_name = "id"
      field_value = $input.id_equipamento
    } as $equipamento

    precondition ($equipamento != null) {
      error_type = "notfound"
      error = "Equipamento nao encontrado."
    }
    function.run "equipamentos/consultar_dependencias" {
      input = {id_equipamento: $equipamento.id}
    } as $dependencias

    precondition ($dependencias != null && $dependencias.id_equipamento == $equipamento.id && ($dependencias.possui_os == true || $dependencias.possui_os == false)) {
      error_type = "inputerror"
      error = "Nao foi possivel confirmar as ordens do equipamento."
    }
    precondition ($dependencias.possui_os == false) {
      error_type = "inputerror"
      error = "Equipamento possui ordens de servico vinculadas. Exclusao bloqueada."
    }
    db.del equipamento {
      field_name = "id"
      field_value = $equipamento.id
    }
  }
  response = {id_equipamento: $equipamento.id, excluido: true}
}

