import PySimpleGUI as gui
import requests
import xmltodict
from datetime import datetime, timedelta
import re


tipos_postais = {'02259': 'MD COM GEOMARKETING POR REGIAO', '02267': 'MD COM GEOMARKETING ENDERECADA',
                 '02275': 'MD COM GEOMARKETING ENDERECADA', '04014': 'SEDEX A VISTA', '04022': 'SEDEX ON LINE A VISTA',
                 '04030': 'PAC ON LINE A VISTA', '04065': 'SEDEX A VISTA PGTO NA ENTREGA', '04073': 'SPP A VISTA E A FATURAR',
                 '04081': 'SPP A VISTA E A FATURAR', '04103': 'COMBO SEDEX A VISTA', '04138': 'SEDEX CONTRATO GRAND FORMATOS',
                 '04146': 'SEDEX CONTR GRAND FORMATOS LM', '04154': 'SEDEX CONTRATO AGENCIA LM', '04162': 'SEDEX CONTRATO AGENCIA',
                 '04170': 'SEDEX REVERSO ESPELHO 04162', '04189': 'SEDEX CONTR AGENCIA PAGTO ENTR', '04197': 'COMBO SEDEX CONTRATO AGENCIA',
                 '04227': 'CORREIOS MINI ENVIOS CTR AG', '04243': 'SEDEX REVERSO 04170 LM', '04251': 'SEDEX CONTR AG PAGTO ENTREG LM',
                 '04278': 'SEDEX CONTRATO UO LM', '04308': 'PAC CONTR AG PAGTO ENTREGA LM', '04316': 'SEDEX CONTRATO - UO',
                 '04332': 'PAC CONTRATO UO LM', '04340': 'COMBO SEDEX CONT AG AR ELET LM', '04359': 'COMBO SEDEX CONTRATO AGENCI LM',
                 '04367': 'PAC CONTRATO AGENCIA LM', '04375': 'PAC REVERSO 04677 LM', '04383': 'PAC CONTR GRANDES FORMATOS LM',
                 '04405': 'SEDEX 12 SCADA A VISTA', '04413': 'SEDEX 12 REVERSO SGPB A FATURA', '04421': 'SEDEX 10 SCADA A VISTA',
                 '04430': 'SEDEX HOJE SCADA  A VISTA FATU', '04448': 'SEDEX HOJE REVERSO SGPB FATURA', '04456': 'COMBO SEDEX 10 SCADA A VISTA',
                 '04464': 'COMBO SEDEX HOJE SCADA VIST FA', '04472': 'COMBO SEDEX 12 SCADA A VISTA', '04499': 'COMBO SEDEX 12 AR ELETR SCADA',
                 '04502': 'COMBO SEDEX 10 AR ELETR SCADA', '04510': 'PAC A VISTA', '04529': 'COMBO SEDEX HOJE AR ELET SCADA',
                 '04537': 'SEDEX CONTRATO GRANDES FORMATO', '04553': 'SEDEX CONTRATO AGENCIA TA', '04561': 'SEDEX CONT AG PAG ENT TA',
                 '04588': 'COMBO SEDEX CONT AG TA', '04596': 'PAC CONTRATO AGENCIA TA', '04600': 'PAC CONT AG PAG ENT TA',
                 '04618': 'PAC CONTRATO GRANDES FORMATOS', '04669': 'PAC CONTRATO AGENCIA', '04677': 'PAC REVERSO ESPELHO 04669',
                 '04685': 'PAC CONTRATO AGENCIA PAGTO ENT', '04693': 'PAC CONTRATO GRANDES FORMATOS',
                 '04707': 'PAC A VISTA PAGTO NA ENTREGA', '04715': 'COMBO PAC A VISTA', '04812': 'PAC CONTRATO - UO',
                 '04839': 'COMBO SEDEX A VISTA AR ELETRON', '04901': 'COMBO SEDEX A VISTA EMBALAGEM', '04910': 'COMBO PAC A VISTA EMBALAGEM',
                 '04928': 'SEDEX REVERSO TA ESPELHO 04553', '04936': 'PAC REVERSO TA ESPELHO 04596',
                 '10014': 'CARTA SIMPLES A VISTA', '10022': 'CARTA SOCIAL', '10030': 'CARTA REGISTRADA VISTA SELO SE',
                 '10057': 'CARTA FATURAR OP ACIMA 500 GR', '10065': 'CARTA A FATURAR CHANCELA',
                 '10073': 'CARTA AGF OP', '10081': 'CARTA REGISTRADA O3 ETIQ', '10090': 'CARTA REGISTRADA PR1 SELO E SE',
                 '10120': 'CARTA SIMPLES ADMINISTRATIVA', '10138': 'CARTA REG FAT ETIQ', '10146': 'CARTA REG MOD FAT ETIQ',
                 '10154': 'CARTA REGISTRADA O1 ETIQ', '10162': 'CARTA REGISTRADA O2 ETIQ', '10189': 'E-CARTA A4 MON RG-FAIXA 1',
                 '10200': 'CARTA REGISTRADA PL3', '10456': 'E-CARTA A4 MON RG ARD-FAIXA 1', '10499': 'E-CARTA A4 MON RG ARD-FAIXA 5',
                 '10502': 'E-CARTA A4 MON RG ARD-FAIXA 6', '10510': 'E-CARTA A4 MON RG ARD-FAIXA 7', '10570': 'E-CARTA A4 MON RG ARD-FAIXA 13',
                 '10600': 'E-CARTA A4 MON RG ARD-FAIXA 15', '10669': 'E-CARTA A4 MON RG ARD-FX 15', '10707': 'CARTA COM REG CTR EP MÁQ FRAN',
                 '10715': 'CARTA COM SIMPLES CTO MÁQ FRAN', '10723': 'CARTA COM REG MOD CTO EP MÁQ F', '10987': 'REGISTRADO ADMINISTRATIVO',
                 '11711': 'CARTA REGISTRADA C AR B1', '11720': 'CARTA REGISTRADA C AR PR1', '11835': 'CARTA REGISTRADA O3', '11843': 'CARTA REGISTRADA O4',
                 '11851': 'CARTA REGISTRADA PL1', '11860': 'E-CARTA TABELA BASE ECD', '11878': 'E-CARTA TABELA BASE ECR',
                 '11886': 'E-CARTA ECD 01', '11894': 'E-CARTA ECD 02', '11908': 'E-CARTA ECD 03', '11916': 'E-CARTA ECD 04',
                 '11924': 'E-CARTA ECR 01', '11932': 'E-CARTA ECR 02', '11940': 'E-CARTA ECR 03', '11959': 'E-CARTA ECR 04',
                 '11967': 'E-CARTA SIMPLES ECS 01', '11975': 'E-CARTA SIMPLES ECS 02', '11983': 'E-CARTA SIMPLES TB ECS',
                 '11991': 'POSTAL RESPOSTA', '12165': 'POSTAL RESPOSTA DPVAT', '12203': 'COMBO MDB LOCAL CHANCELA E PP',
                 '12211': 'COMBO MDB ESTADUAL CHANC E PP', '12220': 'COMBO MDB NACIONAL CHANC E PP', '12227': 'COMBO MDE LOCAL +PP FX2',
                 '12238': 'COMBO MDE LOCAL +PP FX1', '12254': 'COMBO MDE ESTADUAL + PP FX1', '12262': 'COMBO MDE NACIONAL +PP FX1',
                 '12289': 'COMBO MDE ESTADUAL +PP FX2', '12297': 'COMBO MDE NACIONAL +PP FX2', '12300': 'COMBO MDE LOCAL +PP FX3',
                 '12319': 'COMBO MDE ESTADUAL +PP FX3', '12327': 'COMBO MDE NACIONAL +PP FX3', '12335': 'COMBO MDE LOCAL +PP FX4',
                 '12351': 'COMBO MDE ESTADUAL +PP FX4', '12360': 'COMBO MDE NACIONAL +PP FX4', '12378': 'COMBO MDE LOCAL +PP FX5',
                 '12386': 'COMBO MDE ESTADUAL +PP FX5', '12394': 'COMBO MDE NACIONAL +PP FX5', '12416': 'COMBO MDE LOCAL +PP FX6',
                 '12424': 'COMBO MDE ESTADUAL +PP FX6', '12432': 'COMBO MDE NACIONAL +PP FX6', '12440': 'COMBO MDE LOCAL +PP FX7',
                 '12459': 'COMBO MDE ESTADUAL +PP FX7', '12467': 'COMBO MDE NACIONAL +PP FX7', '12483': 'CARTA REGISTRADA A VISTA',
                 '12491': 'CARTA REGISTRO MODICO A VISTA', '12505': 'CARTA NAO COML REGISTRADA', '12513': 'CARTA NAO COML REGISTRO MODICO',
                 '12556': 'CARTA A FATURAR SELO E SE', '12637': 'CARTA NAO COMERCIAL A VISTA', '12645': 'CARTA COMERCIAL A VISTA',
                 '14010': 'MALA DIRETA POSTAL NORMAL LOCA', '14028': 'MALA DIRETA POSTAL URGENTE LOC', '14036': 'MALA DIRETA POSTAL DOMICILIARI',
                 '14575': 'MDP BASICA-NACIONAL- A FATURAR', '14591': 'MDP BASICA-NACIONAL- A VISTA', '14745': 'MDP BASICA- LOCAL 1- A FATURAR',
                 '14753': 'MDP BASICA-ESTADUAL- A FATURAR', '14761': 'MDP BASICA-LOCAL 1- A VISTA', '14770': 'MDP BASICA-ESTADUAL- A VISTA',
                 '14877': 'MDPD NAO END (FATURAR)', '15270': 'MDPE - URGENTE  - LOCAL', '15288': 'MDPE - URGENTE - ESTADUAL',
                 '15296': 'MDPE - URGENTE - NACIONAL', '15300': 'MDPB ESTADUAL A FAT CHANCELA', '15318': 'MDPB LOCAL A FAT CHANCELA',
                 '15326': 'MDPB NACIONAL A FAT CHANCELA', '15350': 'MDB A VISTA CHANCELA NACIONAL', '15547': 'MDB LOCAL PROMO DIA CLIENTE',
                 '15555': 'MDB EST PROMO DIA CLIENTE', '15563': 'MDB NAC PROMO DIA CLIENTE', '15571': 'MDB RCN ATE 20KG LOCAL CHANC',
                 '15580': 'MDB RCN ATE 20KG ESTADO CHANC', '15598': 'MDB RCN ATE 20KG LOCAL FRANQ',
                 '15610': 'MDB RCN ATE 20KG NACIO FRANQ', '15628': 'MDB RCN ATE 20KG NACIO CHANC', '15636': 'MDB RCN ATE 20KG ESTADO FRANQ',
                 '15962': 'COMBO MD DOMICILIARIA PP FAT', '16012': 'CARTÃO POSTAL NACIONAL', '20010': 'IMPRESSONACIONAL NORMAL',
                 '20109': 'IMPRESSO NAC URGENTE FAT CHANC', '20125': 'IMPRESSO NACI NORMAL FAT CHANC', '20141': 'IMPRESSO NAC URGENTE FAT MFD',
                 '20150': 'IMPRESSO NAC NORMAL FAT MFD', '20206': 'IMPRESSO NORMAL _RCN_ATE 20KG', '20214': 'IMPRESSO NACIONAL URGENTE',
                 '20354': 'IMPRESSO RCN ATE 20KG CHANCELA', '20362': 'IMPRESSO REGISTRADO A VISTA', '20370': 'IMPRESSO URGENTE REG A VISTA',
                 '20397': 'IMPRESSO URG REG MOD A VISTA', '20419': 'IMPRESSO REG MODICO A VISTA', '22012': 'CECOGRAMA NACIONAL', '31100': 'SERVIÇOS BASICOS -OPERAÇÃO B -',
                 '31119': 'SERVIÇOS BASICOS-OPERAÇÃO B -', '31127': 'SERVIÇOS BASICOS-OPER B -ANUAL', '31135': 'SERVIÇOS BASICOS-OP B -ANUAL',
                 '31283': 'SERVIÇOS BASICOS -OPERAÇÃO B -', '31291': 'SERVIÇOS BASICOS -OPERAÇÃO B -', '35050': 'DISTRIBUIÇÃO DE REAVISOS-',
                 '35068': 'DISTRIB DE DOCUMENTOS DIVERSOS', '35122': 'DISTRIBUIÇÃO CONVENCIONAL DE', '35130': 'DISTRIBUIÇÃO DE REAVISOS -',
                 '35149': 'DISTRIBUIÇÃO DE DOCUMENTOS', '35173': 'DISTRIB DE CONTAS COM ENTREGA', '35190': 'DISTRIB DE CONTAS COM ENTREGA',
                 '35220': 'DISTRIBUIÇÃO CONTAS ÁGUA/LUZ', '35238': 'DISTRIBUIÇÃO CONTAS ÁGUA/LUZ', '35246': 'DISTRIBUIÇÃO CONTAS ÁGUA/LUZ',
                 '35254': 'DISTRIBUIÇÃO CONTAS ÁGUA/LUZ', '36080': 'REM ECON ORG TRANSITO EST S/AR', '36099': 'REM ECON ORG TRANSITO EST C/AR',
                 '36102': 'REM ECON ORG TRANSITO NAC C/AR', '36110': 'REMES ECON TALÃO CARTÃO', '36129': 'REMES ECON TALÃO CARTÃO',
                 '36137': 'REMES ECON TALÃO CARTÃO', '36145': 'REMES ECON TALÃO CARTÃO', '36200': 'REMESSA ECON.TALAO/CARTAO',
                 '36250': 'REMESSA EXPRESSA BANRISUL', '39012': 'SEDEX CORREIOS LOG', '39217': 'PAC CORREIOS LOG', '40010': 'SEDEX A VISTA SCADA',
                 '40045': 'SEDEX A COBRAR', '40096': 'SEDEX (CONTRATO)', '40126': 'SEDEX A COBRAR-ENCOMENDA', '40150': 'SERVICO DE PROTOCOLO POSTAL -',
                 '40169': 'SEDEX 12 A FATURAR', '40177': 'SEDEX ADMINISTRATIVO CSHOPPING', '40215': 'SEDEX 10 A FATURAR', '40223': 'SEDEX 10-ENCOMENDA',
                 '40290': 'SEDEX HOJE A FATURAR', '40355': 'REM EXP CRVL/CRV/CNH E NOTIFIC', '40380': 'SEDEX REVERSO 40096', '40398': 'SEDEX REVERSO 40436',
                 '40436': 'SEDEX - CONTRATO', '40444': 'SEDEX - CONTRATO', '40517': 'SEDEX REVERSO 40444', '40525': 'REMES EXP ÓRGÃOS DE TRÂNSITO -',
                 '40533': 'REMES EXP ÓRGÃOS DE TRÂNSITO-', '40541': 'REMES EXP ÓRGÃOS DE TRÂNSITO-', '40550': 'SEDEX ADMINISTRATIVO', '40568': 'SEDEX - CONTRATO',
                 '40576': 'SEDEX REVERSO - CONTRATO', '40584': 'SEDEX 10 REVERSO A FATURAR', '40606': 'SEDEX - CONTRATO', '40614': 'SEDEX REVERSO - CONTRATO',
                 '40622': 'REMESSA EXP TALAO DE CHEQUES-', '40630': 'SEDEX PAGAMENTO NA ENTREGA -', '40665': 'REMESSA EXP TALAO DE CHEQUES/',
                 '40673': 'REMESSA EXP TALAO DE CHEQUES/', '40681': 'REMESSA EXP TALAO DE CHEQUES/', '40690': 'REMESSA EXP TALAO DE CHEQUES/',
                 '40703': 'REMESSA EXP TALAO DE CHEQUES/', '40711': 'REMESSA EXP TALAO DE CHEQUES/', '40720': 'REMESSA EXP TALAO DE CHEQUES/',
                 '40738': 'REMESSA EXP TALAO DE CHEQUES/', '40746': 'REMESSA EXP TALAO DE CHEQUES/', '40754': 'REMESSA EXP TALAO DE CHEQUES/',
                 '40762': 'REMESSA EXP TALAO DE CHEQUES/', '40789': 'SEDEX 10', '40797': 'SEDEX 10 REVERSO', '40819': 'SEDEX PAGAMENTO NA ENTREGA -',
                 '40878': 'SEDEX HOJE - ROLO E PACOTE', '40886': 'SEDEX 10 - PACOTE E ROLO', '40894': 'SEDEX 12- PACOTE E  ROLO', '40940': 'COMBO SEDEX 10 A FATURAR',
                 '40959': 'COMBO SEDEX A VISTA SCADA', '40991': 'COMBO SEDEX HOJE A FATURAR', '41068': 'PAC', '41076': 'PAC REVERSO 4106-8', '41106': 'PAC À VISTA SCADA',
                 '41203': 'PAC ADMINISTRATIVO', '41211': 'PAC - CONTRATO', '41220': 'PAC - REVERSO DO 4121-1', '41238': 'PAC - PAGAMENTO NA ENTREGA -',
                 '41254': 'PAC ADMINISTRATIVO CSHOPPING', '41262': 'PAC PAGAMENTO NA ENTREGA -', '41270': 'SEDEX - GRANDES FORMATOS', '41300': 'PAC GRANDES FORMATOS',
                 '41378': 'SEDEX GRANDES FORMATOS', '41408': 'SEDEX REPOSTAGEM', '41432': 'SEDEX PAGAMENTO NA ENTREGA', '41440': 'SEDEX PAGAMENTO NA ENTREGA', '41459': 'COMBO PAC A VISTA SCADA',
                 '41467': 'COMBO SEDEX CONTRATO', '41483': 'COMBO SEDEX 12 A FATURAR', '41491': 'PAC REPOSTAGEM', '41530': 'PAC INTERM E-COMMERCE TAB41068',
                 '41548': 'SEDEX INTERM E-COMMERCE 40096', '41556': 'SEDEX PRE PAGO VIA INTERNET', '41564': 'SEDEX 10 PRE PAGO VIA INTERNET',
                 '41572': 'SEDEX 12 PRE PAGO VIA INTERNET', '41599': 'SEDEX HOJE PRE PAGO VIA INTERN', '41602': 'PAC PRE PAGO VIA INTERNET',
                 '41610': 'REMESSA AGRUPADA PAC', '41629': 'REMESSA AGRUPADA PAC N POLIT',
                 '41637': 'COMBO SEDEX ELEICOES', '41645': 'COMBO SEDEX HOJE ELEICOES', '41653': 'COMBO SEDEX 10 ELEICOES', '41661': 'COMBO PAC ELEICOES',
                 '41670': 'COMBO SEDEX 12 ELEICOES', '41700': 'SEDEX REPOSTAGEM REVERSO', '41726': 'PAC REPOSTAGEM REVERSO', '43010': 'REEMB POSTAL NORMAL (C AVULSO)',
                 '44105': 'MALOTE', '54658': 'TAXA DE ARMAZENAGEM', '68233': 'CARTA VIA INTERNET', '73881': 'ENTREGA EXPRESSA', '74950': 'CARGA CONSOLIDADA EXPRESSA ES',
                 '75043': 'REMESSA SIMPLES LOCAL -', '75078': 'DISTRIBUICAO DE CARNES', '75159': 'DISTRIBUICAO DE CONTAS DE TELE', '75329': 'DISTRIBUICAO DE NOTIFICACOES',
                 '75701': 'IMPRESSAO E DISTRIBUICAO DE EX', '81019': 'E-SEDEX STANDARD', '81027': 'E-SEDEX PRIORITARIO', '81035': 'E-SEDEX EXPRESS', '81043': 'E-SEDEX  REVERSO',
                 '81108': 'E-SEDEX ADMINISTRATIVO CSHOP', '81124': 'E-SEDEX INTERM E-COMMERCE', '81833': 'E-SEDEX GRUPO II', '81841': 'E-SEDEX  REVERSO GRUPO II',
                 '81850': 'E-SEDEX TOCANTINS', '81868': 'E-SEDEX GRUPO I', '81876': 'E-SEDEX  REVERSO GRUPO I', '82015': 'FAC SIMPLES LOCAL', '82023': 'FAC SIMPLES ESTADUAL',
                 '82031': 'FAC SIMPLES NACIONAL', '82040': 'FAC SIMPLES LOC SEM DESC', '82066': 'FAC SIMPLES ESTAD SEM DESC', '82074': 'FAC SIMPLES SEM PRE REQUISITO',
                 '82082': 'FAC REG SEM PRE REQUISITO', '82090': 'FAC REG COM AR SEM PRE REQUISI', '82104': 'FAC REGISTRADO LOCAL', '82112': 'FAC REGISTRADO ESTADUAL',
                 '82120': 'FAC REGISTRADO NACIONAL', '82139': 'FAC REGISTRADO LOCAL COM AR', '82147': 'FAC REGISTRADO ESTADUAL COM AR', '82155': 'FAC REGISTRADO NACIONAL COM AR',
                 '82309': 'FAC SIMPLES LOCAL ACIMA 500 G', '82317': 'FAC SIMPLES ESTAD ACIMA 500 G', '82325': 'FAC SIMPLES NAC ACIMA 500 G',
                 '82333': 'FAC REGIST LOCAL ACIMA 500 G', '82341': 'FAC REGISTRADO EST ACIMA 500 G', '82350': 'FAC REGISTRADO NAC ACIMA 500 G',
                 '82368': 'FAC REG LOCAL C/ AR ACIMA 500G', '82376': 'FAC REG EST C/ AR ACIMA 500 G', '82384': 'FAC REG NAC C/ AR ACIMA 500 G',
                 '82392': 'FAC MONITORADO NACIONAL', '82406': 'FAC MONITORADO ESTADUAL', '82414': 'FAC MONITORADO LOCAL', '82422': 'FAC SIMPLES NACI SEM DESC',
                 '85480': 'VENDA DE AEROGRAMA NACIONAL'}

