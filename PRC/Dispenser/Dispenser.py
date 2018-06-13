class Error(Exception):
    pass

class SemCedulasException(Error):
    def __init__(self, message):
        self.message = message

class ValorNaoSacavelException(Error):
    def __init__(self, message):
        self.message = message


class Cedula:
    def __init__(self, valor, extenso):
        self.__valor = valor
        self.__extenso = extenso

    @property
    def valor(self):
        return self.__valor

    @valor.setter
    def valor(self, novoValor):
        self.__valor = novoValor

    @property
    def extenso(self):
        return self.__extenso

    @extenso.setter
    def extenso(self, novoValor):
        self.__extenso = novoValor

    def __str__(self):
        return self.__extenso

class Numerario:
    def __init__(self, cedula, quantidade):
        self._cedula = cedula
        self._quantidade = quantidade

    @property
    def cedula(self):
        return self._cedula

    @property
    def quantidade(self):
        return self._quantidade

    @cedula.setter
    def cedula(self, novoValor):
        self._cedula = novoValor

    @quantidade.setter
    def quantidade(self, novoValor):
        self._quantidade = novoValor

    def contabilizar(self):
        return self._cedula.valor*self._quantidade

class Gaveta:
    def __init__(self):
        self._conteudo = []

    def adicionarValores(self, numerario):
        self._conteudo.append(numerario)

    def totalizar(self):
        retorno = 0
        for numerario in self._conteudo:
            retorno+=numerario.contabilizar()
        return retorno

    def retirarValores(self, numerario):
        cedula = numerario.cedula
        for nu in self._conteudo:
            if nu.cedula == cedula:
                #print ("Achei a cedula, tem agora ", nu.quantidade)
                if nu.quantidade >= numerario.quantidade:
                    nu.quantidade = nu.quantidade-numerario.quantidade
                else:
                    raise SemCedulasException("Cedulas insuficientes")

    def retirarValor(self, valor):
        valores = []
        saque = []
        for nu in self._conteudo:
            if nu.quantidade > 0:
                valores.append(nu.cedula)
        valores.sort(key=lambda c: c.valor, reverse=True)
        #print (len(valores))
        while valor != 0:
            for v in valores:
                #print (str(v))
                if v.valor > valor:
                    continue
                nume = Numerario(v,0)
                qtd = 0
                while v.valor <= valor:
                    #print (v, " - ", v.valor%valor, " e sobra: ", valor-v.valor)
                    valor -= v.valor
                    qtd += 1
                nume.quantidade = qtd
                saque.append(nume)
            if valor == 1:
                #print (u"Impossível sacar")
                raise ValorNaoSacavelException("Impossivel Sacar")
                break
        if valor == 0:
            for nume in saque:
                print("Cedula: ", nume.cedula, " Quantidade: ", nume.quantidade)
                self.retirarValores(nume)

class Dispenser:
    def __init__(self,  gaveta):
        self._gavetaInicial = gaveta
        self._gaveta = gaveta

    def valoresIniciais(self):
        return self._gavetaInicial.totalizar() 

    def valoresAtuais(self):
        return self._gaveta.totalizar() 

    def retirar(self, valor):
        self._gaveta.retirarValor(valor)

#import ipdb;ipdb.set_trace()
#doisReais = Cedula(2, "Dois Reais")
#cincoReais = Cedula(5, "Cinco Reais")
#dezReais = Cedula(10, "Dez Reais")
#vinteReais = Cedula(20, "Vinte Reais")
#cinquentaReais = Cedula(50, "Cinquenta Reais")
#cemReais = Cedula(100, "Cem Reais")
