# subscriber.py
import paho.mqtt.client as mqtt
import time
import json
import re  # For cleaning up LLM output

from gemini_ai_call import *  # Make sure these imports are correct
from gemini_myapi import *

# Importing the necessary functions for the Gemini API LLM Interaction to Work
def __get_gemini_client__() -> genai.GenerativeModel:
    genai.configure(api_key=the_api_key)
    gemini_model = genai.GenerativeModel("gemini-1.5-flash")
    return gemini_model

gemini_model = __get_gemini_client__()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Successfully connected to the Health broker")
        client.subscribe("gemini_llm_test/healthsensor")  # Subscribe to the correct topic
    else:
        print(f"Connection failed with code {rc}")

def on_message(client, userdata, msg):
    received_message = msg.payload.decode()

    try:
        data = json.loads(received_message)
        # Extract relevant health data points
        spo2 = data.get("SpO2")
        blood_glucose = data.get("Blood_Glucose")
        heart_rate = data.get("Heart_Rate")
        dehydration = data.get("Dehydration_Level")
        pulse = data.get("Pulse")
        temperature = data.get("Body_Temperature")
        timestamp = data.get("timestamp")

    except (json.JSONDecodeError, KeyError) as e:  # Handle both JSON and key errors
        print(f"Error processing message: {e}")
        return  # Exit early if there's a problem with the data

    print(f"\n✨ Health Data Received at {timestamp} ✨\n{'-'*50}\n")
    print(f"SpO2: {spo2}, Blood Glucose: {blood_glucose}, Heart Rate: {heart_rate}, Dehydration: {dehydration}, Pulse: {pulse}, Temperature: {temperature}\n")

    prompt = f"""
    You are a helpful and informative health advisor.  A patient is using a personal health sensor and has provided the following data.  Please provide general advice and insights based on this data.  Do not give medical diagnoses or treatment recommendations.  If any values are outside of typical ranges, mention that the patient should consult with a healthcare professional.  Be respectful and avoid alarming language.  Structure your response clearly using bullet points for each metric.

    ```json
    {received_message}
    ```
    """

    try:
        response = gemini_model.generate_content(prompt).text

        # Clean up LLM output (remove extra newlines, etc.)
        cleaned_response = re.sub(r'\n+', '\n', response).strip()

        print("\nB. Health Insights and Advice:\n")
        for line in cleaned_response.split("\n"):
            print(f" - {line}") # Bullet points for each piece of advice
        print("\n")

        # Save LLM responses (append to the file)
        with open("llm_insights.json", "a") as f:
            json.dump({"timestamp": timestamp, "health_data": data, "llm_response": cleaned_response}, f, indent=4) # Save the data, timestamp and response
            f.write("\n")

    except Exception as e:
        print(f"🚨 Error calling Gemini API: {e}")

    print(f"\n{'-'*50}\n✨ End of Health Analysis ✨\n🩺💖\n")

#################################################################################################################
                    #---------- Creating the subscriber client ---------#
subscriber = mqtt.Client()
subscriber.on_connect = on_connect
subscriber.on_message = on_message

# Connect to public broker
print("Connecting to the University broker...")
subscriber.connect("test.mosquitto.org", 1883, 60)


#################################################################################################################
                    #---------- Customizing Console.log Header ---------#

from colorama import init, Fore, Style

init(autoreset=True)  # Initialize colorama

def display_health_header():
    print(Fore.MAGENTA + Style.BRIGHT + f"""
{'='*60}
{' '*15}💖 HEALTH INSIGHTS 🩺
{'='*60}
{Fore.GREEN}🔬 Monitoring Your Well-being with AI ✨
{'-'*60}
{Fore.YELLOW}Explore • Learn • Empower
{'-'*60}
{Style.RESET_ALL}
""")

def main_menu():  # You might not need a menu in this case, but I'll leave it
    display_health_header()
    print(Fore.CYAN + """
WHAT TO EXPECT:
-----------
1. 📈 Real-time Health Monitoring
2. 🧠 AI-Powered Insights
3. 🤝 Personalized Advice (General)

    """ + Style.RESET_ALL)

# # Call the header display function (you can call it directly)
# display_health_header() # No need for a menu if just showing health data

# Call the function to demonstrate
main_menu()
#################################################################################################################

# Start the subscriber loop
subscriber.loop_start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping subscriber...")
    subscriber.loop_stop()
    subscriber.disconnect()