import RPi.GPIO as GPIO
import time
import threading

from sonar import Sonar

class Robo(object):
    pwmDirPin = 3
    frenteDir = 17
    trasDir = 27

    pwmEsqPin = 14
    frenteEsq = 15
    trasEsq = 18

    def __init__(self):
	self.ler_sensores()

	pwmDir = GPIO.PWM(self.pwmDirPin, 100)
	pwmDir.start(30);
	pwmEsq = GPIO.PWM(self.pwmEsqPin, 100)
	pwmEsq.start(30);

	self.frente()

	'''
	time.sleep(0.5)
	GPIO.output(self.frenteDir,0)
	GPIO.output(self.frenteEsq,1)
	GPIO.output(self.frenteEsq, 0)
	GPIO.output(self.trasEsq, 1)

	s = Sonar()
	while True:
	    distancia = s.medir()
	    print distancia
	    if distancia < 10:
	        GPIO.output(self.frenteEsq,0)
	        GPIO.output(self.trasEsq, 0)
	        GPIO.output(self.frenteDir,0)
		GPIO.output(self.trasDir, 0)
	    else:
       		GPIO.output(self.trasDir, 0)
        	GPIO.output(self.frenteDir,1)
        	GPIO.output(self.trasEsq, 0)
        	GPIO.output(self.frenteEsq,1)'''

    def ler_sensores(self):
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(self.frenteDir, GPIO.OUT)
	GPIO.setup(self.trasDir, GPIO.OUT)
	GPIO.setup(self.pwmDirPin, GPIO.OUT)

	GPIO.setup(self.frenteEsq, GPIO.OUT)
	GPIO.setup(self.trasEsq, GPIO.OUT)
	GPIO.setup(self.pwmEsqPin, GPIO.OUT)

    def frente(self):
	time.sleep(0.5)
	GPIO.output(self.frenteEsq, 0)
	GPIO.output(self.trasEsq, 1)
	GPIO.output(self.frenteDir, 1)
	GPIO.output(self.trasDir, 0)

    # Funciona
    def tras(self):
	time.sleep(0.5)
	GPIO.output(self.frenteEsq, 0)
	GPIO.output(self.trasEsq, 1)
	GPIO.output(self.frenteDir, 0)
	GPIO.output(self.trasDir, 1)

    # Funciona
    def esquerda(self):
	time.sleep(0.5)
	GPIO.output(self.trasDir, 0)
	GPIO.output(self.frenteDir, 1)
	GPIO.output(self.trasEsq, 0)
	GPIO.output(self.frenteEsq, 1)

    def direita(self):
	time.sleep(0.5)
	GPIO.output(self.trasDir, 0)
	GPIO.output(self.frenteDir, 1)
	GPIO.output(self.trasEsq, 0)
	GPIO.output(self.frenteEsq, 1)

    # Funciona
    def parar(self):
	time.sleep(0.5)
	GPIO.output(self.trasDir, 1)
	GPIO.output(self.frenteDir, 1)
	GPIO.output(self.trasEsq, 1)
	GPIO.output(self.frenteEsq, 1)

if __name__ == "__main__":
	r = Robo()
