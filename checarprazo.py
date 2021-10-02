import PySimpleGUI as gui
import requests
import xmltodict
from datetime import datetime

urlinterna = 'http://scppws.correiosnet.int/calculador/CalcPrecoPrazo.asmx/CalcDataMaxima?codigoObjeto='
urlexterna = 'http://ws.correios.com.br/calculador/calcprecoprazo.asmx/CalcDataMaxima?codigoObjeto='

url = urlexterna
lista_objetos = []

gui.theme('Reddit')

class ObjetoPostal:

    def __init__(self, codigo_postal):
        dados_postais = self.request_dict_dados_postais(codigo_postal)
        self.codigo = dados_postais['codigo']
        self.ultimo_evento = dados_postais['descricaoUltimoEvento']
        self.erro = dados_postais['msgErro']
        self.vencimento = self.get_vencimento_from_string(dados_postais['dataMaxEntrega'])
        self.vencimento_formatado = self.vencimento.strftime("%d/%m/%Y")
        self.status = self.get_status(self.vencimento)
        self.color = None
        
    
    def print_object(self):
        print('Código: ' , self.codigo)
        print('Status: ', self.status)
        print('Vencimento: ' , self.vencimento.strftime("%d/%m/%Y"))


    def get_status(self, data):
        self.dias_diferenca = (datetime.today() - data).days
        if(self.dias_diferenca < 0):
            self.color = 'green'
            return 'No Prazo'
        elif(self.dias_diferenca > 0):
            self.color = 'red'
            return 'Vencido'
        else:
            self.color = 'blue'
            return 'Entregar Hoje'

    def get_vencimento_from_string(self, string_data):
        if (string_data != None):
            return datetime.strptime(string_data, '%d/%m/%Y %H:%M')
        else:
            return datetime.today()

    def request_dict_dados_postais(self, codigo_postal):
        get_xml = requests.get(url + codigo_postal)
        dict_objeto_postal = xmltodict.parse(get_xml.text)
        return dict_objeto_postal['cResultadoObjeto']['Objetos']['cObjeto']
    
    def layout(self):
        return [self.codigo, self.vencimento_formatado, self.status]
  
#Layouts
frame_layout = [
    [gui.Text('AA123456789BR', key='-frame_codigo-', font='Helvetica 24', size=(26,1))],
    [gui.Text('99/99/9999', key='-frame_data-'), gui.Text('Status', key='-frame_status-')]
    ]

window_layout = [
    [gui.Text('Consulta Prazo')],
    [gui.Input(key='codigo', size=(26,1), focus=True), gui.Button('checar',bind_return_key=True )],
    [gui.Frame('Objeto', frame_layout, element_justification='c', key=('-frame-'))],
    [gui.Table([['','','']], headings=['OBJETO', 'VENCIMENTO', 'SITUAÇÃO'], key='-table-')]
    
        ]

window = gui.Window('Checar Prazo', window_layout, size=(400,300))


def on_checar_click(codigo_objeto):
    novo_objeto = ObjetoPostal(codigo_objeto)
    update_frame(novo_objeto)
    clear_input()
    lista_objetos.insert(0, novo_objeto.layout())
    update_table()

def update_table():
    window['-table-'].update(values=lista_objetos)

def clear_input():
    window['codigo'].update('')
    window['codigo'].focus = True

def update_frame(novo_objeto):
    window['-frame_codigo-'].update(novo_objeto.codigo)
    window['-frame_data-'].update(novo_objeto.vencimento_formatado)
    window['-frame_status-'].update(novo_objeto.status)



# Loop Window
while True:   
    event, values = window.read()
    if event == gui.WINDOW_CLOSED: break
    elif event == 'checar':
        on_checar_click(values['codigo'])
window.Close()




