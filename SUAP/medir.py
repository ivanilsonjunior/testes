import json
import requests
import time

urls = { "token":"https://suap.ifrn.edu.br/api/v2/autenticacao/token/",
         "dados":"https://suap.ifrn.edu.br/api/v2/minhas-informacoes/meus-dados/",
         "portal":"http://portal.ifrn.edu.br",
         "suap":"https://suap.ifrn.edu.br"}

autenticacao = {
    "username": "SUA_MATRICULA",
    "password": "SUA_SENHA"
}


tempoToken = 1000.0
tempoInf = 1000.0
tempoPortal = 1000.0
tempoSUAP = 1000.0

def getToken():
    inicio = time.time()
    response = requests.post(urls['token'], data=autenticacao)
    global tempoToken
    tempoToken = (time.time()-inicio)
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))['token']
    return None

cabecalho={'Authorization': 'JWT {0}'.format(getToken())}

def getInformacoes():
    inicio = time.time()
    response = requests.get(urls['dados'], headers=cabecalho)
    global tempoInf
    tempoInf = time.time()-inicio
    if response.status_code == 200:
        return response.content.decode('utf-8')
    return None

def getPortal():
    inicio = time.time()
    response = requests.get(urls['portal'])
    global tempoPortal
    tempoPortal = time.time()-inicio

def getSUAP():
    inicio = time.time()
    response = requests.get(urls['suap'])
    global tempoSUAP
    tempoSUAP = time.time()-inicio


getPortal()
getSUAP()
getInformacoes()
#informacoes = json.loads(getInformacoes())


#print ("Portal: {0} - SUAP: {1} - Token: {2} - Informacoes: {3}".format(tempoSUAP, tempoPortal, tempoToken, tempoInf))

thingSpeak = "https://api.thingspeak.com/update?api_key=69EN4QDFFY25I18K&field1={1}&field2={0}&field3={3}&field4={2}".format(tempoSUAP, tempoPortal, tempoToken, tempoInf)

requests.get(thingSpeak)

# Para ver o conteudo de informacoes, descomente a linha abaixo
# VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV
#print (informacoes)
#print ("Matricula: {0}\n\tNome: {1}\n\tE-Mail: {2}".format(informacoes['matricula'], informacoes['nome_usual'], informacoes['email']))
