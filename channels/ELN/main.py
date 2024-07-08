import time
from mqtt_handler import MQTTHandler
from database_handler import DatabaseHandler
from openai_handler import OpenAIHandler

# Configurations
OPENAI_API_KEY = "sk-proj-6RaDaBsQ7frhcFdMm8MaT3BlbkFJD6dLTboO5p7GuskIVBHn"
MQTT_BROKER_URL = "9b15b5bc687c4ecfb410a4fbe8df96b6.s2.eu.hivemq.cloud"
MQTT_BROKER_PORT = 8883
MQTT_USERNAME = "cheminformatics"
MQTT_PASSWORD = "cogni88."
DB_USER = 'situation'
DB_PASSWORD = "aichem567."
DB_HOST = 'den1.mysql6.gear.host'
DB_NAME = 'situation'

class Application:
    def __init__(self, openai_key, mqtt_config, db_config):
        self.openai_handler = OpenAIHandler(openai_key)
        self.database_handler = DatabaseHandler(
            db_config['user'],
            db_config['password'],
            db_config['host'],
            db_config['database']
        )
        self.mqtt_handler = MQTTHandler(
            broker_url=mqtt_config['url'],
            broker_port=mqtt_config['port'],
            username=mqtt_config['username'],
            password=mqtt_config['password'],
            on_message_callback=self.on_message
        )

    def on_message(self, client, userdata, message):
        question = message.payload.decode('utf-8')
        print(f"Received question: {question}")
        response = self.openai_handler.get_response(question)
        print(f"OpenAI response: {response}")
        sql_query = self.determine_sql_query(response)
        if sql_query:
            result = self.database_handler.execute_query(sql_query)
            self.mqtt_handler.publish("ELN", payload=result)
        else:
            self.mqtt_handler.publish("ELN", payload="Unable to determine SQL query.")

    def determine_sql_query(self, response):
        if "material for Experiment" in response:
            experiment_id = self.extract_experiment_id(response)
            return f"SELECT material_amount FROM experiments WHERE experiment_id = {experiment_id}"
        elif "Molecule in Experiment" in response:
            experiment_id = self.extract_experiment_id(response)
            return f"SELECT molecule_name FROM molecules WHERE experiment_id = {experiment_id}"
        else:
            return None

    def extract_experiment_id(self, response):
        import re
        match = re.search(r'Experiment (\d+)', response)
        if match:
            return int(match.group(1))
        else:
            return None

    def run(self):
        self.mqtt_handler.connect()
        try:
            self.mqtt_handler.client.loop_forever()
        except KeyboardInterrupt:
            print("Disconnecting...")
            self.mqtt_handler.disconnect()
            self.database_handler.close()

# Main function
def main():
    mqtt_config = {
        'url': MQTT_BROKER_URL,
        'port': MQTT_BROKER_PORT,
        'username': MQTT_USERNAME,
        'password': MQTT_PASSWORD
    }
    db_config = {
        'user': DB_USER,
        'password': DB_PASSWORD,
        'host': DB_HOST,
        'database': DB_NAME
    }

    app = Application(OPENAI_API_KEY, mqtt_config, db_config)
    app.run()

if __name__ == "__main__":
    main()