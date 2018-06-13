import json
import requests
import time

urls = { "token":"https://suap.ifrn.edu.br/api/v2/autenticacao/token/",
         "dados":"https://suap.ifrn.edu.br/api/v2/minhas-informacoes/meus-dados/"}

autenticacao = {
    "username": "SEU_USUARIO",
    "password": "SUA_SENHA"
}


def getToken():
    response = requests.post(urls['token'], data=autenticacao)
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))['token']
    return None

cabecalho={'Authorization': 'JWT {0}'.format(getToken())}

def getInformacoes():
    response = requests.get(urls['dados'], headers=cabecalho)
    if response.status_code == 200:
        return response.content.decode('utf-8')
    return None

inicio = time.time()
informacoes = json.loads(getInformacoes())
final = time.time()-inicio
# Para ver o conteudo de informacoes, descomente a linha abaixo
# VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV
#print (informacoes)
print ("Matricula: {0}\n\tNome: {1}\n\tE-Mail: {2}\n\tTempo: {3:.2f} s".format(informacoes['matricula'], informacoes['nome_usual'], informacoes['email'], final))
