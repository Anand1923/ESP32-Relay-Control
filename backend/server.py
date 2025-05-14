from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional
import time
import threading
import paho.mqtt.client as mqtt
from datetime import datetime

# FastAPI App Initialization
app = FastAPI()

# Database Simulation
class WateringSchedule(BaseModel):
    times: List[str]  # List of watering times (e.g., ['10:10', '21:10'])
    duration_minutes: int  # Duration for watering
    last_watered: Optional[str] = None

# In-Memory Store (Replace with PostgreSQL Logic Later)
watering_config = WateringSchedule(times=['10:10', '21:10'], duration_minutes=30)

# MQTT Broker Configuration
MQTT_BROKER = '0.0.0.0'  # Change to your MQTT broker IP
MQTT_PORT = 1883
MQTT_TOPIC = 'relay/control'

# MQTT Client Setup
client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

def send_watering_command(action: str):
    """Send watering command to MQTT Broker."""
    if action in ['ON', 'OFF']:
        client.publish(MQTT_TOPIC, action)
        print(f"[x] Watering Command Sent: {action}")


def schedule_watering():
    """Scheduled watering based on the configured times."""
    def check_and_water():
        current_time = datetime.now().strftime('%H:%M')
        if current_time in watering_config.times:
            print(f"[x] Triggered watering at {current_time}")
            send_watering_command('ON')
            watering_config.last_watered = current_time
            # Turn off after the specified duration
            threading.Timer(watering_config.duration_minutes * 60, send_watering_command, args=['OFF']).start()
    
    while True:
        check_and_water()
        time.sleep(60)  # Check every minute

# Start the Scheduler in a Thread
threading.Thread(target=schedule_watering, daemon=True).start()

@app.post('/trigger/manual')
def manual_trigger(background_tasks: BackgroundTasks):
    """API to manually trigger the watering system."""
    background_tasks.add_task(send_watering_command, 'ON')
    threading.Timer(watering_config.duration_minutes * 60, send_watering_command, args=['OFF']).start()
    return {'status': 'Manual watering triggered.'}


@app.post('/configure')
def configure_watering(schedule: WateringSchedule):
    """API to configure watering times and duration."""
    watering_config.times = schedule.times
    watering_config.duration_minutes = schedule.duration_minutes
    return {
        'status': 'Configuration updated.',
        'times': schedule.times,
        'duration_minutes': schedule.duration_minutes
    }


@app.get('/status')
def status_check():
    """API to check the current status."""
    return {
        'Last Watered': watering_config.last_watered,
        'Next Scheduled Watering': watering_config.times
    }
