#include <ArduinoJson.h>
#include <ArduinoJson.hpp>  // must be version 5.13.x!
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

int ldrPin = A0;

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels
#define OLED_RESET     -1 // Reset pin # (or -1 if sharing Arduino reset pin)

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

int lineHeight = 8; // Assuming text size of 1, each line height is 8 pixels
int currentLine = 0;


void mySerial(String message) {
  unsigned long currentTime = millis();
  display.clearDisplay();
  currentLine = 0;
  
  display.setCursor(0, currentLine * lineHeight*2);
  display.printf("%lu: %s", currentTime, message.c_str());
  display.display();
  delay(500);

  // Prepare for the next line
  currentLine++;
  if (currentLine * lineHeight >= SCREEN_HEIGHT) {
    // If reached bottom, scroll back to top
    display.clearDisplay();
    currentLine = 0;
  }
}

#include <DHTesp.h>
#ifdef ESP8266
 #include <ESP8266WiFi.h>
 #else
 #include <WiFi.h>
#endif

/* #include <ArduinoJson.h> */
#include <PubSubClient.h>
#include <WiFiClientSecure.h>

/****** WiFi Connection Details *******/
const char* ssid = "";
const char* password = "";

/******* MQTT Broker Connection Details *******/
const char* mqtt_server = "xx.s2.eu.hivemq.cloud";
const char* mqtt_username = "cheminformatics";
const char* mqtt_password = "";
const int mqtt_port =8883;

/**** Secure WiFi Connectivity Initialisation *****/
WiFiClientSecure espClient;

/**** MQTT Client Initialisation Using WiFi Connection *****/
PubSubClient client(espClient);

unsigned long lastMsg = 0;
#define MSG_BUFFER_SIZE (50)
char msg[MSG_BUFFER_SIZE];

/****** root certificate *********/

static const char *root_ca PROGMEM = R"EOF(xxx
)EOF";

/************* Connect to WiFi ***********/
void setup_wifi() {
  delay(10);
  Serial.print("\nConnecting to ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  randomSeed(micros());
  Serial.println("\nWiFi connected\nIP address: ");
  Serial.println(WiFi.localIP());
}

/************* Connect to MQTT Broker ***********/
void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    String clientId = "ESP8266Client-";   // Create a random client ID
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    if (client.connect(clientId.c_str(), mqtt_username, mqtt_password)) {
      mySerial("connected with: " + clientId);

      client.subscribe("test");   // subscribe the topics here

    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");   // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

/***** Call back Method for Receiving MQTT messages and Switching LED ****/

void callback(char* topic, byte* payload, unsigned int length) {

  digitalWrite(LED_BUILTIN, HIGH);
  delay(100); 
  digitalWrite(LED_BUILTIN, LOW);  
  
  String incommingMessage = "";
  for (int i = 0; i < length; i++) incommingMessage+=(char)payload[i];

  mySerial("Message arrived ["+String(topic)+"]"+incommingMessage);

  //--- check the incomming message
    if( strcmp(topic,"led_state") == 0){
     if (incommingMessage.equals("1")) digitalWrite(LED_BUILTIN, HIGH);   // Turn the LED on
     else digitalWrite(LED_BUILTIN, LOW);  // Turn the LED off
  }

}

/**** Method for Publishing MQTT Messages **********/
void publishMessage(const char* topic, String payload , boolean retained){
  if (client.publish(topic, payload.c_str(), true))
      mySerial("Message publised ["+String(topic)+"]: " + payload);
}

/**** Application Initialisation Function******/
void setup() {
  pinMode(LED_BUILTIN, OUTPUT);

  Serial.begin(9600);
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println(F("SSD1306 allocation failed"));
    for (;;); // Don't proceed, loop forever
  }
  display.clearDisplay();
  display.setTextSize(1); // Small text
  display.setTextColor(SSD1306_WHITE);
  
  while (!Serial) delay(1);
  setup_wifi();

  #ifdef ESP8266
    espClient.setInsecure();
  #else
    espClient.setCACert(root_ca);      // enable this line and the the "certificate" code for secure connection
  #endif

  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);


}

/******** Main Function *************/
void loop() {
  mySerial(".");

  if (!client.connected()) reconnect(); // check if client is connected
  client.loop();

  unsigned long ms = millis(); // Get milliseconds since startup
  unsigned long seconds = ms / 1000; // Convert to seconds
  unsigned long minutes = seconds / 60; // Convert to minutes
  unsigned long hours = minutes / 60; // Convert to hours
  seconds = seconds % 60;
  minutes = minutes % 60;
  hours = hours % 24; // Ensure hours within 24-hour format

  // Convert hours, minutes, and seconds to a string
  String timestamp = String(hours) + " h, " + String(minutes) + " min and " + String(seconds) + " sec";
 
  String output;
  StaticJsonBuffer<200> jsonBuffer;
  JsonObject& doc = jsonBuffer.createObject();
  // Add values to the document
  doc["entity"] = "esp8266_test_unit";
  doc["event"] = "STATUS";
  doc["verb"] = "value"; 
  doc["noun"] = "timestamp"; 
  doc["data"] = timestamp; 
  doc.printTo(output);
  
  publishMessage("esp8266_test_unit", output, true);

    String LDRoutput;
  StaticJsonBuffer<200> jsonBufferLDR;
  JsonObject& LDRdoc = jsonBufferLDR.createObject();
  // Add values to the document
  LDRdoc["entity"] = "esp8266_test_unit";
  LDRdoc["event"] = "STATUS";
  LDRdoc["verb"] = "value"; 
  LDRdoc["noun"] = "LDR"; 
  LDRdoc["data"] = analogRead(ldrPin); 
  LDRdoc.printTo(LDRoutput);
  publishMessage("esp8266_test_unit", LDRoutput, true);
  


  delay(5000);

}
