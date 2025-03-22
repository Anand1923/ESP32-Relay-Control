# ESP32-Relay-Control-

This project is an **automated garden watering system** using an **ESP32, relay module, solenoid valve, and a Python backend with MQTT**. The system allows remote control of a solenoid valve via MQTT messages, enabling automated irrigation.

## Components Used

| Component   | Description | Price (INR) | Link |
|------------|-------------|------------|------|
| **ESP32** | Microcontroller for processing MQTT commands | 519 | [ESP32](https://www.amazon.in/dp/B071XP56LM?ref=ppx_yo2ov_dt_b_fed_asin_title) |
| **Relay Module** | 3.3V 1-Channel Relay for switching solenoid | 129 | [Relay](https://rees52.com/products/3-3v-1-channel-relay-module-1-channel-3-3v-low-level-trigger-relay-module-optocoupler-isolation-terminal-for-arduino-rs5660?variant=44209831346343) |
| **Solenoid Valve** | Controls water flow based on relay signal | 300 | [Solenoid](https://www.amazon.in/dp/B09TKBZ4DT?ref=ppx_yo2ov_dt_b_fed_asin_title) |
| **Jumper Wires** | For making connections | 34 | [Jumper Wires](https://rees52.com/products/female-to-female-jumper-wires-20cm-connector-jumper-wires-rk005?variant=44583514996903) |
| **5V Power Adapter** | Used to power ESP32 | 149 | [Power Adapter](https://www.amazon.in/dp/B0BNDWG6BN?ref=ppx_yo2ov_dt_b_fed_asin_title) |
| **12V Power Adapter** | Used to power solenoid valve | - | Any standard 12V adapter |

---

## Circuit Wiring

1. **ESP32 to Relay Module:**
   - **VCC** (ESP32) → **VCC** (Relay)
   - **GND** (ESP32) → **GND** (Relay)
   - **GPIO26** (ESP32) → **IN** (Relay)

2. **Relay Module to Solenoid Valve and Power Adapter:**
   - **COM** (Relay) → **+12V** from **12V Adapter**
   - **NO** (Relay) → **Solenoid Positive (+)**
   - **Solenoid Negative (-)** → **12V Adapter Negative (-)**

3. **ESP32 Power Supply:**
   - Powered via **USB cable** connected to your PC or **5V adapter**.

---

## Software Setup

### 1. Install Arduino IDE and Libraries

- Install [Arduino IDE](https://www.arduino.cc/en/software)
- Install ESP32 Board:
  1. Go to **File → Preferences**
  2. Add the following URL to "Additional Board Manager URLs":
     ```
     https://dl.espressif.com/dl/package_esp32_index.json
     ```
  3. Open **Boards Manager**, search for **ESP32**, and install.

- Install required libraries:
  - `PubSubClient` (for MQTT)
  - `WiFi` (for WiFi connectivity)

### 2. Flash ESP32 Code

1. Open `firmware/main.ino` in Arduino IDE.
2. Modify `ssid` and `password` with your WiFi credentials.
3. Modify `mqttServer` with your **MQTT Broker IP**.
4. Select **ESP32 Dev Module** as the board and upload the code.

### 3. Run the Python Backend

1. Install Python 3 and required libraries:
   ```sh
   pip install requirement.txt
   ```
2. Start the MQTT broker (if using Mosquitto):
   ```sh
   mosquitto -v
   ```
3. Run the backend server:
   ```sh
   python server.py
   ```

### 4. Control the Solenoid Valve

To turn ON the solenoid:
```sh
mosquitto_pub -h 192.168.31.79 -t "relay/control" -m "ON"
```

To turn OFF the solenoid:
```sh
mosquitto_pub -h 192.168.31.79 -t "relay/control" -m "OFF"
```

Or send ON or OFF command from Python server


Python server is just a environment for testing. Use your own control logic for relay switching.


---

## Troubleshooting

1. **ESP32 Not Connecting to WiFi?**
   - Check if SSID and password are correct.
   - Restart ESP32 and router.

2. **No MQTT Messages Received?**
   - Ensure `mosquitto` is running on the MQTT broker.
   - Check if ESP32 is successfully connected to MQTT.

3. **Solenoid Not Opening?**
   - Ensure 12V adapter is properly connected.
   - Verify relay connections (COM and NO).

---

## Future Improvements

- Add soil moisture sensor for automatic watering.
- Implement a mobile/web interface for control.
- Store logs of watering events.

---

Feel free to modify and improve! 🚀