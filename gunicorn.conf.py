# gunicorn.conf.py

# Disparado assim que um processo trabalhador (worker) é criado
def post_fork(server, worker):
    server.log.info("Worker inicializado. Conectando cliente MQTT...")
    
    try:
        # Importa a aplicação Flask instalada no worker
        from app import start_mqtt
        # Dispara a conexão MQTT isolada deste worker
        start_mqtt()
    except Exception as e:
        server.log.error(f"Falha ao iniciar MQTT no hook post_fork: {e}")
