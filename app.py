from flask import Flask, render_template, redirect, jsonify
import paho.mqtt.client as mqtt
import json

app = Flask(__name__)

# ==========================================
# CONFIGURAÇÕES MQTT
# ==========================================

MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_CLIENT_ID = "flask_casa"

# ==========================================
# STATUS GLOBAL
# ==========================================

status_atual = {
    "luz": "desligado",
    "porta": "fechada",
    "ventilador": "desligado",
    "temperatura": 25
}

# ==========================================
# MQTT CALLBACKS
# ==========================================

def on_connect(client, userdata, flags, rc):

    if rc == 0:
        print("✅ Conectado ao Broker MQTT")

        # Inscrever nos tópicos
        client.subscribe("casa/status")
        client.subscribe("casa/temperatura")

        print("📡 Inscrito nos tópicos MQTT")

    else:
        print("❌ Falha ao conectar MQTT:", rc)


def on_message(client, userdata, msg):

    global status_atual

    try:
        payload = msg.payload.decode().strip()

        print(f"📥 Mensagem recebida -> {msg.topic}: {payload}")

        # ==========================
        # STATUS GERAL
        # ==========================

        if msg.topic == "casa/status":

            if payload:

                dados = json.loads(payload)

                status_atual["luz"] = dados.get("luz", "desligado")
                status_atual["porta"] = dados.get("porta", "fechada")
                status_atual["ventilador"] = dados.get("ventilador", "desligado")
                status_atual["temperatura"] = dados.get("temperatura", 25)

                print("✅ Status atualizado")

        # ==========================
        # TEMPERATURA
        # ==========================

        elif msg.topic == "casa/temperatura":

            if payload:

                status_atual["temperatura"] = float(payload)

                print("🌡 Temperatura atualizada")

    except Exception as erro:

        print("❌ Erro ao processar MQTT:", erro)


# ==========================================
# INICIAR MQTT
# ==========================================

def start_mqtt():

    global mqtt_client

    mqtt_client = mqtt.Client(client_id=MQTT_CLIENT_ID)

    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    # Reconexão automática
    mqtt_client.reconnect_delay_set(min_delay=1, max_delay=120)

    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)

    mqtt_client.loop_start()

    print("🚀 MQTT iniciado")


# ==========================================
# ROTAS FLASK
# ==========================================

@app.route("/")
def index():

    return render_template(
        "index.html",
        status=status_atual
    )


# ==========================================
# LIGAR
# ==========================================

@app.route("/ligar/<dispositivo>")
def ligar(dispositivo):

    try:

        if dispositivo == "luz":

            mqtt_client.publish("casa/luz", "ligar")

            print("📤 MQTT enviado -> casa/luz : ligar")

        elif dispositivo == "ventilador":

            mqtt_client.publish("casa/ventilador", "ligar")

            print("📤 MQTT enviado -> casa/ventilador : ligar")

        elif dispositivo == "porta":

            mqtt_client.publish("casa/porta", "abrir")

            print("📤 MQTT enviado -> casa/porta : abrir")

    except Exception as erro:

        print("❌ Erro ao publicar MQTT:", erro)

    return redirect("/", code=302)


# ==========================================
# DESLIGAR
# ==========================================

@app.route("/desligar/<dispositivo>")
def desligar(dispositivo):

    try:

        if dispositivo == "luz":

            mqtt_client.publish("casa/luz", "desligar")

            print("📤 MQTT enviado -> casa/luz : desligar")

        elif dispositivo == "ventilador":

            mqtt_client.publish("casa/ventilador", "desligar")

            print("📤 MQTT enviado -> casa/ventilador : desligar")

        elif dispositivo == "porta":

            mqtt_client.publish("casa/porta", "fechar")

            print("📤 MQTT enviado -> casa/porta : fechar")

    except Exception as erro:

        print("❌ Erro ao publicar MQTT:", erro)

    return redirect("/", code=302)


# ==========================================
# API STATUS
# ==========================================

@app.route("/api/status")
def api_status():

    return jsonify(status_atual)


# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":

    print("===================================")
    print("🏠 SISTEMA CASA INTELIGENTE")
    print("===================================")

    start_mqtt()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
        use_reloader=False
    )