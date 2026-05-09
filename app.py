from flask import Flask, render_template, redirect, jsonify
from dispositivos import Luz, Ventilador, Porta, SensorTemperatura
import threading
import time

app = Flask(__name__)

# Criando dispositivos

luz = Luz("Luz da Sala")
ventilador = Ventilador("Ventilador")
porta = Porta("Porta")
sensor = SensorTemperatura()

def automacao_ventilador():
    while True:
        temp = sensor.ler()
        if temp > 28:
            ventilador.ligar()
        else:
            ventilador.desligar()
        time.sleep(10)  # Verificar a cada 10 segundos

# Iniciar thread para automação
thread = threading.Thread(target=automacao_ventilador, daemon=True)
thread.start()

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
        porta.abrir()

    return redirect("/")

@app.route("/desligar/<dispositivo>")
def desligar(dispositivo):
    if dispositivo == "luz":
        luz.desligar()
    elif dispositivo == "ventilador":
        ventilador.desligar()
    elif dispositivo == "porta":
        porta.fechar()

    return redirect("/")

@app.route("/api/status")
def api_status():
    return jsonify({
        "luz": luz.status(),
        "ventilador": ventilador.status(),
        "porta": porta.status(),
        "temperatura": sensor.ler()
    })

if __name__ == "__main__":
    app.run(debug=True)