urlinterna = 'http://scppws.correiosnet.int/calculador/CalcPrecoPrazo.asmx/CalcDataMaxima?codigoObjeto='
urlexterna = 'http://ws.correios.com.br/calculador/calcprecoprazo.asmx/CalcDataMaxima?codigoObjeto='

url = urlinterna
lista_objetos = []
lista_colors = []
empy_object = {'codigo': '', 'descricaoUltimoEvento': '',
               'msgErro': 'Não foi possível objter dados', 'dataMaxEntrega': None, 'servico': None}

class ObjetoRegistrado:

    def __init__(self, codigo_postal, off = False):
        if off:
            dados_postais = codigo_postal
        else:
            dados_postais = self.request_dict_dados_postais(codigo_postal)
        self.codigo = self.validate_codigo(dados_postais['codigo'])
        self.ultimo_evento = dados_postais['descricaoUltimoEvento']
        self.erro = dados_postais['msgErro']
        self.vencimento = self.get_vencimento_from_string(
            dados_postais['dataMaxEntrega'])
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
        print('Código: ', self.codigo)
        print('Status: ', self.status)
        print('Vencimento: ', self.vencimento.strftime("%d/%m/%Y"))

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
            return empy_object

    def layout(self):
        return [self.codigo, self.vencimento_formatado, self.status]

