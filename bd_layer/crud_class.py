import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import contador
import auth_layer.jwt_class as auth_class
import utils
import os

#cred = credentials.Certificate("bd_layer\service_key.json")
cred = credentials.Certificate(os.environ.get("service_key"))
firebase_admin.initialize_app(cred)

db=firestore.client()

db.collection("usuarios_fabrica")
db.collection("feriados_e_datas")
db.collection("paginas_de_dados")

#create
def create_usuarios_fabrica_BD(id, login):
  docs = db.collection("usuarios_fabrica").where("id", "==", "{}".format(id)).get()
  if not docs:
    db.collection("usuarios_fabrica").add({'id':'{}'.format(id), 'login':'{}'.format(login)})
    docs_pos = db.collection("usuarios_fabrica").where("id", "==", "{}".format(id)).get() 
    list_doc = list(map(lambda doc: doc.to_dict(), docs_pos))
    return (201, list_doc)
  return (400, [])

def create_feriados_e_datas_DB(dia, periodo):
  docs = db.collection("feriados_e_datas").where("dia", "==", "{}".format(dia)).get()
  if not docs :
    db.collection("feriados_e_datas").add({'dia':'{}'.format(dia), 'periodo':'{}'.format(periodo)})
    docs_pos = db.collection("feriados_e_datas").where("dia", "==", "{}".format(dia)).get() 
    list_doc = list(map(lambda doc: doc.to_dict(), docs_pos))
    return (201, list_doc)
  return (400, [])

def create_paginas_de_dados_BD(login, quantas_paginas):
  docs = db.collection("paginas_de_dados").where("login", "==", "{}".format(login.lower())).get()
  if not docs :
    db.collection("paginas_de_dados").add({'login':'{}'.format(login.lower()), 'percorre_quantas_paginas':'{}'.format(quantas_paginas)})
    docs_pos = db.collection("paginas_de_dados").where("login", "==", "{}".format(login.lower())).get() 
    list_doc = list(map(lambda doc: doc.to_dict(), docs_pos))
    return (201, list_doc)
  return (400, [])

#update
def update_paginas_de_dados_BD(login, quantas_paginas):
  docs = db.collection("paginas_de_dados").where("login", "==", "{}".format(login.lower())).get()
  if docs:
    key = docs[0].id
    db.collection("paginas_de_dados").document(key).update({'percorre_quantas_paginas':'{}'.format(quantas_paginas)})
    docs_pos = db.collection("paginas_de_dados").where("login", "==", "{}".format(login.lower())).get() 
    list_doc = list(map(lambda doc: doc.to_dict(), docs_pos))
    return (200, list_doc)
  return (404, [])


#delete
def delete_usuarios_fabrica_BD(id):
  docs = db.collection("usuarios_fabrica").where("id", "==", "{}".format(id)).get()
  if docs:
    key = docs[0].id
    db.collection("usuarios_fabrica").document(key).delete()
    list_doc = list(map(lambda doc: doc.to_dict(), docs))
    return (200, list_doc) 
  return (404, [])
  
def delete_feriados_e_datas_DB(dia):
  docs = db.collection("feriados_e_datas").where("dia", "==", "{}".format(dia)).get()
  if docs :
    key = docs[0].id
    db.collection("feriados_e_datas").document(key).delete()
    list_doc = list(map(lambda doc: doc.to_dict(), docs))
    return (200, list_doc) 
  return (404, [])

#read by id
def read_usuarios_fabrica_BD_by_id(id):
  docs = db.collection("usuarios_fabrica").where("id", "==", "{}".format(id)).get()
  if docs:
    list_doc = list(map(lambda doc: doc.to_dict(), docs)) 
    return (200, list_doc)
  return (404, [])

def read_feriados_e_datas_DB_by_id(dia):
  docs = db.collection("feriados_e_datas").where("dia", "==", "{}".format(dia)).get()
  if docs :
    list_doc = list(map(lambda doc: doc.to_dict(), docs)) 
    return (200, list_doc)
  return (404, [])

def read_paginas_de_dados_BD_by_id(login):
  docs = db.collection("paginas_de_dados").where("login", "==", "{}".format(login.lower())).get()
  if docs :
    list_doc = list(map(lambda doc: doc.to_dict(), docs)) 
    return (200, list_doc)
  return (404, [])

#read all
def read_usuarios_fabrica_BD_all():
  docs = db.collection("usuarios_fabrica").get()
  if docs:
    list_docs = list(map(lambda doc: doc.to_dict(), docs)) 
    list_docs.sort(key=utils.sort_dict_logins)
    list_docs_sorted = list_docs
    return (200, list_docs_sorted)
  return (404, {})

def read_feriados_e_datas_DB_all():
  docs = db.collection("feriados_e_datas").get()
  if docs:
    list_docs = list(map(lambda doc: doc.to_dict(), docs)) 
    list_docs.sort(key=utils.sort_dict_dias, reverse=True)
    list_docs_sorted = list_docs
    return (200, list_docs_sorted)
  return (404, [])

def read_paginas_de_dados_BD_all():
  docs = db.collection("paginas_de_dados").get()
  if docs :
    list_docs = list(map(lambda doc: doc.to_dict(), docs)) 
    return (200, list_docs)
  return (404, [])

def read_all_users_readmine(jwt):
  user_login = auth_class.verify_and_decode_jwt(jwt)
  all_redmine_users_dict = contador.counting_users((user_login["usuario"], user_login["senha"]))
  if type(all_redmine_users_dict) is dict:
    lower_redmine_users_dict = dict((k, v.lower()) for k, v in all_redmine_users_dict.items()) 
    sorted_redmine_users = sorted(lower_redmine_users_dict.items(), key=lambda x:x[1])
    return(200, sorted_redmine_users)
  return (400, [])
  



