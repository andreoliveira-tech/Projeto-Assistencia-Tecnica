// PREPARATORIO, NAO PUBLICAR: ordem_servico e nome fisico proposto, sem tabela existente.
// Requer resolver e conferir o schema real de OS. Nao criar OS neste incremento.
function "equipamentos/consultar_dependencias" {
  input {
    int id_equipamento
  }
  stack {
    precondition ($input.id_equipamento > 0) {
      error_type = "inputerror"
      error = "id_equipamento deve ser um inteiro positivo."
    }
    db.query ordem_servico {
      where = $db.ordem_servico.id_equipamento == $input.id_equipamento
      return = {type: "exists"}
    } as $possui_os
  }
  response = {id_equipamento: $input.id_equipamento, possui_os: $possui_os}
}

