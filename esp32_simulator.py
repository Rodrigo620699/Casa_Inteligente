import paho.mqtt.client as mqtt
import time
import random
import json

# Para testar localmente com o mesmo broker do Wokwi/Flask, use um broker público.
# Se quiser usar Mosquitto local apenas no PC, mantenha localhost, mas o Wokwi não conseguirá se conectar nele.
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_CLIENT_ID = "esp32_sim"

def on_connect(client, userdata, flags, rc):
    print("Simulador conectado ao MQTT")
    client.subscribe("casa/luz")
    client.subscribe("casa/porta")
    client.subscribe("casa/ventilador")

def on_message(client, userdata, msg):

    global status_atual

    try:

        topic = msg.topic

        payload = msg.payload.decode().strip()

        print(f"📥 {topic} -> {payload}")

        # Ignorar payload vazio
        if not payload:

            print("⚠ Payload vazio ignorado")

            return

        # =====================================
        # TEMPERATURA
        # =====================================

        if topic == "casa/temperatura":

            try:

                status_atual["temperatura"] = float(payload)

                print("🌡 Temperatura atualizada")

            except Exception as erro:

                print("Erro temperatura:", erro)

        # =====================================
        # STATUS
        # =====================================

        elif topic == "casa/status":

            try:

                dados = json.loads(payload)

                status_atual["luz"] = dados.get(
                    "luz",
                    "desligada"
                )

                status_atual["porta"] = dados.get(
                    "porta",
                    "fechada"
                )

                status_atual["ventilador"] = dados.get(
                    "ventilador",
                    "desligado"
                )

                status_atual["temperatura"] = dados.get(
                    "temperatura",
                    0
                )

                print("✅ Status atualizado")

            except Exception as erro:

                print("❌ JSON inválido:", erro)

    except Exception as erro:

        print("❌ Erro MQTT:", erro)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, MQTT_CLIENT_ID)
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

status = {
    "luz": "desligada",
    "porta": "fechada",
    "ventilador": "desligado",
    "temperatura": 25
}

while True:
    # Verificar mensagens MQTT
    client.check_msg()

    # Simular temperatura
    status["temperatura"] = round(random.uniform(20, 35), 1)

    # Controle automático ventilador (apenas se não foi controlado manualmente recentemente)
    # Para simplificar, manter automático, mas comandos manuais prevalecem
    # Aqui, só atualizar se não foi mudado por comando
    # Mas para demo, vamos manter o automático

    # Publicar
    client.publish("casa/temperatura", str(status["temperatura"]))
    client.publish("casa/status", json.dumps(status))

    print("Publicado:", status)
    time.sleep(2)