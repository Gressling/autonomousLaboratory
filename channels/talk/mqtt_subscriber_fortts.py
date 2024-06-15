import signal
import time
import paho.mqtt.client as paho
from paho import mqtt
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

# TTS Setup
def text_to_speech(text, output_file):
    tts = gTTS(text=text, lang='en')
    tts.save(output_file)
    print(f"Audio file saved as '{output_file}'.")

def play_audio(file_path):
    audio = AudioSegment.from_file(file_path)
    play(audio)

def exit_handler(signal, frame):
    """Handles termination signals."""
    print("Signal received, cleaning up...")
    client.disconnect()
    print("Exit.")
    exit(0)

signal.signal(signal.SIGINT, exit_handler)
signal.signal(signal.SIGTERM, exit_handler)

# ----------------- MQTT Configuration
client = paho.Client(client_id="subscriber_dev", userdata=None, protocol=paho.MQTTv5)
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
client.username_pw_set("cheminformatics", input("Password:"))

# ----------------- MQTT Event Handlers
def on_connect(client, userdata, flags, rc, properties):
    """Handles MQTT connection events."""
    if rc == 0:
        print("Connected to the broker successfully.")
        client.subscribe("#", qos=1)
    else:
        print(f"Connection failed with code {rc}")

def on_message(client, userdata, msg):
    """Handles incoming messages."""
    try:
        print(f"Received message on topic {msg.topic}: {msg.payload.decode()}")
        text = msg.payload.decode()
        output_file = "output.mp3"
        text_to_speech(text, output_file)
        play_audio(output_file)
    except Exception as e:
        print(f"Error processing message: {e}")

# Attach event handlers to MQTT client
client.on_connect = on_connect
client.on_message = on_message

# ----------------- Start MQTT Client
client.connect("9b15b5bc687c4ecfb410a4fbe8df96b6.s2.eu.hivemq.cloud", 8883)
client.loop_start()

# Keep the script running
while True:
    time.sleep(1)
