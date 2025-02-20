import paho.mqtt.client as mqtt
import time
import json
import random
from datetime import datetime

# Define health ranges for different contexts
HEALTH_RANGES = {
    "default": {
        "SpO2": (95, 100),
        "Blood_Glucose": (70, 140),
        "Heart_Rate": (60, 100),
        "Dehydration_Level": (0, 5),
        "Pulse": (60, 100),
        "Body_Temperature": (97.0, 99.0)
    },
    "pregnant": {
        "SpO2": (95, 100),
        "Blood_Glucose": (70, 140),  # Can be higher during pregnancy
        "Heart_Rate": (70, 90),      # Typically elevated during pregnancy
        "Dehydration_Level": (0, 4), # More sensitive to dehydration
        "Pulse": (70, 90),           # Usually higher during pregnancy
        "Body_Temperature": (97.5, 99.5)  # Slightly elevated
    },
    "exercising": {
        "SpO2": (95, 100),
        "Blood_Glucose": (70, 150),   # Can vary during exercise
        "Heart_Rate": (90, 170),      # Elevated during exercise
        "Dehydration_Level": (2, 7),  # Higher during exercise
        "Pulse": (90, 170),           # Elevated during exercise
        "Body_Temperature": (98.0, 101.0)  # Higher during exercise
    },
    "working": {
        "SpO2": (95, 100),
        "Blood_Glucose": (70, 140),
        "Heart_Rate": (60, 90),
        "Dehydration_Level": (0, 6),  # Can be higher if sedentary
        "Pulse": (60, 90),
        "Body_Temperature": (97.0, 99.0)
    }
}

def generate_health_data(context="default"):
    ranges = HEALTH_RANGES[context]
    return {
        "SpO2": round(random.uniform(*ranges["SpO2"]), 1),
        "Blood_Glucose": random.randint(*ranges["Blood_Glucose"]),
        "Heart_Rate": random.randint(*ranges["Heart_Rate"]),
        "Dehydration_Level": round(random.uniform(*ranges["Dehydration_Level"]), 1),
        "Pulse": random.randint(*ranges["Pulse"]),
        "Body_Temperature": round(random.uniform(*ranges["Body_Temperature"]), 1),
        "timestamp": datetime.now().isoformat(),
        "context": context  # Add context to the data
    }
    

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
    # Simulate different contexts
    contexts = ["default", "pregnant", "exercising", "working"]
    current_context_index = 0
    
    while True:
        # Rotate through contexts every 5 iterations
        if random.randint(1, 5) == 1:
            current_context_index = (current_context_index + 1) % len(contexts)
        
        context = contexts[current_context_index]
        health_data = generate_health_data(context)
        
        topic = "gemini_llm_test/healthsensor"
        publisher.publish(
            topic,
            json.dumps(health_data),
            qos=1
        )
        print(f"Published to {topic} (Context: {context}): {health_data}")
        time.sleep(1)

except KeyboardInterrupt:
    print("Stopping publisher...")
    publisher.loop_stop()
    publisher.disconnect()