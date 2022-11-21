import csv
from random import randint

def sort_dict_logins(e):
  lower_login = e['login'].lower()
  return lower_login

def sort_dict_dias(e):
  lower_login = e['dia'].lower()
  return lower_login

def result_to_json(list_issues, list_results):

    # result retorno
    # types_of_priorities[str(journals_priority)], sla_result, delta_time_sla, diff_sla, atuou_em_feriados_ou_finais_de_semana, primeira_atribuicao 

    if (len(list_issues) == len(list_results)):

        list_rows = []

        for i in range(len(list_issues)):

            passou_result = "-"
            sla_result = "Nao"
            tempo_liquido = ""
            prioridade_tipo = list_results[i][0] 

            if list_results[i][1] == 0 :
                passou_result = to_hours(list_results[i][3]) 

            if list_results[i][1] == 1 :
                sla_result = "Sim"    
            
            if list_results[i][1] == 2 :
                sla_result = "NAO ATUOU"

            if str(prioridade_tipo) == "Baixa":
               tempo_liquido = "36h" 

            elif str(prioridade_tipo) == "Normal":
                tempo_liquido = "24h"

            else:
                tempo_liquido = "12h"
                prioridade_tipo = "Alta"
            
            dict_row = {
                "Sistema": str(list_results[i][5]),
                "Tarefa": str(list_issues[i]),
                "Prioridade":str(prioridade_tipo),
                "Data de atribuicao": str(list_results[i][6]),
                "Tempo Liquido":str(tempo_liquido),
                "Data de entrega para Homologacao": str(list_results[i][7]),
                "Data de alterado para Resolvido": str(list_results[i][8]),
                "Delta_tempo":to_hours(list_results[i][2]),
                "IPS(horas uteis de atraso)": passou_result,
                "Nivel de serviço dentro do acordo?": sla_result,
                "Feriado":str(list_results[i][4]) 
                }
            
            list_rows.append(dict_row)


        return([200, list_rows]) 

    else:
        return([424,[{"error": "Por algum motivo a lista de tarefas esta maior que a lista de resultados da análise, arquivo não foi gerado"}]])

def to_hours(string_data):

    string_data = str(string_data)

    tamanho = len(string_data)
    horas_formatada = string_data

    dias_list = []
    dias_str = ""
    dias_num = 0
    i = 0

    if tamanho > 8:

        while string_data[i] != " ":
            dias_list.append(string_data[i])
            i += 1

        for letra in dias_list:
            dias_str = dias_str + str(letra)  
        
        dias_num = int(dias_str)

        divisao = string_data.split(", ")

        hours_minutes_seconds = divisao[1].split(":")

        dias_totais_pre = 24 * dias_num

        dias_totais_pos = dias_totais_pre + int(hours_minutes_seconds[0])

        horas_formatada = "{}:{}:{}".format(str(dias_totais_pos), str(hours_minutes_seconds[1]), str(hours_minutes_seconds[2]))

    return horas_formatada