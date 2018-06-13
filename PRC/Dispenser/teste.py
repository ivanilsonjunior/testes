from _socket import gaierror

from Dispenser import *
#import ipdb;ipdb.set_trace()


doisReais = Cedula(2, "Dois Reais")
cincoReais = Cedula(5, "Cinco Reais")
dezReais = Cedula(10, "Dez Reais")
vinteReais = Cedula(20, "Vinte Reais")
cinquentaReais = Cedula(50, "Cinquenta Reais")
cemReais = Cedula(100, "Cem Reais")

gaveta = Gaveta()
gaveta.adicionarValores(Numerario(dezReais, 500))
gaveta.adicionarValores(Numerario(doisReais, 1000))
gaveta.adicionarValores(Numerario(cincoReais, 1000))
gaveta.adicionarValores(Numerario(cemReais, 1000))
#gaveta.adicionarValores(Numerario(vinteReais, 1000))
#print(gaveta.totalizar())
#gaveta.retirarValores(Numerario(dezReais, 100))
#print (gaveta.totalizar())
dis = Dispenser(gaveta)
print (dis.valoresAtuais())
try:
    dis.retirar(120)
except Exception:
    print ("erro ao retirar")

try:
    dis.retirar(515)
except Exception:
    print ("erro ao retirar")

#except Error
print (dis.valoresAtuais())
#print(dezReais)
#@gaveta.setter
#def gaveta(self, novoValor):
#    self.__gaveta = novoValor
   
#import Dispenser
#gaveta1 = dict(doisReais=200, cincoReias=100, dezReais=50, vinteReais=30, cinquentaReais=30, cemReais=20)
#gaveta = { ''.join(dois
#}
#disp = Dispenser(gaveta1)
#print (disp.valores())
#print (dezReais)
