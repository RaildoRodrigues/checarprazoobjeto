import PySimpleGUI as gui
import requests
import xmltodict
from datetime import datetime

urlinterna = 'http://scppws.correiosnet.int/calculador/CalcPrecoPrazo.asmx/CalcDataMaxima?codigoObjeto='
urlexterna = 'http://ws.correios.com.br/calculador/calcprecoprazo.asmx/CalcDataMaxima?codigoObjeto='

url = urlinterna

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
        self.dias_diferenca = (datetime.today() - data).days
        if(self.dias_diferenca < 0):
            self.color = 'green'
            return 'No Prazo'
        elif(self.dias_diferenca > 0):
            self.color = 'red'
            return 'Vencido'
        else:
            self.color = 'blue'
            return 'Hoje'

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
        layout_data = self.vencimento.strftime("%d/%m/%Y")
        return [[gui.Text(self.codigo), gui.Text(self.dias_diferenca)]]
    

    
#Layouts
frame_layout = [
    [gui.Text('AA123456789BR')],
    [gui.Text('99/99/9999'), gui.Text('Status')]
    ]

window_layout = [
    [gui.Text('Consulta Prazo')],
    [gui.Input(key='codigo', size=(13,1)), gui.Button('checar')],
    [gui.Frame('Objeto', frame_layout)],
    
        ]

window = gui.Window('Checar Prazo', window_layout, size=(300,300))

# Loop Window
while True:   
    event, values = window.read()
    if event == gui.WINDOW_CLOSED: break
    elif event == 'checar':
        on_checar_click(values['codigo'])
window.Close()
