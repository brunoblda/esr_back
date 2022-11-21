from asyncio import run_coroutine_threadsafe
from dataclasses import field
from http.cookiejar import FileCookieJar
from lib2to3.pgen2.token import NEWLINE
from getpass import getpass
from re import I
import requests
import contador   
import datetime
import result_to_csv as to_csv
from bd_layer import crud_class
from service_layer.params_formater import Params_formater
from auth_layer import jwt_class as auth_class

import json

if __name__ == '__main__':

  params = Params_formater(
    crud_class.read_usuarios_fabrica_BD_all(),
    crud_class.read_feriados_e_datas_DB_all(),
    crud_class.read_paginas_de_dados_BD_all()
  )

  params.validar_todas_entradas_do_banco()

  if params.validar_todas_entradas(): 

    offset_numero = 0
    issues_resolved_list = []

    # percorre por 10 paginas com 50 issues cada
    percorre_quantas_paginas = params.quantidade_de_paginas_out()

    url_login = 'https://redmine.iphan.gov.br/redmine/issues.json' 

    login_failed = True

    auth_user = ("bruno.adao", "bLDA1991.")

    qual_mes = "09" 

    qual_ano = "2022"

    dias_feriados = params.feriados_lista_out()

    for i in range(percorre_quantas_paginas):

      url_base = 'https://redmine.iphan.gov.br/redmine'
      projects = '/projects.json'
      issues = '/issues.json'
      issue7400 = "/issues/7400.json"
      notas = 'include=journals'
      sustentacao = 'tracker_id=49'
      status_closed = 'status_id=closed'
      add_filtro = '&'
      iniciarFiltro = '?'
      # 100 sao muitos dados, esbarrou no limite de json de itens (5000)
      limit = 'limit=50'
      offset = 'offset='+ str(offset_numero)

      url_request = url_base + issues + iniciarFiltro + \
        status_closed + add_filtro + limit + add_filtro + offset

      response = requests.get(url_request, auth=auth_user)

      dicionario = response.text

      dicionario_deconding = json.loads(dicionario)

      # criar um arquivo resultado mostrando a resposta de cada pagina
      """
      json_object = json.dumps(dicionario_deconding, indent=4, ensure_ascii=False)

      with open("resultado.json", "w", encoding='utf-8') as outfile:
          outfile.write(json_object)
      """

      # all_issues_list = dicionario["issues"]

      for tarefa in dicionario_deconding["issues"]:
        closed_on = tarefa["closed_on"]
        mes_closed = closed_on[5:7]
        ano_closed = closed_on[0:4]

        created_on = tarefa["created_on"]
        mes_created = created_on[5:7]    
        ano_created = created_on[0:4]

        status = tarefa["status"]["name"]
        tipo = tarefa["tracker"]["name"]
        if (status == "Resolvida") & (mes_closed == str(qual_mes)) & (ano_closed == str(qual_ano)) & (tipo == "Sustentação"):
          issues_resolved_list.append(tarefa["id"])

      offset_numero = offset_numero + 50

    list_of_results = []

    # leandro, rhoxanna, mauricio, cristiano, romao, gestor fabrica, desenvolvedor fabrica, sabino, michel, henrique, testador fabrica, valter, domingos, vinicius
    usuarios_da_fabrica = params.usuarios_fabrica_lista_out()

    for issue in issues_resolved_list:
        list_of_results.append(contador.execute(issue, dias_feriados, auth_user, usuarios_da_fabrica))
    
    to_csv.result_to_csv(issues_resolved_list, list_of_results)