class ObjetoSimples:
    def __init__(self, codigo_postal):
        self.erro = ''
        self.vencimento = self.get_vencimento_from_string(
            codigo_postal)  # data postagem
        self.dia_devolucao = self.add_workdays(self.vencimento, 12)
        self.codigo = 'SIMPLES P: ' + self.vencimento.strftime("%d/%m/%Y")
        self.ultimo_evento = 'Postado dia ' + \
            self.vencimento.strftime("%d/%m/%Y")
        self.dias_apos_postagem = self.dias_uteis_entre_datas(self.vencimento)
        self.vencimento_formatado = 'D + ' + str(self.dias_apos_postagem)
        self.tipo = 'FAQ/CEDO'
        self.color = None
        self.bg_color = None
        self.status = self.get_status(self.dias_apos_postagem)

    def layout(self):
        vencimento = self.dia_devolucao.strftime("%d/%m/%Y")
        return ['FAC/CEDO', vencimento, self.status]

    def get_status(self, dias):
        vencimento = 12
        if(dias < vencimento):
            self.color = 'dark green'
            self.bg_color = 'pale green'
            return 'Entregar até ' + self.dia_devolucao.strftime("%d/%m/%Y")
        elif(dias > vencimento):
            self.color = 'red'
            self.bg_color = 'dark salmon'
            return 'Vencido dia ' + self.dia_devolucao.strftime("%d/%m/%Y")
        else:
            self.color = 'dark blue'
            self.bg_color = 'light blue'
            return 'Entregar Hoje'

    def get_vencimento_from_string(self, string):
        substring = string[-6:]
        try:
            return datetime.strptime(substring, '%d%m%y')
        except:
            return datetime.today()

    def dias_uteis_entre_datas(self, data_inical, data_final=datetime.today()):
        if data_final.date() <= data_inical.date():
            return 0
        dias_uteis = 0
        while data_inical.date() <= data_final.date():
            if data_inical.isoweekday() < 6:
                dias_uteis += 1
            data_inical += timedelta(days=1)
        return dias_uteis

    def add_workdays(self, data_inicial, days_to_add):
        workdays = days_to_add
        current_date = data_inicial
        while workdays > 0:
            current_date += timedelta(days=1)
            weekday = current_date.weekday()
            if weekday >= 5:
                continue
            workdays -= 1
        return current_date

