# publisher.py
import paho.mqtt.client as mqtt
import time
import json
import random
from datetime import datetime

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Successfully connected to broker")
    else:
        print(f"Connection failed with code {rc}")

# Create publisher client
publisher = mqtt.Client()
publisher.on_connect = on_connect

# Connect to public broker
print("Connecting to broker...")

# (broker, port, keepalive)
publisher.connect("test.mosquitto.org", 1883, 60)
publisher.loop_start()

try:
    while True:
        health_data = {
            "SpO2": round(random.uniform(90, 100), 1),  # Realistic SpO2 range
            "Blood_Glucose": random.randint(70, 150),  # Realistic Blood Glucose range
            "Heart_Rate": random.randint(60, 100),  # Realistic Heart Rate range
            "Dehydration_Level": round(random.uniform(0, 10), 1), # Example dehydration scale (0-10)
            "Pulse": random.randint(60, 100), # Same range as heart rate (often similar)
            "Body_Temperature": round(random.uniform(97.0, 99.0), 1), # Realistic body temperature range
            "timestamp": datetime.now().isoformat()
        }

        topic = "gemini_llm_test/healthsensor" # More appropriate topic name
        publisher.publish(
            topic,
            json.dumps(health_data),
            qos=1
        )
        print(f"Published to {topic}: {health_data}")
        time.sleep(1)  # Adjust sleep time as needed

except KeyboardInterrupt:
    print("Stopping publisher...")
    publisher.loop_stop()
    publisher.disconnect()