// Valida e normaliza Cliente sem consultar ou gravar no banco.
function "clientes/validar_dados" {
  description = "Retorna nome, CPF, telefone e e-mail validados e normalizados."

  input {
    text nome filters=trim|min:1
    text cpf filters=trim
    text telefone filters=trim
    email email filters=trim|lower
  }

  stack {
    // Remove apenas caracteres de máscara; letras continuam inválidas.
    var $cpf {
      value = "/[ .-]/"|regex_replace:"":$input.cpf
    }
    var $telefone {
      value = "/[ ()-]/"|regex_replace:"":$input.telefone
    }

    precondition ("/^[0-9]{11}$/"|regex_matches:$cpf) {
      error_type = "inputerror"
      error = "CPF deve conter exatamente 11 dígitos, com ou sem máscara."
    }
    precondition ("/^[0-9]{10,11}$/"|regex_matches:$telefone) {
      error_type = "inputerror"
      error = "Telefone deve conter DDD e 10 ou 11 dígitos, com ou sem máscara."
    }

    // O número completo permanece texto, preservando zeros à esquerda.
    var $primeiro_digito {
      value = $cpf|substr:0:1
    }
    var $todos_iguais {
      value = true
    }
    var $soma_primeiro {
      value = 0
    }
    var $soma_segundo {
      value = 0
    }

    var $i {
      value = 0
    }
    while ($i < 11) {
      each {
        var $caractere {
          value = $cpf|substr:$i:1
        }
        conditional {
          if ($caractere != $primeiro_digito) {
            var.update $todos_iguais {
              value = false
            }
          }
        }
        conditional {
          if ($i < 9) {
            var $digito {
              value = $caractere|to_int
            }
            var.update $soma_primeiro {
              value = $soma_primeiro + $digito * (10 - $i)
            }
            var.update $soma_segundo {
              value = $soma_segundo + $digito * (11 - $i)
            }
          }
        }
        var.update $i {
          value = $i + 1
        }
      }
    }

    precondition (!$todos_iguais) {
      error_type = "inputerror"
      error = "CPF inválido: todos os dígitos são iguais."
    }

    var $resto_primeiro {
      value = $soma_primeiro % 11
    }
    var $verificador_primeiro {
      value = 0
    }
    conditional {
      if ($resto_primeiro >= 2) {
        var.update $verificador_primeiro {
          value = 11 - $resto_primeiro
        }
      }
    }

    precondition (($cpf|substr:9:1|to_int) == $verificador_primeiro) {
      error_type = "inputerror"
      error = "CPF inválido: primeiro dígito verificador incorreto."
    }

    var $resto_segundo {
      value = ($soma_segundo + $verificador_primeiro * 2) % 11
    }
    var $verificador_segundo {
      value = 0
    }
    conditional {
      if ($resto_segundo >= 2) {
        var.update $verificador_segundo {
          value = 11 - $resto_segundo
        }
      }
    }

    precondition (($cpf|substr:10:1|to_int) == $verificador_segundo) {
      error_type = "inputerror"
      error = "CPF inválido: segundo dígito verificador incorreto."
    }
  }

  response = {
    nome: $input.nome
    cpf: $cpf
    telefone: $telefone
    email: $input.email
  }
  guid = "k8X1BeNgINt2LcDZdvK_qAIz9Q8"
}
