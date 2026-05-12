from machine import Pin
from dht import DHT22
from time import sleep
import network
from umqtt.simple import MQTTClient
import gc
import json

# ==========================================
# WIFI
# ==========================================

WIFI_SSID = "Wokwi-GUEST"
WIFI_PASSWORD = ""

# ==========================================
# MQTT
# ==========================================

MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_CLIENT_ID = "esp32_casa"

TOPIC_TEMPERATURA = b"casa/temperatura"
TOPIC_STATUS = b"casa/status"

# ==========================================
# SENSOR TEMPERATURA
# ==========================================

sensor = DHT22(Pin(15))

# LED indicador temperatura alta
led_temp = Pin(2, Pin.OUT)

# ==========================================
# LÂMPADA
# ==========================================

led_verde_lamp = Pin(18, Pin.OUT)
led_vermelho_lamp = Pin(19, Pin.OUT)

lampada_ligada = False

# ==========================================
# PORTA
# ==========================================

led_verde_porta = Pin(21, Pin.OUT)
led_vermelho_porta = Pin(22, Pin.OUT)

porta_aberta = False

# ==========================================
# VENTILADOR
# ==========================================

ventilador = Pin(23, Pin.OUT)

# LEDS ventilador
led_verde_vent = Pin(25, Pin.OUT)
led_vermelho_vent = Pin(26, Pin.OUT)

# Estado inicial
ventilador.off()

led_verde_vent.off()
led_vermelho_vent.on()

# ==========================================
# WIFI
# ==========================================

def conectar_wifi():

    wlan = network.WLAN(network.STA_IF)

    wlan.active(True)

    wlan.connect(WIFI_SSID, WIFI_PASSWORD)

    print("📶 Conectando WiFi...")

    while not wlan.isconnected():

        sleep(1)

    print("✅ WiFi conectado")
    print(wlan.ifconfig())

# ==========================================
# MQTT
# ==========================================

def conectar_mqtt():

    client = MQTTClient(
        MQTT_CLIENT_ID,
        MQTT_BROKER,
        MQTT_PORT
    )

    client.connect()

    print("✅ MQTT conectado")

    return client

# ==========================================
# CONEXÕES
# ==========================================

conectar_wifi()

client = conectar_mqtt()

# ==========================================
# LOOP PRINCIPAL
# ==========================================

while True:

    # ======================================
    # LEITURA TEMPERATURA
    # ======================================

    sensor.measure()

    temperatura = sensor.temperature()

    print("🌡 Temperatura:", temperatura)

    # ======================================
    # CONTROLE VENTILADOR AUTOMÁTICO
    # ======================================

    if temperatura > 28:

        # Liga ventilador
        ventilador.on()

        # LED verde ON
        led_verde_vent.on()

        # LED vermelho OFF
        led_vermelho_vent.off()

        # LED temperatura ON
        led_temp.on()

        print("🌀 Ventilador LIGADO")

    else:

        # Desliga ventilador
        ventilador.off()

        # LED verde OFF
        led_verde_vent.off()

        # LED vermelho ON
        led_vermelho_vent.on()

        # LED temperatura OFF
        led_temp.off()

        print("❄ Ventilador DESLIGADO")

    # ======================================
    # LÂMPADA FIXA
    # ======================================

    led_verde_lamp.off()
    led_vermelho_lamp.on()

    # ======================================
    # PORTA FIXA
    # ======================================

    led_verde_porta.off()
    led_vermelho_porta.on()

    # ======================================
    # STATUS MQTT
    # ======================================

    status = {

        "temperatura": temperatura,

        "ventilador": "ligado" if temperatura > 28 else "desligado"
    }

    payload = json.dumps(status)

    client.publish(TOPIC_STATUS, payload)

    client.publish(
        TOPIC_TEMPERATURA,
        str(temperatura)
    )

    gc.collect()

    sleep(1)