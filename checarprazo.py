import PySimpleGUI as gui
from PySimpleGUI.PySimpleGUI import Text, rgb
import requests
import xmltodict
from datetime import date, datetime

urlinterna = 'http://scppws.correiosnet.int/calculador/CalcPrecoPrazo.asmx/CalcDataMaxima?codigoObjeto='
urlexterna = 'http://ws.correios.com.br/calculador/calcprecoprazo.asmx/CalcDataMaxima?codigoObjeto='

url = urlexterna

gui.theme('Reddit')


def on_checar_click(codigo_objeto):
    novo_objeto = ObjetoPostal(codigo_objeto)
    window.extend_layout(window['lista'], novo_objeto.layout())

class ObjetoPostal:

    def __init__(self, codigo_postal):
        dados_postais = self.request_dict_dados_postais(codigo_postal)
        self.codigo = dados_postais['codigo']
        self.ultimo_evento = dados_postais['descricaoUltimoEvento']
        self.erro = dados_postais['msgErro']
        self.vencimento = self.get_vencimento_from_string(dados_postais['dataMaxEntrega'])
        self.status = self.get_status(self.vencimento)
        self.color = None
    
    def print_object(self):
        print('Código: ' , self.codigo)
        print('Status: ', self.status)
        print('Vencimento: ' , self.vencimento)


    def get_status(self, data):
        if(data > date.today()):
            self.color = 'green'
            return 'No Prazo'
        elif(data < date.today()):
            self.color = 'red'
            return 'Vencido'
        elif(data == date.today()):
            self.color = 'blue'
            return 'Hoje'

    def get_vencimento_from_string(self, string_data):
        if (string_data != None):
            return datetime.strftime(string_data, '%d/%m/%y %H:%M:%S')
        else:
            return date.today()

    def request_dict_dados_postais(self, codigo_postal):
        get_xml = requests.get(url + codigo_postal)
        dict_objeto_postal = xmltodict.parse(get_xml.text)
        return dict_objeto_postal['cResultadoObjeto']['Objetos']['cObjeto']
    
    def layout(self):
        layout_data = self.vencimento.strftime("%d/%m/%Y")
        return [[gui.Text(self.codigo, text_color=self.color), gui.Text(layout_data, background_color=self.color)]]
    

    
# Window Layout    
layout = [
    [gui.Text('Código de rastreamento')],
    [gui.Input(key='codigo', size=(13,1)), gui.Button('checar')],
    [gui.Column([],key='lista', size=(24,1))]
        ]
window = gui.Window('Checar Prazo', layout, size=(300,300))

# Loop Window
while True:   
    event, values = window.read()
    if event == gui.WINDOW_CLOSED: break
    elif event == 'checar':
        on_checar_click(values['codigo'])
window.Close()




