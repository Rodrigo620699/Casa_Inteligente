# Casa Inteligente Integrada com ESP32

Este projeto integra uma interface web Flask com um ESP32 para controle de dispositivos IoT via MQTT.

## Componentes

- **Backend**: Flask (Python) com MQTT
- **Frontend**: HTML/CSS/JavaScript
- **Hardware**: ESP32 com DHT22, LEDs, botões
- **Broker MQTT**: Mosquitto local

## Instalação

1. Instalar Mosquitto MQTT broker (já instalado).
2. Instalar dependências Python: `pip install flask paho-mqtt`
3. Configurar WiFi no `esp32_main.py` (SSID, senha).
4. Configurar IP do broker no `esp32_main.py` (IP da máquina).

## Execução

1. Iniciar Mosquitto: `& "C:\Program Files\mosquitto\mosquitto.exe" -c "mosquitto.conf" -v`
2. Executar Flask: `python app.py`
3. Executar simulador ESP32: `python esp32_simulator.py` (simula o ESP32 via MQTT)
4. Acessar http://127.0.0.1:5000
5. Para usar no Wokwi: carregar `esp32_main.py` no Wokwi e usar um broker público como `broker.hivemq.com`.
   - No Wokwi, mantenha `WIFI_SSID = "Wokwi-GUEST"` e `WIFI_PASSWORD = ""`.
   - O broker local `localhost` não é acessível diretamente do Wokwi.
   - Se quiser usar Mosquitto local com Wokwi, crie um túnel (ngrok, localtunnel, etc.) ou publique o broker na internet.

## Funcionalidades

- Controle de luz, porta e ventilador via web.
- Leitura de temperatura DHT22.
- Ventilador liga automaticamente se temp >28°C.
- Status atualizado em tempo real via MQTT.

## Pinos ESP32

- DHT22: 15
- LED Temp: 2
- Botão Luz: 4
- LED Luz Verde: 18
- LED Luz Vermelho: 19
- Botão Porta: 5
- LED Porta Verde: 21
- LED Porta Vermelho: 22
- Ventilador: 23

## Tópicos MQTT

- `casa/luz`: "ligar"/"desligar"
- `casa/porta`: "abrir"/"fechar"
- `casa/ventilador`: "ligar"/"desligar"
- `casa/temperatura`: valor float
- `casa/status`: JSON com status
