import PySimpleGUI as gui
import requests
import xmltodict
from datetime import datetime

urlinterna = 'http://scppws.correiosnet.int/calculador/CalcPrecoPrazo.asmx/CalcDataMaxima?codigoObjeto='
urlexterna = 'http://ws.correios.com.br/calculador/calcprecoprazo.asmx/CalcDataMaxima?codigoObjeto='

url = urlinterna
lista_objetos = []
lista_colors = []

class ObjetoPostal:

    def __init__(self, codigo_postal):
        dados_postais = self.request_dict_dados_postais(codigo_postal)
        self.codigo = self.validate_codigo(dados_postais['codigo'])
        self.ultimo_evento = dados_postais['descricaoUltimoEvento']
        self.erro = dados_postais['msgErro']
        self.vencimento = self.get_vencimento_from_string(dados_postais['dataMaxEntrega'])
        self.vencimento_formatado = self.vencimento.strftime("%d/%m/%Y")
        self.tipo = self.validate_servico(dados_postais['servico'])
        self.color = None
        self.bg_color = None
        self.status = self.get_status(self.vencimento)
        self.check_erro()


    def validate_servico(self, servico_string):
        try:
            return dicionario_de_tipos[servico_string]
        except:
            return ''

    def validate_codigo(self, code_string):
        if code_string == None:
            return 'VAZIO'
        else:
            return code_string[:13].upper()

    def check_erro(self):
        if self.erro != None:
            self.codigo = 'ERRO'
            self.vencimento_formatado = ''
            self.tipo = ''
            self.ultimo_evento = ''
            self.color = 'black'
            self.bg_color = 'salmon'
            self.status = self.erro
    
    def print_object(self):
        print('Código: ' , self.codigo)
        print('Status: ', self.status)
        print('Vencimento: ' , self.vencimento.strftime("%d/%m/%Y"))


    def get_status(self, data):
        self.dias_diferenca = (datetime.today() - data).days
        hoje = datetime.today().date()
        vencimento = data.date()
        if(vencimento > hoje):
            self.color = 'dark green'
            self.bg_color = 'pale green'
            return 'No Prazo'
        elif(vencimento < hoje):
            self.color = 'red'
            self.bg_color = 'dark salmon'
            return 'Vencido'
        else:
            self.color = 'dark blue'
            self.bg_color = 'light blue'
            return 'Entregar Hoje'

    def get_vencimento_from_string(self, string_data):
        if (string_data != None):
            return datetime.strptime(string_data, '%d/%m/%Y %H:%M')
        else:
            return datetime.today()

    def request_dict_dados_postais(self, codigo_postal):
        try:
            get_xml = requests.get(url + codigo_postal)
            dict_objeto_postal = xmltodict.parse(get_xml.text)
            return dict_objeto_postal['cResultadoObjeto']['Objetos']['cObjeto']
        except:
            gui.popup('erro de conexão')
    
    def layout(self):
        return [self.codigo, self.vencimento_formatado, self.status]
  
#Layouts
gui.theme('Reddit')

menu_layout = [['Ajuda', ['Instruções::help', 'Sobre::sobre']]]

frame_layout = [
    [gui.Text('', key='-frame_codigo-', font='Helvetica 30 bold', size=(26,2),expand_y=True ,expand_x=True,justification='center', pad=0)],
    [gui.Text('', key='-frame_data-', font='Helvetica 24', size=(26,2),expand_y=True ,expand_x=True,justification='center',pad=0)],
    [gui.Text('', key='-frame_tipo-', size=(36,1))],
    [gui.Text('', key='-frame_status-', size=(36,2))],
    [gui.Text('', key='-frame_evento-', size=(36,1))]
    ]

window_layout = [
    [gui.Menu(menu_layout)],
    [gui.Text('Consulta Prazo')],
    [gui.Input(key='codigo', size=(26,1), focus=True), gui.Button('checar',bind_return_key=True )],
    [gui.Frame('Objeto', frame_layout, element_justification='c', key=('-frame-'))],
    [gui.Table([['','','']], headings=['   OBJETO   ', 'VENCIMENTO', '    SITUAÇÃO    '], key='-table-', justification = "left")]
    
        ]

window = gui.Window('Checar Prazo', window_layout, size=(420,480), icon='verificaprazo.ico')



def on_checar_click(codigo_objeto):
    carregando()
    novo_objeto = ObjetoPostal(codigo_objeto)
    update_frame(novo_objeto)
    clear_input()
    lista_objetos.insert(0, novo_objeto.layout())
    lista_colors.insert(0, novo_objeto.bg_color)
    update_table()

def carregando():
    window['-frame_codigo-'].update('carregando...')
    window['-frame_codigo-'].update(text_color='black')
    window['-frame_codigo-'].update(background_color='white')
    window['-frame_data-'].update(background_color='white')
    window['-frame_data-'].update('')
    window['-frame_status-'].update('')
    window['-frame_tipo-'].update('')
    window['-frame_evento-'].update('')
    window.finalize()


def update_table():
    window['-table-'].update(values=lista_objetos)
    for i in range(len(lista_colors)):
        window['-table-'].update(row_colors=[(i, lista_colors[i])])

  

def clear_input():
    window['codigo'].update('')
    window['codigo'].focus = True

def update_frame(novo_objeto):
    #alterar textos
    window['-frame_codigo-'].update(novo_objeto.codigo)
    window['-frame_data-'].update(novo_objeto.vencimento_formatado)
    window['-frame_status-'].update('Situação: ' + novo_objeto.status)
    window['-frame_tipo-'].update('Tipo: ' + novo_objeto.tipo)
    window['-frame_evento-'].update('Evento: ' + novo_objeto.ultimo_evento)
    #alterar cor da fonte
    window['-frame_codigo-'].update(text_color=novo_objeto.color)
    window['-frame_data-'].update(text_color=novo_objeto.color)
    #alterar background
    window['-frame_codigo-'].update(background_color=novo_objeto.bg_color)
    window['-frame_data-'].update(background_color=novo_objeto.bg_color)

def carregar_tipos_postais():
    tipos_url = 'http://ws.correios.com.br/calculador/calcprecoprazo.asmx/ListaServicos?'
    xml = requests.get(tipos_url)
    lista_de_tipos = xmltodict.parse(xml.text)['cResultadoServicos']['ServicosCalculo']['cServicosCalculo']
    dicionario_de_tipos = {}
    for tipo in lista_de_tipos:
        dicionario_de_tipos[tipo['codigo']] = tipo['descricao']
    return dicionario_de_tipos

try:
    dicionario_de_tipos = carregar_tipos_postais()
except:
    gui.popup('Erro ao carregar tipos postais')
    dicionario_de_tipos = {}
    #window.close()


# Loop Window

while True:   
    event, values = window.read()
    if event == gui.WINDOW_CLOSED: break
    elif event == 'checar':
        on_checar_click(values['codigo'])
    elif event == 'Instruções::help':
        text = """Essa aplicação é auxiliar, ela não substitui nenhum sistema dos correios, é utilizada para verificar o prazo de entrega de objetos postais, todos os dados são retirados da própia API dos correios, disponível em:
http://ws.correios.com.br/calculador/calcprecoprazo.asmx
        """
        gui.popup(text,icon='verificaprazo.ico', title='Instruções')
    elif event == 'Sobre::sobre':
        gui.popup('tecnologia utilizada: python\nerros e dúvidas: raildorcv@correios.com.br', icon='verificaprazo.ico', title='Sobre')
window.Close()

