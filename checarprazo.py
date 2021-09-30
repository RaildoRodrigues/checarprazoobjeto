import PySimpleGUI as gui

def on_checar_click(codigo):
    print(codigo)
    
def object_block_layout(codigo, data_entrega):
    return [[gui.Text(codigo), gui.Text(data_entrega)]]
    
# Window Layout    
layout = [
    [gui.Text('Código de rastreamento')],
    [gui.Input(key='codigo', size=(13,1)), gui.Button('checar')],
    [gui.Column([],key='lista')]
        ]
window = gui.Window('Checar Prazo', layout, size=(300,300))

# Loop Window
while True:   
    event, values = window.read()
    if event == gui.WINDOW_CLOSED: break
    elif event == 'checar':
        on_checar_click(values['codigo'])
window.Close()
