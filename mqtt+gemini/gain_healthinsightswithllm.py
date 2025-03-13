# SUBSCRIBER

import paho.mqtt.client as mqtt
import time
import json
import sqlite3
import matplotlib.pyplot as plt
from colorama import init, Fore, Style

init(autoreset=True)

# Placeholder for Gemini API (assuming it’s correctly set up)
from gemini_ai_call import *
from gemini_myapi import *

# Importing the necessary functions for the Gemini API LLM Interaction to Work
def __get_gemini_client__() -> genai.GenerativeModel:
    genai.configure(api_key=the_api_key)
    gemini_model = genai.GenerativeModel("gemini-1.5-flash")
    return gemini_model

gemini_model = __get_gemini_client__()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Successfully connected to broker")
        client.subscribe("health_sensor/data")
    else:
        print(f"Connection failed with code {rc}")

def fetch_resting_values():
    conn = sqlite3.connect("health_data.db")
    c = conn.cursor()
    c.execute("SELECT metric, value FROM resting_values")
    resting = dict(c.fetchall())
    conn.close()
    return resting

def fetch_latest_current_values():
    conn = sqlite3.connect("health_data.db")
    c = conn.cursor()
    c.execute("SELECT metric, value, context FROM current_values WHERE timestamp = (SELECT MAX(timestamp) FROM current_values)")
    latest = c.fetchall()
    conn.close()
    return {metric: (value, context) for metric, value, context in latest}

def get_available_metrics():
    conn = sqlite3.connect("health_data.db")
    c = conn.cursor()
    c.execute("SELECT DISTINCT metric FROM resting_values")
    metrics = [row[0] for row in c.fetchall()]
    conn.close()
    return metrics

def plot_comparison(resting, current, context, metrics):
    metrics_to_plot = resting.keys() if "all" in metrics.lower() else [m for m in metrics.split(",") if m in resting]
    resting_vals = [resting[m] for m in metrics_to_plot]
    current_vals = [current.get(m, (0, ""))[0] for m in metrics_to_plot]
    
    fig, ax = plt.subplots(figsize=(8, 5))
    x = range(len(metrics_to_plot))
    ax.bar([i - 0.2 for i in x], resting_vals, 0.4, label="Resting", color="blue")
    ax.bar([i + 0.2 for i in x], current_vals, 0.4, label="Current", color="orange")
    ax.set_xticks(x)
    ax.set_xticklabels(metrics_to_plot, rotation=45)
    ax.set_ylabel("Value")
    ax.set_title(f"Health Metrics Comparison ({context.capitalize()})", fontsize=12, pad=10)
    ax.legend()
    plt.tight_layout()
    plt.show()

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    print(f"Received data (Context: {data['context']}): {data}")

def display_header():
    print(Fore.MAGENTA + Style.BRIGHT + f"""
{'='*60}
{' '*15}💖 VitalitySync 🩺
{'='*60}
{Fore.GREEN}🔬 Stay Ahead, Stay Healthy - Monitoring Your Well-being with AI ✨
{'-'*60}
""")

# Predefined list of possible contexts (situations)
POSSIBLE_CONTEXTS = ["resting", "running", "walking", "exercising"]

subscriber = mqtt.Client()
subscriber.on_connect = on_connect
subscriber.on_message = on_message
subscriber.connect("broker.hivemq.com", 1883, 60)  # Updated broker
subscriber.loop_start()

display_header()
print(Fore.CYAN + "Running in background. Stop with Ctrl+C to request insights." + Style.RESET_ALL)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nStopping subscriber...")
    subscriber.loop_stop()
    subscriber.disconnect()

    # Fetch data for visualization and insights
    resting_values = fetch_resting_values()
    latest_values = fetch_latest_current_values()
    available_metrics = get_available_metrics()
    
    # User interaction loop
    while True:
        print("\n" + Fore.YELLOW + "What would you like to know about your health?" + Style.RESET_ALL)
        print("Say 'Tell me about my health!' to get insights, or 'exit' to leave.")
        # print(Fore.CYAN + f" - Available metrics: {', '.join(available_metrics)} (or 'all')")
        # print(f" - Possible situations: {', '.join(POSSIBLE_CONTEXTS)}" + Style.RESET_ALL)
        user_input = input("Your choice: ").strip().lower()

        if user_input == "exit":
            print(Fore.MAGENTA + "\nSigning off with love! 💖 Take care! 🌟" + Style.RESET_ALL)
            break
        elif user_input == "tell me about my health!":
            print(Fore.CYAN + f"Metrics available: {', '.join(available_metrics)} (or 'all')")
            metrics = input("Which metrics? (comma-separated, e.g., 'Heart_Rate, SpO2' or 'all'): ").strip()
            print(Fore.CYAN + f"Situations: {', '.join(POSSIBLE_CONTEXTS)}")
            context = input("What were you doing? (e.g., 'running'): ").strip()

            # Validate and process metrics
            if not metrics or not context:
                print(Fore.RED + "Please provide both metrics and context!" + Style.RESET_ALL)
                continue
            valid_metrics = [m.strip() for m in metrics.split(",") if m.strip() in available_metrics or m.lower() == "all"]
            if not valid_metrics and metrics.lower() != "all":
                print(Fore.RED + f"Invalid metrics! Choose from: {', '.join(available_metrics)} or 'all'" + Style.RESET_ALL)
                continue
            if context not in POSSIBLE_CONTEXTS:
                print(Fore.RED + f"Invalid context! Choose from: {', '.join(POSSIBLE_CONTEXTS)}" + Style.RESET_ALL)
                continue

            current_subset = (
                {k: v[0] for k, v in latest_values.items()} if "all" in metrics.lower()
                else {k: v[0] for k, v in latest_values.items() if k in valid_metrics}
            )

            # Visualize with enhanced labels
            plot_comparison(resting_values, latest_values, context, metrics)
            
            # Structured prompt for LLM
            prompt = f"""
            You are Gemini, a friendly health AI assistant.
            
            A patient is using a personal health sensor and has provided the following data.
            
            Please provide general advice and insights based on this data and the current context. 
            Compare the user's current health metrics with their resting values and provide structured insights based on the context '{context}'.
             
            Structure your response clearly using bullet points for each metric.
                
            Do not give medical diagnoses or treatment recommendations.
            If any values are outside of typical ranges for their current activity, mention that the patient should consult with a healthcare professional.
            Be respectful and avoid alarming language.

            Resting Values: {json.dumps(resting_values)}
            Current Values: {json.dumps(current_subset)}
            Context: {context}
            """
            response = gemini_model.generate_content(prompt).text
            print("\n" + Fore.GREEN + "Gemini's Insights:" + Style.RESET_ALL)
            print(response)
        else:
            print(Fore.RED + "Oops! I didn’t catch that. Try 'Tell me about my health!' or 'exit'." + Style.RESET_ALL)