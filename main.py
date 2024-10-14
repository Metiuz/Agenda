from Controls.controls import (
    DateShowDays,
    DateShowDaysWeek,
    Agendamentos,
    Button,
    CalendarioDataPicker,
    dataHoje,
    dataHoje_formatada,
    horaHoje,
    verif_duplicata,
    buscar_dados,
    buscar_dados_filtrados,
    ft
)
import calendar
from datetime import datetime
import sqlite3
from time import sleep

# ### iniciar o banco de dados ###
# conexao = sqlite3.connect('agendamentos.db')
# cursor = conexao.cursor()

# cursor.execute(''' CREATE TABLE agenda_unha (
#                cliente TEXT,
#                tipo_servico TEXT,
#                data_agendamento TEXT,
#                hora_agendamento TEXT
#                )
# ''')
# conexao.commit()
# conexao.close()

def main(pagina: ft.Page):
    pagina.title = 'Agenda'
    pagina.vertical_alignment = ft.MainAxisAlignment.CENTER
    pagina.window.width = 480
    pagina.window.height = 854
    pagina.scroll = True
    pagina.window.icon = ft.icons.ARTICLE
    meses = ['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro']
    tipos_serviço = ['Acrigel','Banho de gel','Pé e mão','Mão','Pé','Postiça Realista','Esmaltação em gel']
    dic_agendamentos = buscar_dados()

    def adicionar_agendamento(e):
        dlg_agendar.content.controls[0].value = ''
        dlg_agendar.content.controls[1].value = tipos_serviço[0]
        dlg_agendar.content.controls[2].controls[1].value = dataHoje_formatada()
        dlg_agendar.content.controls[3].controls[1].value = horaHoje()
        pagina.open(dlg_agendar)
        pagina.update()

    def escolha_mes(e):
        limpar_conteudo()
        preenchimento_dias()
        pagina.update()

    def agendamentos_dia(e):
        mes, ano = data_selecionada()
        self_date = ''
        if e.control.content.controls[0].controls[0].value != '':
            pagina.open(dlg_agendamento)

            if e.control.content.controls[0].controls[0].value in range(1, 10):
                self_date = f'0{e.control.content.controls[0].controls[0].value}/{meses.index(mes)+1}/{ano}'
            else:
                self_date = f'{e.control.content.controls[0].controls[0].value}/{meses.index(mes)+1}/{ano}'

    def data_selecionada() -> tuple[str, int]:
        mes: str = ddmes.value
        ano: int = ddano.value
        return mes, ano
    
    def dias_mes():
        mes, ano = data_selecionada()
        primeiro_dia, total_dias = calendar.monthrange(year=int(ano), month=meses.index(mes)+1)
        return primeiro_dia, total_dias
    
    def preenchimento_dias():
        primeiro_dia, total_dias = dias_mes()
        for day in range(1, total_dias + 1):
            agendados.controls[2].controls[primeiro_dia + day - 1].content.controls[0].controls[0].value = day
    
    def dia_anterior(e):
        mes, ano = data_selecionada()
        limpar_conteudo()
        if meses.index(mes) > 0:
            ddmes.value = meses[meses.index(mes)-1]
        else:
            ddmes.value = meses[11]
            ddano.value = ano - 1
        preenchimento_dias()
        pagina.update()

    def proximo_dia(e):
        mes, ano = data_selecionada()
        limpar_conteudo()
        if meses.index(mes) < 11:
            ddmes.value = meses[meses.index(mes)+1]
        else:
            ddmes.value = meses[0]
            ddano.value = ano + 1
        preenchimento_dias()
        pagina.update()
        
    def limpar_conteudo():
        for i in range(42):
            agendados.controls[2].controls[i].content.value = ''
    
    def abrir_CalendarioDataPicker(e):
        pagina.open(calendario)
        calendario.preenchimento()
        preencher_data_selecionada()
        pagina.update()
    
    def salvar_data(e):
        mes, ano = calendario.data_selecionada()
        dia = calendario.identify_selected_Number()
        mes = meses.index(mes)+1 if meses.index(mes)+1 >= 10 else f'0{meses.index(mes)+1}'
        dlg_agendar.content.controls[2].controls[1].value = f'{dia}/{mes}/{ano}'
        pagina.open(dlg_agendar)
    def fechar_calendario(e):
        pagina.open(dlg_agendar)

    def abrir_TimePicker(e):
        pagina.open(relogio)
        pagina.update()

    def onchange(e):
        print(str(relogio.value)[:5])
        dlg_agendar.content.controls[3].controls[1].value = str(relogio.value)[:5]
        dlg_agendar.update()

    def salvar_DB(e):
        cliente = dlg_agendar.content.controls[0].value
        servico = dlg_agendar.content.controls[1].value
        data = dlg_agendar.content.controls[2].controls[1].value
        hora = dlg_agendar.content.controls[3].controls[1].value
        data_hora = f'{data} {hora}'
        if dlg_agendar.content.controls[0].value != '':
            if verif_duplicata(data_hora):
                dlg_agendar.content.controls[4].value = 'Horário já agendado! Tente outro horário.'
                dlg_agendar.update()
                dlg_agendar.content.controls[4].value = ''
            else:    
                print(f'Cliente: {dlg_agendar.content.controls[0].value}\nTipo serviço: {dlg_agendar.content.controls[1].value}\nData: {dlg_agendar.content.controls[2].controls[1].value}\nHora: {dlg_agendar.content.controls[3].controls[1].value}')
                conexao = sqlite3.connect('agendamentos.db')
                cursor = conexao.cursor()
                cursor.execute(" INSERT INTO agenda_unha VALUES(:cliente, :tipo_servico, :data_agendamento, :hora_agendamento)",
                    {
                        'cliente':str(cliente),
                        'tipo_servico':str(servico),
                        'data_agendamento':str(data),
                        'hora_agendamento':str(hora)
                    })
                conexao.commit()
                conexao.close()
                dlg_agendar.content.controls[4].value = 'Agendado!'
                dlg_agendar.content.controls[4].color = 'blue'
                dlg_agendar.update()
                dlg_agendar.content.controls[4].value = ''
                dlg_agendar.content.controls[4].color = 'red'
        else:
            dlg_agendar.content.controls[4].value = 'Preencha todos os campos!'
            dlg_agendar.update()
            dlg_agendar.content.controls[4].value = ''

    def fechar_agendar(e):
        pagina.close(dlg_agendar)

    def preencher_data_selecionada():
        dia, mes, ano = dlg_agendar.content.controls[2].controls[1].value.split('/')[0], dlg_agendar.content.controls[2].controls[1].value.split('/')[1], dlg_agendar.content.controls[2].controls[1].value.split('/')[2]
        calendario.content.controls[0].controls[1].value = ano
        calendario.content.controls[0].controls[0].value = meses[int(mes)-1]
        for i in range(42):
            if calendario.content.controls[2].controls[i].content.value == int(dia):
                calendario.content.controls[2].controls[i].bgcolor = 'blue'
            
    ddmes = ft.Dropdown(
        width=140,
        value=meses[dataHoje()[1]-1],
        on_change=escolha_mes,
        label ='Mês',
        options=[
            ft.dropdown.Option(text=mes) for mes in meses
        ]
    )
    
    ddano = ft.Dropdown(
        width= 100,
        value=dataHoje()[2],
        on_change=escolha_mes,
        label='Ano',
        options=[
            ft.dropdown.Option(text=anos) for anos in range(1900, 2101, 1)
        ],
    )

    agendados = ft.Column(
        controls=[
            ft.Row(
                width=pagina.window.width,
                controls=[
                    ddmes,
                    ddano,
                    Button(
                        icone=ft.icons.KEYBOARD_ARROW_UP,
                        on_click= dia_anterior
                    ),
                    Button(
                        icone=ft.icons.KEYBOARD_ARROW_DOWN,
                        on_click= proximo_dia
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),
            ft.Row(
                controls=[
                    DateShowDaysWeek(
                        value=value
                    ) for value in ['Seg','Ter','Qua','Qui','Sex','Sáb','Dom']
                ],
                width=pagina.window.width,
                wrap=True,
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=1,
            ),
            ft.Row(
                controls=[
                    DateShowDays(
                        value='',
                        on_click=agendamentos_dia
                    ) for value in range(42)
                ],
                width=pagina.window.width,
                wrap=True,
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=1,
                run_spacing=0.5
            )
        ]
    )
    visao = ft.Column(
        width=pagina.window.width,
        height=pagina.window.height-150,
        controls=[
            ft.Row(
                controls=[
                    ft.ElevatedButton(
                        text='Agendar',
                        icon=ft.icons.ADD,
                        on_click=adicionar_agendamento,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),
            agendados,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=50,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    dlg_agendamento = Agendamentos(
        title=ft.Text(
            value=f'Agendamentos',
            text_align=ft.TextAlign.CENTER,
        ),
        content=ft.Column(
            width=500,
            height=600,
            controls=[

            ]
        ),
        actions=[
            ft.TextButton(
                text='Fechar',
                on_click=lambda e: pagina.close(dlg_agendamento)
            )
        ]
    )

    dlg_agendar = Agendamentos(
        actions=[
            ft.TextButton(
                text='Salvar', on_click=salvar_DB
            ),
            ft.TextButton(
                'Fechar', on_click=fechar_agendar
            )
        ],
        on_dismiss=fechar_agendar,
        content=ft.Column(
            width=500,
            height=350,
            controls=[
                ft.TextField(
                    autofocus=False,
                    capitalization=ft.TextCapitalization.SENTENCES,
                    value='',
                    label='Cliente',
                ),
                ft.Dropdown(
                    value=tipos_serviço[0],
                    label='Serviço',
                    options=[
                        ft.dropdown.Option(text=text) for text in tipos_serviço
                    ]
                ),
                ft.Row(
                    controls=[
                        ft.IconButton(
                            icon=ft.icons.CALENDAR_MONTH,
                            on_click=abrir_CalendarioDataPicker
                        ),
                        ft.Text(
                            value=dataHoje_formatada(),
                            size=16,
                            width= 100,
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ]
                ),
                ft.Row(
                    controls=[
                        ft.IconButton(
                            icon=ft.icons.TIMER,
                            on_click=abrir_TimePicker
                        ),
                        ft.Text(
                            value=horaHoje(),
                            size=16,
                            width= 100,
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ]
                ),
                ft.Text(value='', color='red')
            ]
        )
    )

    calendario = CalendarioDataPicker(
        actions=[
            ft.TextButton(text='Salvar', on_click=salvar_data),
            ft.TextButton(text='Fechar', on_click=fechar_calendario),
        ],
        on_dismiss=fechar_calendario
    )

    relogio = ft.TimePicker(
        confirm_text="Confirmar",
        error_invalid_text="Hora inválida",
        help_text="Escolha o horário",
        on_change=onchange,
    )
    
    pagina.add(
        visao,
    )
    
    preenchimento_dias()
    pagina.update()
    print('Iniciando!')
if __name__ == '__main__':
    ft.app(target=main, assets_dir="assets")