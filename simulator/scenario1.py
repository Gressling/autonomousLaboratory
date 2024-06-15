import signal
import time
import paho.mqtt.client as paho
from paho import mqtt
from utilities.env_manager import utils

utils.load_and_print_env_variables()

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
client.publish("talk", payload="SPEAK Hello World!")
time.sleep(5)
client.publish("talk", payload="SPEAK Anyone there?")
time.sleep(5)
client.publish("talk", payload="SPEAK OK, some scale work.")
client.publish("scale", payload="SCALE 244")
time.sleep(1)

# transferred with chatGPT

# Researcher speaks into the microphone to prepare the titration setup.
client.publish("Microphone/STT", payload="PREPARE TITRATION SETUP")

# The smart lab system returns a checklist of required items and setup steps for the titration.
client.publish("Speaker/TTS", payload="RETURN TITRATION SETUP CHECKLIST")

# Camera captures frames of the lab to detect the presence and correct setup of required items.
client.publish("Camera/CV", payload="DETECT SETUP")

# Camera confirms the presence of the titrant and indicator solution.
client.publish("Camera/CV", payload="VERIFY TITRANT INDICATOR")

# Additional verification steps by the camera.
client.publish("Camera/CV", payload="VERIFY ...")

# The smart lab system confirms experiment can begin.
client.publish("Speaker/TTS", payload="RETURN CONFIRMATION")

# Buffered readings from the scale, pH meter, and thermometer are analyzed.
client.publish("Scale/PH_Meter/Thermometer", payload="ANALYZE [PH METER] READINGS")

# Thalamus detects the pH level approaching the endpoint and determines necessary actions.
client.publish("Thalamus", payload="DECELERATE TITRANT ADDITION")

# The speaker outputs the command to slow down the addition of titrant.
client.publish("Speaker/TTS", payload="RETURN MESSAGE")


# -- SCENARIO END -------------------------

client.publish("STATUS", payload="talk-simulator: Stopped")
time.sleep(1)
client.disconnect()
print("Exit.")
exit(0)

