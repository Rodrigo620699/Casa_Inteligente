import random


class Dispositivo:
    def __init__(self, nome):
        self.nome = nome
        self.estado = False

    def ligar(self):
        self.estado = True

    def desligar(self):
        self.estado = False

    def status(self):
        return "Ligado" if self.estado else "Desligado"
    

class Luz(Dispositivo):
    pass

class Ventilador(Dispositivo):
    pass

class Porta(Dispositivo):
    def ligar(self):
        self.estado = True  # Aberta

    def desligar(self):
        self.estado = False  # Fechada

    def abrir(self):
        self.ligar()

    def fechar(self):
        self.desligar()

    def status(self):
        return "Aberta" if self.estado else "Fechada"
    
# Sensor de temperatura:

class SensorTemperatura:
    def ler(self):
        return random.randint(20, 35)
    
