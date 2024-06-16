# ----------------- Imports
# env_manager/utils.py
import os
from utilities.env_manager import utils

import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
print(os.getenv('AICHEM_MQTT_LOGIN'))
print(os.getenv('AICHEM_DB_LOGIN'))


utils.load_and_print_env_variables()

import signal
import time
import mysql.connector
import paho.mqtt.client as paho
from paho import mqtt

# ----------------- Signal Handling
def exit_handler(signal, frame):
    """Handles termination signals."""
    print("Signal received, cleaning up...")
    # Clean-up operations before exit
    cursor.close()
    cnx.disconnect()
    client.disconnect()
    print("Exit.")
    exit(0)

# Attach handlers to termination signals
signal.signal(signal.SIGINT, exit_handler)
signal.signal(signal.SIGTERM, exit_handler)

# ----------------- Database Configuration
dbpw=os.getenv('AICHEM_DB_LOGIN')
print(dbpw)

cnx = mysql.connector.connect(
    user='situation', 
    password=dbpw,
    host='den1.mysql6.gear.host',
    database='situation'
)
cursor = cnx.cursor()

query = (
    "INSERT INTO `situation`.`situation2` (`channel`, `prompt`) "
    "VALUES (%s, %s);"
)

# ----------------- MQTT Configuration
client = paho.Client(client_id="dev", userdata=None, protocol=paho.MQTTv5)
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
mqttpw=os.getenv('AICHEM_MQTT_LOGIN')
print(mqttpw)
client.username_pw_set("cheminformatics", mqttpw)

# ----------------- MQTT Event Handlers
def on_message(client, userdata, message):
    """Handles incoming MQTT messages."""
    channel = message.topic
    mymessage = message.payload.decode('utf-8')
    print(f"Received message {channel}: {mymessage}")
    
    values = (channel, mymessage)
    cursor.execute(query, values)
    cnx.commit()

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

# ----------------- Database Configuration
dbpw=os.getenv('AICHEM_DB_LOGIN')
print(dbpw)

cnx = mysql.connector.connect(
    user='situation', 
    password=dbpw,
    host='den1.mysql6.gear.host',
    database='situation'
)
cursor = cnx.cursor()

query = (
    "INSERT INTO `situation`.`situation2` (`channel`, `prompt`) "
    "VALUES (%s, %s);"
)

# ----------------- Start MQTT and Publish Initial Message
client.connect("9b15b5bc687c4ecfb410a4fbe8df96b6.s2.eu.hivemq.cloud", 8883)
print("Connected.")

client.publish("STATUS", payload="STEM: Started")
print("STEM: Started ...")

# ----------------- Run MQTT Event Loop
client.loop_forever()
