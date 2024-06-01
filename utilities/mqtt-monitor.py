# ----------------- Imports
import signal
import time
import paho.mqtt.client as paho
from paho import mqtt

# ----------------- Signal Handling
def exit_handler(signal, frame):
    """Handles termination signals."""
    print("Signal received, cleaning up...")
    # Clean-up operations before exit
    client.disconnect()
    print("Exit.")
    exit(0)

# Attach handlers to termination signals
signal.signal(signal.SIGINT, exit_handler)
signal.signal(signal.SIGTERM, exit_handler)

# ----------------- MQTT Configuration
client = paho.Client(client_id="dev", userdata=None, protocol=paho.MQTTv5)
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
client.username_pw_set("cheminformatics", input("Enter MQTT password: "))

# ----------------- MQTT Event Handlers
def on_message(client, userdata, message):
    """Handles incoming MQTT messages."""
    channel = message.topic
    mymessage = message.payload.decode('utf-8')
    print(f"{channel}: {mymessage}")

def on_connect(client, userdata, flags, rc, properties):
    """Handles MQTT connection events."""
    if rc == 0:
        print("Connected to the broker successfully.")
        client.subscribe("#", qos=1) # https://www.hivemq.com/blog/mqtt-essentials-part-5-mqtt-topics-best-practices/
    else:
        print(f"Connection failed with code {rc}")

# Attach event handlers to MQTT client
client.on_connect = on_connect
client.on_message = on_message

# ----------------- Start MQTT and Publish Initial Message
client.connect("9b15b5bc687c4ecfb410a4fbe8df96b6.s2.eu.hivemq.cloud", 8883)
print("Connected!")


# ----------------- Run MQTT Event Loop
client.loop_forever()
