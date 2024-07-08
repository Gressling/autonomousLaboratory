import paho.mqtt.client as paho
from paho import mqtt

class MQTTHandler:
    def __init__(self, broker_url, broker_port, username, password, on_message_callback):
        self.client = paho.Client(client_id="dev_client", userdata=None, protocol=paho.MQTTv5)
        self.client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
        self.client.username_pw_set(username, password)
        self.client.on_connect = self.on_connect
        self.client.on_message = on_message_callback
        self.broker_url = broker_url
        self.broker_port = broker_port

    def on_connect(self, client, userdata, flags, rc, properties):
        if rc == 0:
            print("Connected to the broker successfully.")
            client.subscribe("ELN", qos=1)  # Subscribe to the topic
        else:
            print(f"Connection failed with code {rc}")

    def connect(self):
        self.client.connect(self.broker_url, self.broker_port)
        self.client.loop_start()

    def publish(self, topic, payload):
        self.client.publish(topic, payload=payload)

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()
