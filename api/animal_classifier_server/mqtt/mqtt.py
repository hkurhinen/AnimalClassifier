import random
import paho.mqtt.client as paho
from paho import mqtt

broker = 'localhost'
port = 1883
client_id = f'animal-classifier-server-{random.randint(0, 1000)}'
mqtt_client = None

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = paho.Client(client_id)
    #client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
    #client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def get_mqtt_client():
  global mqtt_client
  if mqtt_client is None or not mqtt_client.is_connected:
    mqtt_client = connect_mqtt()
  return mqtt_client
