from pydantic import BaseModel

class Login(BaseModel):
  usuario: str
  senha: str

class Usuario_fabrica(BaseModel):
  id: str
  login: str

class Feriados_e_datas(BaseModel):
  dia: str
  periodo: str

class Pagina_de_dados(BaseModel):
  quantas_paginas: str

class jwt(BaseModel):
  jwt_token: str

class Extract_body(BaseModel):
  mes: str
  ano: str
