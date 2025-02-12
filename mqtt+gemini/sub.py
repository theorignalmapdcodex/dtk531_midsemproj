# subscriber.py
import paho.mqtt.client as mqtt
import time
import json

from gemini_ai_call import * 
from gemini_myapi import *

# 0. Importing the necessary functions for the Gemini API LLM Interaction to Work
def __get_gemini_client__() -> genai.GenerativeModel:
    genai.configure(api_key=the_api_key)
    gemini_model = genai.GenerativeModel("gemini-1.5-flash")
    return gemini_model

gemini_model = __get_gemini_client__()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Successfully connected to the University broker")
        # Subscribe to topic
        client.subscribe("gemini_llm_test/uscolleges/schdetails")
    else:
        print(f"Connection failed with code {rc}")
      

def on_message(client, userdata, msg):
    
    # 1. Receive and decode the MQTT message
    received_message = msg.payload.decode()

    try:
        data = json.loads(received_message) # Parse the JSON
        school_name = data.get("Institution_Name")  # Extract school name, handle missing key
    except json.JSONDecodeError:
        school_name = "Invalid JSON Received" # Handle JSON decoding errors
    except Exception as e:
        school_name = f"Error: {e}"

    # Improved separator with emojis and a clearer title with the school name
    print(f"\n✨ {school_name} Insights & History 📜\n{'-'*50}\n")

    print("A. Message Payload From Developed JSON file via a subscription topic:\n", received_message, "\n")

    # 2. Create a prompt for the Gemini API
    prompt = f"""
                Generate a comprehensive summary analysis of this school and its corresponding data, 
                tailored for a student considering college in the US.  

                Specifically, please include the following:

                *   A detailed overview of the school's academics, student life, and campus culture.
                *   Information about the year the school was founded.
                *   One historic event that significantly shaped the college's identity.
                *   One unique aspect that makes this university stand out from other institutions.  This could be a special program, a distinctive research focus, a unique tradition, or any other factor that sets it apart.

                Here is the information about the school:

                ```json
                {received_message}
              """

    # 3. Call the Gemini API
    try:
        response = gemini_model.generate_content(prompt).text
        print("\nB. Gemini LLM's Response:\n")
        for line in response.split("\n"):
            print(f"  - {line}")
        print("\n")
        
        # Saving only the response to a JSON file as context for future LLM interactions
        with open("llm_responses.json", "a") as f:
            json.dump(response, f, indent=4)
            f.write("\n") 
    except Exception as e:
        print(f"🚨 Error calling Gemini API: {e}")  # Added an error emoji

    # 4. Separator (Now with emojis and a nicer look including the school name)
    print(f"\n{'-'*50}\n✨ End of {school_name} Analysis ✨\n🎓🏫\n") # More emojis and a clear "End of Analysis" message with the school's name

# Create subscriber client
subscriber = mqtt.Client()
subscriber.on_connect = on_connect
subscriber.on_message = on_message

# Connect to public broker
print("Connecting to the University broker...")
subscriber.connect("test.mosquitto.org", 1883, 60)


#################################################################################################################
                    #---------- Customizing Console.log Header ---------#

from colorama import init, Fore, Style

init(autoreset=True)  # Initialize colorama for cross-platform color support

def display_app_header():
    print(Fore.CYAN + Style.BRIGHT + f"""
{'='*60}
{' '*10}🏛️ CAMPUS CHRONICLES 🎓
{'='*60}
{Fore.GREEN}🔍 Discover the Hidden Stories of Academic Institutions! 📜✨
{'-'*60}
{Fore.YELLOW}Explore • Learn • Connect • Inspire
{'-'*60}
{Style.RESET_ALL}
""")

def main_menu():
    display_app_header()
    print(Fore.CYAN + """
WHAT TO EXPECT:
-----------
1. 🏫 University Profiles
2. 📚 Historical Archives
3. 🌐 Campus Insights

    """ + Style.RESET_ALL)

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