# Layouts
gui.theme('Reddit')

menu_layout = [['Ajuda', ['Instruções::help', 'Sobre::sobre']]]

frame_layout = [
    [gui.Text('', key='-frame_codigo-', font='Helvetica 30 bold', size=(26, 2),
              expand_y=True, expand_x=True, justification='center', pad=0)],
    [gui.Text('', key='-frame_data-', font='Helvetica 24', size=(26, 2),
              expand_y=True, expand_x=True, justification='center', pad=0)],
    [gui.Text('', key='-frame_tipo-', size=(36, 1), justification='left')],
    [gui.Text('', key='-frame_status-', size=(36, 2), justification='left')],
    [gui.Text('', key='-frame_evento-', size=(36, 1), justification='left')]
]

conferir_layout = [
    [gui.Menu(menu_layout)],
    [gui.Input(key='codigo', size=(26, 1), focus=True),
     gui.Button('checar', bind_return_key=True)],
    [gui.Frame('Objeto', frame_layout,
               element_justification='c', key=('-frame-'))],
    [gui.Text('Histórico')],
    [gui.Table([['', '', '']], headings=['   OBJETO   ', 'VENCIMENTO',
               '        SITUAÇÃO        '], key='-table-', justification="left", num_rows=20)]

]
lote_layout = [
    [gui.Multiline(size=(56, 16), key='-input_lote-')],
    [gui.Button('Verificar Lote', key='-verificar-')],
    [gui.Table([['']], headings=['Hoje'], def_col_width=13,auto_size_columns=False, key='-hoje-' ), gui.Table([['']], headings=['Vencidos'],def_col_width=13,auto_size_columns=False, key='-vencidos-' ),
    gui.Table([['']], headings=['No prazo'], def_col_width=13,auto_size_columns=False, key='-noprazo-' )]

]

