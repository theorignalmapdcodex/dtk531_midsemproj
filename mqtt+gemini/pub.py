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
    with open('../datasets/schoolsdata.json', 'r') as f:
        schools = json.load(f)

    while True:
        
        # Randomly select a school from the list
        school = random.choice(schools)
        
        school_data = {
            "Unit_ID": school["Unit ID"],
            "Institution_Name": school["Institution Name"],
            "Avg_Net_Price": school["Avg Net Price"],
            "City": school["City"],
            "State": school["State"],
            "Zip_Code": school["Zip Code"],
            "Category": school["Category"],
            "SAT_Reading_75th": school["SAT Reading 75th"],
            "SAT_Math_75th": school["SAT Math 75th"],
            "timestamp": datetime.now().isoformat()
        }

        topic = "gemini_llm_test/uscolleges/schdetails"
        publisher.publish(
            topic,
            json.dumps(school_data),
            qos=1
        )
        print(f"Published to {topic}: {school_data}")
        time.sleep(1)  # Adjust sleep time as needed
        
except KeyboardInterrupt:
    print("Stopping publisher...")
    publisher.loop_stop()
    publisher.disconnect()