import paho.mqtt.client as mqtt

# MQTT Broker details
MQTT_BROKER = "0.0.0.0"  # Change to your MQTT broker IP
MQTT_PORT = 1883
MQTT_TOPIC = "relay/control"

# Function to handle messages received
def on_message(client, userdata, msg):
    print(f"Received message on {msg.topic}: {msg.payload.decode()}")

# Function to handle connection
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe(MQTT_TOPIC)
    else:
        print(f"Connection failed with error code {rc}")

# Create MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to MQTT Broker
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

#for testing
while True:
    command = input("Enter ON/OFF to control relay: ").strip().upper()
    if command in ["ON", "OFF"]:
        client.publish(MQTT_TOPIC, command)
        print(f"Sent '{command}' to topic '{MQTT_TOPIC}'")
    else:
        print("Invalid command! Type ON or OFF.")