def on_verifica_click(multiline_text):
    codigos = re.findall(r'[A-Za-z]{2}[0-9]{9}[A-Za-z]{2}', multiline_text)
    hoje = []
    vencidos = []
    noprazo = []
    lista_de_objetos = request_dict_objetos(codigos)
    for objeto in lista_de_objetos:
        objeto_postal = ObjetoRegistrado(objeto, True)
        if objeto_postal.status == 'Entregar Hoje':
            hoje.append([objeto_postal.codigo])
        elif objeto_postal.status == 'Vencido':
            vencidos.append([objeto_postal.codigo])
        elif objeto_postal.status == 'No Prazo':
            noprazo.append([objeto_postal.codigo])

    window['-hoje-'].update(values=hoje)
    window['-vencidos-'].update(values=vencidos)
    window['-noprazo-'].update(values=noprazo)

def request_dict_objetos(lista_de_codigos):
    lista_de_objetos = []
    string_de_codigos = ''
    if len(lista_de_codigos) > 100:
        lista_de_objetos.extend(request_dict_objetos(lista_de_codigos[100:]))
        lista_de_codigos = lista_de_codigos[0:100]

    for codigo in lista_de_codigos:
        string_de_codigos += codigo + ','
    
    try:
        get_xml = requests.get(url + string_de_codigos)
        dict_objeto_postal = xmltodict.parse(get_xml.text)
        lista_de_objetos.extend(dict_objeto_postal['cResultadoObjeto']['Objetos']['cObjeto'])
    except:
        lista_de_objetos = []

    if type(lista_de_objetos) == list:
        return lista_de_objetos
    else:
        return []
        



