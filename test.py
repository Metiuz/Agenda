import flet as ft
from datetime import datetime
import sqlite3

# def main(pagina: ft.Page):
#     pagina.title = 'test'

#     lista = ft.Dropdown(options=['Janeiro','Fevereiro'])

#     pagina.add(lista)
# ft.app(main)

# def dataHoje():
#     dia = str(datetime.today())[:10].split('-')[2]
#     mes = str(datetime.today())[:10].split('-')[1]
#     ano = str(datetime.today())[:10].split('-')[0]
#     print(f'{dia}/{mes}/{ano}')

# dataHoje()

# def horaHoje():
#     hora = str(datetime.today())[11:16]
#     return hora

# horaHoje()

# def verif_duplicata(checar):
#     data_hora = []
#     conexao = sqlite3.connect('agendamentos.db')
#     cursor = conexao.cursor()
#     data = cursor.execute("SELECT data_agendamento FROM agenda_unha")
#     data = data.fetchall()
#     hora = cursor.execute("SELECT hora_agendamento FROM agenda_unha")
#     hora = hora.fetchall()
#     for i in range(len(data)):
#         data_hora.append(f'{data[i][0]} {hora[i][0]}')
#     conexao.close()
#     return checar in data_hora
    

# if verif_duplicata('11/10/2024 05:18'):
#     print('Sim')
# else:
#     print('Não')

def buscar_dados_filtrados(data_filtro):
    conexao = sqlite3.connect('agendamentos.db')
    cursor = conexao.cursor()
    dados = cursor.execute(f"SELECT * FROM agenda_unha WHERE data_agendamento= '{data_filtro}'")
    dados = dados.fetchall()
    dic_agendamentos = {
        'cliente':[],
        'tipo_servico':[],
        'data':[],
        'hora':[]
    }
    for i in range(len(dados)):
        dic_agendamentos['cliente'].append(dados[i][0])
        dic_agendamentos['tipo_servico'].append(dados[i][1])
        dic_agendamentos['data'].append(dados[i][2])
        dic_agendamentos['hora'].append(dados[i][3])
    conexao.close()
    return dic_agendamentos

buscar_dados_filtrados('11/10/2024')