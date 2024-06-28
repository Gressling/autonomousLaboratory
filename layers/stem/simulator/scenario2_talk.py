import signal
import time
import paho.mqtt.client as paho
from paho import mqtt

def exit_handler(signal, frame):
    """Handles termination signals."""
    print("Signal received, cleaning up...")
    # Clean-up operations before exit
    client.disconnect()
    print("Exit.")
    exit(0)

signal.signal(signal.SIGINT, exit_handler)
signal.signal(signal.SIGTERM, exit_handler)

# ----------------- MQTT Configuration
client = paho.Client(client_id="dev", userdata=None, protocol=paho.MQTTv5)
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
client.username_pw_set("cheminformatics", input("Password:"))

# ----------------- MQTT Event Handlers
def on_connect(client, userdata, flags, rc, properties):
    """Handles MQTT connection events."""
    if rc == 0:
        print("Connected to the broker successfully.")
        client.subscribe("#", qos=1) # https://www.hivemq.com/blog/mqtt-essentials-part-5-mqtt-topics-best-practices/
    else:
        print(f"Connection failed with code {rc}")

# Attach event handlers to MQTT client
client.on_connect = on_connect

# ----------------- Start MQTT and Publish Initial Message
client.connect("9b15b5bc687c4ecfb410a4fbe8df96b6.s2.eu.hivemq.cloud", 8883)
print("Connected.")

client.publish("STATUS", payload="talk-simulator: Started")
print("talk-simulator: Started ...")
time.sleep(1)

# -- SCENARIO START -------------------------

client.publish("talk", payload="Hello World!")
time.sleep(5)
client.publish("talk", payload="Anyone there?")
time.sleep(8)
client.publish("talk", payload="Please use Aspirin as edukt")
time.sleep(8)

# -- SCENARIO END -------------------------

client.publish("STATUS", payload="talk-simulator: Stopped")
time.sleep(1)
client.disconnect()
print("Exit.")
exit(0)

