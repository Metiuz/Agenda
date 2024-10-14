import flet as ft
import calendar
from datetime import datetime
from typing import Any, List, Optional
from flet_core.control import Control
from flet_core.types import OptionalEventCallable
import sqlite3

meses = ['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro']
horas = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24']

class DateShowDaysWeek(ft.Container):
    def __init__(
        self,
        value: str
    ):
        super().__init__()
        self.width = 385 / 7
        self.height = 385 / 7
        self.border_radius = 3
        self.border = ft.border.all(
            width=0.5,
            color='#00003c'
        )
        self.content = ft.Text(
            value=value,
            color=ft.colors.BLACK,
            size=14,
            weight='bold',
            text_align=ft.TextAlign.CENTER
        )
        self.alignment=ft.alignment.center
        self.bgcolor=ft.colors.GREY
        
class DateShowDays(ft.Container):
    def __init__(
        self,
        value: str,
        on_click: ft.ControlEvent
    ):
        super().__init__()
        self.width = 385 / 7
        self.height = 385 / 7
        self.border_radius = 3
        self.border = ft.border.all(
            width=0.5,
            color=ft.colors.WHITE
        )
        self.content = ft.Column(
            width= self.width,
            height=self.height,
            controls=[
                ft.Row(
                    width=self.width,
                    # height=15,
                    controls=[ft.Text(
                        value=value,
                        color=ft.colors.WHITE,
                        size=14,
                        weight='bold',
                        text_align=ft.TextAlign.LEFT
                    )]
                ),
                ft.Icon(
                    name=None,size=30
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0
        )
        self.alignment=ft.alignment.top_left
        self.padding = 3
        self.on_click= on_click
    


def dataHoje():
    dia = int(str(datetime.today())[:10].split('-')[2])
    mes = int(str(datetime.today())[:10].split('-')[1])
    ano = int(str(datetime.today())[:10].split('-')[0])
    return dia, mes, ano

def dataHoje_formatada():
    dia = int(str(datetime.today())[:10].split('-')[2])
    mes = int(str(datetime.today())[:10].split('-')[1])
    ano = int(str(datetime.today())[:10].split('-')[0])
    if dia in range(1, 10):
        data_formatada = f'0{dia}/{mes}/{ano}'
    else:
        data_formatada = f'{dia}/{mes}/{ano}'
    return data_formatada

def horaHoje():
    hora = str(datetime.today())[11:16]
    return hora

def verif_duplicata(checar):
    data_hora = []
    conexao = sqlite3.connect('agendamentos.db')
    cursor = conexao.cursor()
    data = cursor.execute("SELECT data_agendamento FROM agenda_unha")
    data = data.fetchall()
    hora = cursor.execute("SELECT hora_agendamento FROM agenda_unha")
    hora = hora.fetchall()
    for i in range(len(data)):
        data_hora.append(f'{data[i][0]} {hora[i][0]}')
    conexao.close()
    return checar in data_hora

def buscar_dados():
    conexao = sqlite3.connect('agendamentos.db')
    cursor = conexao.cursor()
    dados = cursor.execute("SELECT * FROM agenda_unha")
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

class Agendamentos(ft.AlertDialog):
    def __init__(
            self,
            title: ft.Text = None,
            content: Optional[Control] = None,
            actions: Optional[List[Control]] = None,
            on_dismiss: OptionalEventCallable = None
    ):
        super().__init__()
        self.open=False
        self.modal = False
        self.title = title
        self.content = content
        self.actions = actions
        self.on_dismiss = on_dismiss

class Button(ft.IconButton):
    def __init__(
            self,
            icone: ft.icons,
            on_click: ft.ControlEvent
    ):
        super().__init__()
        self.icon = icone
        self.icon_size = 50
        self.icon_color = ft.colors.GREY
        self.on_click = on_click

class CalendarioDataPicker(ft.AlertDialog):
    def __init__(
            self,
            actions: Optional[List[Control]] = None,
            on_dismiss: OptionalEventCallable = None
    ):
        super().__init__()
        self.title = ft.Text(
            value='Selecione uma data',
            text_align=ft.TextAlign.CENTER,
        )
        self.modal = False,
        self.on_dismiss = on_dismiss
        self.content = ft.Column(
            width=300,
            height=350,
            # alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                # Controles
                ft.Row(
                    spacing=4,
                    controls=[
                        ft.Dropdown(
                            width=100,
                            value=meses[dataHoje()[1]-1],
                            text_size=12,
                            label ='Mês',
                            on_change=self.on_change,
                            options=[
                                ft.dropdown.Option(text=mes) for mes in meses
                            ]
                        ),
                        ft.Dropdown(
                            width= 80,
                            value=dataHoje()[2],
                            text_size=12,
                            label='Ano',
                            on_change=self.on_change,
                            options=[
                                ft.dropdown.Option(text=anos) for anos in range(1900, 2101, 1)
                            ],
                        ),
                        ft.IconButton(
                            icon=ft.icons.KEYBOARD_ARROW_LEFT,
                            icon_size=28,
                            icon_color="white",
                            on_click=self.mes_anterior
                        ),
                        ft.IconButton(
                            icon=ft.icons.KEYBOARD_ARROW_RIGHT,
                            icon_size=28,
                            icon_color="white",
                            on_click=self.mes_posterior
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                # Dias da Semana do calendário
                ft.Row(
                    wrap=True,
                    controls=[
                        ft.Container(
                            width=220/7,
                            height=220/7,
                            content=ft.Text(
                                value=dias,
                                size=18,
                                weight='bold',
                                text_align=ft.TextAlign.CENTER
                            ),
                            padding=0
                        )for dias in ['S','T','Q','Q','S','S','D']
                    ]
                ),
                # Dias do mês do calendário
                ft.Row(
                    wrap=True,
                    run_spacing=10,
                    controls=[
                       ft.Container(
                           width=220/7,
                           height=220/7,
                           alignment=ft.alignment.center,
                           border_radius=100,
                           content=ft.Text(
                               value='',
                               size=14,
                               text_align=ft.TextAlign.CENTER
                           ),
                           on_click=self.hover_selecionado,
                           padding=0,
                           ink=False
                       ) for _ in range(42)
                    ]
                )
            ]
        )
        self.actions = actions
        self.actions_alignment = ft.MainAxisAlignment.END

    def hover_selecionado(self, e):
        if e.control.content.value != '':
            for i in range(42):
                self.content.controls[2].controls[i].bgcolor = None
            if e.control.bgcolor == None or e.control.bgcolor =="":
                e.control.bgcolor = "blue"
            else:
                e.control.bgcolor = None
            self.update()

    def identify_selected_Number(self) -> tuple[int]:
        for i in range(42):
            if self.content.controls[2].controls[i].bgcolor == 'blue':
                selected = self.content.controls[2].controls[i].content.value if self.content.controls[2].controls[i].content.value >= 10 else f'0{self.content.controls[2].controls[i].content.value}'
                break
        return selected

    def limpar_datas(self):
        for i in range(42):
            self.content.controls[2].controls[i].content.value = ''

    def data_selecionada(self) -> tuple[str, int]:
        mes: str = self.content.controls[0].controls[0].value
        ano: int = self.content.controls[0].controls[1].value
        return mes, ano
    
    def dias_mes(self):
        mes, ano = self.data_selecionada()
        primeiro_dia, total_dias = calendar.monthrange(year=int(ano), month=meses.index(mes)+1)
        return primeiro_dia, total_dias
    
    def preenchimento(self):
        primeiro_dia, total_dias = self.dias_mes()
        for day in range(1, total_dias + 1):
            self.content.controls[2].controls[primeiro_dia + day - 1].content.value = day

    def on_change(self, e):
        self.limpar_datas()
        self.preenchimento()
        self.update()

    def mes_anterior(self, e):
        mes, ano = self.data_selecionada()
        self.limpar_datas()
        if meses.index(mes) > 0:
            self.content.controls[0].controls[0].value = meses[meses.index(mes)-1]
        else:
            self.content.controls[0].controls[0].value = meses[11]
            self.content.controls[0].controls[1].value = ano - 1
        self.preenchimento()
        self.update()

    def mes_posterior(self, e):
        mes, ano = self.data_selecionada()
        self.limpar_datas()
        if meses.index(mes) < 11:
            self.content.controls[0].controls[0].value = meses[meses.index(mes)+1]
        else:
            self.content.controls[0].controls[0].value = meses[0]
            self.content.controls[0].controls[1].value = ano + 1
        self.preenchimento()
        self.update()
