import PySimpleGUI as gui
import requests

url = 'scppws.correiosnet.int/calculador/CalcPrecoPrazo.asmx/CalcDataMaxima?codigoObjeto='

def request_object_prazo(codigo_objeto):
    resultado = requests.get(url + codigo_objeto)
    return resultado

def on_checar_click(codigo_objeto):
    print(request_object_prazo(codigo_objeto))
    #add_objeto_block_layout(codigo_objeto, '23/05/2021')
    
def add_objeto_block_layout(codigo_objeto, data_entrega):
    block = [[gui.Text(codigo_objeto), gui.Text(data_entrega)]]
    window.extend_layout(window['lista'], block)
    
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
