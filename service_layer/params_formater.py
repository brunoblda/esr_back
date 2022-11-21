import datetime
from auth_layer import jwt_class 

class Params_formater():
  def __init__(self, lista_usuarios_fabrica, lista_feriados, paginas_percorrer, token):
    self.lista_usuarios_fabrica = lista_usuarios_fabrica
    self.lista_feriados = lista_feriados
    self.paginas_percorrer = paginas_percorrer
    self.token = token 

  def validar_todas_entradas_do_banco(self):
    if (
      self.lista_usuarios_fabrica[0] == 200
      and self.lista_feriados[0] == 200
      and self.paginas_percorrer[0] == 200
      ):

      return True

    return False

  def feriados_lista_out(self):
    all_feriados = []
    for feriado in self.lista_feriados[1]:
      feriado_split = feriado["dia"].split("-")
      ano= int(feriado_split[0])
      mes = int(feriado_split[1]) 
      dia = int(feriado_split[2])
      data_feriado = (datetime.date(day=dia, month=mes, year=ano), feriado["periodo"])
      all_feriados.append(data_feriado)
    
    return all_feriados
  
  def usuarios_fabrica_lista_out(self):
    all_usuarios = []
    for usuario in self.lista_usuarios_fabrica[1]:
      usuario_id = usuario["id"]
      all_usuarios.append(usuario_id)
    
    return all_usuarios

  def quantidade_de_paginas_out(self):
    paginas_a_percorrer = self.paginas_percorrer[1][0]["percorre_quantas_paginas"]
    
    return int(paginas_a_percorrer) 
    
  def user_login_out(self):
    user_login_decoded = jwt_class.verify_and_decode_jwt(self.token)
    user_tuple = (user_login_decoded["usuario"], user_login_decoded["senha"])

    return user_tuple