window = gui.Window('Verifica Prazo', [[gui.TabGroup([[gui.Tab('Conferir Objeto', conferir_layout), gui.Tab(
    'Consulta em lote', lote_layout)]])]], size=(480, 560), icon='src/verificaprazo.ico')


def on_checar_click(codigo_objeto):
    carregando()
    if len(codigo_objeto) <= 13:
        novo_objeto = ObjetoRegistrado(codigo_objeto)
    elif len(codigo_objeto) <= 40:
        novo_objeto = ObjetoSimples(codigo_objeto)
    else:
        novo_objeto = ObjetoRegistrado(codigo_objeto)
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
    # alterar textos
    window['-frame_codigo-'].update(novo_objeto.codigo)
    window['-frame_data-'].update(novo_objeto.vencimento_formatado)
    window['-frame_status-'].update('Situação: ' + novo_objeto.status)
    window['-frame_tipo-'].update('Tipo: ' + novo_objeto.tipo)
    window['-frame_evento-'].update('Evento: ' + novo_objeto.ultimo_evento)
    # alterar cor da fonte
    window['-frame_codigo-'].update(text_color=novo_objeto.color)
    window['-frame_data-'].update(text_color=novo_objeto.color)
    # alterar background
    window['-frame_codigo-'].update(background_color=novo_objeto.bg_color)
    window['-frame_data-'].update(background_color=novo_objeto.bg_color)


