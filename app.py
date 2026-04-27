from flask import Flask, render_template, redirect
from dispositivos import Luz, Ventilador, Porta, SensorTemperatura

app = Flask(__name__)

# Criando dispositivos

luz = Luz("Luz da Sala")
ventilador = Ventilador("Ventilador")
porta = Porta("Porta")
sensor = SensorTemperatura()

@app.route("/")
def index():
    return render_template("index.html",
        luz=luz,
        ventilador=ventilador,
        porta=porta,
        temperatura=sensor.ler()
    )

@app.route("/ligar/<dispositivo>")
def ligar(dispositivo):
    if dispositivo == "luz":
        luz.ligar()
    elif dispositivo == "ventilador":
        ventilador.ligar()
    elif dispositivo == "porta":
        porta.ligar()

    return redirect("/")

@app.route("/desligar/<dispositivo>")
def desligar(dispositivo):
    if dispositivo == "luz":
        luz.desligar()
    elif dispositivo == "ventilador":
        ventilador.desligar()
    elif dispositivo == "porta":
        porta.desligar()

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
