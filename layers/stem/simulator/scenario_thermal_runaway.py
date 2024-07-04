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
client = paho.Client(client_id="lab_autonomy", userdata=None, protocol=paho.MQTTv5)
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
client.username_pw_set("cheminformatics", input("Password:"))

# ----------------- MQTT Event Handlers
def on_connect(client, userdata, flags, rc, properties):
    """Handles MQTT connection events."""
    if rc == 0:
        print("Connected to the broker successfully.")
        client.subscribe("#", qos=1)  # Subscribe to all topics
    else:
        print(f"Connection failed with code {rc}")

client.on_connect = on_connect

# ----------------- Start MQTT and Publish Initial Message
client.connect("9b15b5bc687c4ecfb410a4fbe8df96b6.s2.eu.hivemq.cloud", 8883)
print("Connected.")

client.publish("STATUS", payload="lab-simulator: Started")
print("lab-simulator: Started ...")
time.sleep(1)

# -- SCENARIO START -------------------------

# Basic greetings
client.publish("talk", payload="SPEAK Hello, this is the autonomous lab system.")
time.sleep(2)
client.publish("talk", payload="SPEAK Preparing for today's experiments.")
time.sleep(2)

# Initial setup checks
client.publish("Microphone/STT", payload="PREPARE INITIAL SETUP")
client.publish("Speaker/TTS", payload="RETURN INITIAL SETUP CHECKLIST")
client.publish("Camera/CV", payload="VERIFY INITIAL SETUP")
time.sleep(3)

# Verifying equipment status
client.publish("Camera/CV", payload="VERIFY ALL EQUIPMENT")
client.publish("Speaker/TTS", payload="EQUIPMENT VERIFICATION IN PROGRESS")
time.sleep(5)

# Starting experiment that might lead to thermal runaway
client.publish("talk", payload="SPEAK Starting experiment involving exothermic reaction.")
client.publish("Sensor/Temperature", payload="MONITOR REACTION TEMPERATURE")
time.sleep(2)

# Simulating thermal runaway detection
client.publish("Sensor/Temperature", payload="TEMPERATURE RISE DETECTED")
time.sleep(2)
client.publish("Speaker/TTS", payload="WARNING: Rapid temperature rise detected. Initiating thermal runaway protocol.")
client.publish("Alarm", payload="ACTIVATE EMERGENCY ALARM")
client.publish("Ventilation", payload="INCREASE VENTILATION")
time.sleep(2)

# System responding to thermal runaway
client.publish("CoolingSystem", payload="ACTIVATE COOLING SYSTEM")
client.publish("Speaker/TTS", payload="Cooling system activated. Please evacuate the lab immediately.")
time.sleep(5)

# Confirming temperature stabilization
client.publish("Sensor/Temperature", payload="VERIFY TEMPERATURE STABILIZATION")
client.publish("Speaker/TTS", payload="Temperature is stabilizing. Monitoring closely.")
time.sleep(5)

# Resuming normal operations after stabilization
client.publish("Sensor/Temperature", payload="TEMPERATURE STABILIZED")
client.publish("Speaker/TTS", payload="Temperature stabilized. It is now safe to re-enter the lab.")
time.sleep(3)

# Resuming normal operations
client.publish("talk", payload="SPEAK Resuming normal laboratory operations.")
client.publish("Microphone/STT", payload="CONTINUE WITH EXPERIMENT")
client.publish("Speaker/TTS", payload="Proceeding with the next steps of the experiment.")
time.sleep(2)

# Data collection and analysis
client.publish("Sensor/Data", payload="COLLECT TEMPERATURE DATA")
client.publish("Sensor/Data", payload="COLLECT PRESSURE DATA")
client.publish("Sensor/Data", payload="COLLECT HUMIDITY DATA")
time.sleep(3)

client.publish("Analyzer", payload="ANALYZE DATA")
client.publish("Speaker/TTS", payload="Data analysis in progress.")
time.sleep(3)

# Decision based on data analysis
client.publish("Analyzer", payload="RESULT ANALYSIS COMPLETE")
client.publish("Speaker/TTS", payload="Analysis complete. Experiment can proceed safely.")
time.sleep(2)

# Experiment completion
client.publish("talk", payload="SPEAK Experiment completed successfully.")
time.sleep(2)

# -- SCENARIO END -------------------------

client.publish("STATUS", payload="lab-simulator: Stopped")
time.sleep(1)
client.disconnect()
print("Exit.")
exit(0)