def carregar_tipos_postais():
    tipos_url = 'http://ws.correios.com.br/calculador/calcprecoprazo.asmx/ListaServicos?'
    xml = requests.get(tipos_url)
    lista_de_tipos = xmltodict.parse(
        xml.text)['cResultadoServicos']['ServicosCalculo']['cServicosCalculo']
    dicionario_de_tipos = {}
    for tipo in lista_de_tipos:
        dicionario_de_tipos[tipo['codigo']] = tipo['descricao']
    return dicionario_de_tipos

# try:
#    dicionario_de_tipos = carregar_tipos_postais()
# except:
#    dicionario_de_tipos = tipos_postais
#    window.close()


dicionario_de_tipos = tipos_postais

# Loop Window

while True:
    event, values = window.read()
    if event == gui.WINDOW_CLOSED:
        break
    elif event == 'checar':
        on_checar_click(values['codigo'])
    elif event == '-verificar-':
        on_verifica_click(values['-input_lote-'])
    elif event == 'Instruções::help':
        text = """Essa aplicação é auxiliar, ela não substitui nenhum sistema dos correios, é utilizada para verificar o prazo de entrega de objetos postais, todos os dados são retirados da própia API dos correios SCPP, disponível em:
http://ws.correios.com.br/calculador/calcprecoprazo.asmx
        """
        gui.popup(text, icon='src/verificaprazo.ico', title='Instruções')
    elif event == 'Sobre::sobre':
        gui.popup('tecnologia utilizada: python\nerros/dúvidas/sugestões: raildorcv@correios.com.br',
                  icon='src/verificaprazo.ico', title='Sobre')
window.Close()


