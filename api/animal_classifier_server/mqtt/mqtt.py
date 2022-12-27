import random
import paho.mqtt.client as paho
from paho import mqtt

broker = 'localhost'
port = 1883
client_id = f'animal-classifier-server-{random.randint(0, 1000)}'
client = None

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = paho.Client(client_id)
    client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
    #client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    client.is_connected

def get_mqtt_client():
  if client is None or not client.is_connected:
    connect_mqtt()
  return client
