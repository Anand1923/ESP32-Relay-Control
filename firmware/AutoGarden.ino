#include <WiFi.h>
#include <PubSubClient.h>

// WiFi & MQTT Configuration
const char* WIFI_SSID = "PK";
const char* WIFI_PASS = "****";
const char* MQTT_SERVER = "192.168.1.100";  //Broker ip
const int MQTT_PORT = 1883;
const char* MQTT_TOPIC = "relay/control";

const int relayPin = 26;  // GPIO connected to Relay

WiFiClient espClient;
PubSubClient client(espClient);

void callback(char* topic, byte* message, unsigned int length) {
    String msg = "";
    for (int i = 0; i < length; i++) {
        msg += (char)message[i];
    }
    Serial.print("MQTT Message: ");
    Serial.println(msg);

    if (msg == "ON") {
        digitalWrite(relayPin, HIGH);
        Serial.println("Relay ON");
    } else if (msg == "OFF") {
        digitalWrite(relayPin, LOW);
        Serial.println("Relay OFF");
    }
}

void setup() {
    Serial.begin(115200);
    pinMode(relayPin, OUTPUT);
    
    // Connect to WiFi
    Serial.print("Connecting to WiFi...");
    WiFi.begin(WIFI_SSID, WIFI_PASS);
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.print(".");
    }
    Serial.println("Connected!");

    // Connect to MQTT
    client.setServer(MQTT_SERVER, MQTT_PORT);
    client.setCallback(callback);

    while (!client.connected()) {
        Serial.print("Connecting to MQTT...");
        if (client.connect("ESP32Client")) {
            Serial.println("Connected to MQTT!");
        } else {
            Serial.println("Failed, retrying in 5s...");
            delay(5000);
        }
    }
    client.subscribe(MQTT_TOPIC);
}

void loop() {
    client.loop();  // Listen for MQTT messages
}
