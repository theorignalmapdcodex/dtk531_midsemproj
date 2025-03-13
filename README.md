# VitalitySync: Empowering Health Monitoring with AI

## Product Description (Pitch) & Reflection

### Product Description
**VitalitySync: Stay Ahead, Stay Healthy**

Imagine spending hours at hospitals just to get basic vitals checked. VitalitySync revolutionizes this outdated process with a smart wearable app that continuously monitors your health metrics. It tracks vital signs like heart rate, blood oxygen, and temperature, securely storing this data and giving you control over who accesses it.

What sets VitalitySync apart is its innovative use of AI-powered health analytics. Using large language models (LLMs) like Gemini, we transform raw data into actionable insights delivered through text. The system communicates via MQTT protocols for real-time data transmission while maintaining strict security standards. You can instantly share your health history with healthcare providers, reducing wait times and improving care quality. The Python-based backend ensures smooth data processing, while AI helps detect anomalies before they become serious.

### Reflection
VitalitySync aligns with modern healthcare needs by solving the real problem of hospital wait times, offering an intuitive user experience through text interaction (with voice support in development), and providing clear value through time savings and better health insights. It scales gracefully with a modular architecture, ready for future hardware integration.

This project is personally compelling to me because, as a student, I’ve experienced the frustration of inaccessible health information and long hospital waits. VitalitySync empowers patients to take control of their health journey while maintaining privacy and trust. It’s not just an app—it’s a new standard for patient-centric healthcare delivery.

---

## Overview
VitalitySync is a software prototype for a wearable health monitoring app. It simulates health data collection, stores it in a local SQLite database, and uses MQTT for real-time data transmission. Users can set resting values via voice, monitor data in the background, and request AI-driven insights (via Gemini API) using text input. The system visualizes metrics with Matplotlib graphs and delivers conversational health advice through an AI assistant named Gemini.

---

## Features
- **Voice Input for Resting Values**: Set initial resting values (e.g., "Heart Rate 70") via microphone during setup.
- **Simulated Health Data**: Generates heart rate, SpO2, blood glucose, and temperature data for contexts like resting, running, walking, and exercising.
- **Real-Time Data Flow**: Publishes data via MQTT to `broker.hivemq.com`.
- **SQLite Storage**: Stores resting and current values in `health_data.db`.
- **Text Interaction**: Request insights with text (e.g., "Tell me about my health!").
- **AI Insights**: Gemini API provides structured health insights.
- **Visualization**: Matplotlib bar graphs compare resting vs. current metrics.

---

## Prerequisites
- Python 3.x
- Gemini API key (set in `gemini_myapi.py` as `the_api_key`).
- Internet connection for MQTT and Gemini API.

---

## Installation
1. **Install Dependencies**:
   ```bash
   pip install paho-mqtt matplotlib colorama SpeechRecognition pyaudio
   ```
   - `paho-mqtt`: For MQTT communication.
   - `matplotlib`: For graphing metrics.
   - `colorama`: For colored terminal output.

2. **Set Up Gemini API**:
   - Ensure `gemini_myapi.py` defines `the_api_key` with your Gemini API key.
   - `gemini_ai_call.py` should include necessary imports (e.g., `import google.generativeai as genai`).

---

## Configurations
- **MQTT Broker**: Uses `broker.hivemq.com` (port 1883) for real-time data transmission.
- **Database**: SQLite database (`health_data.db`) stores resting and current values.
- **Gemini API**: Configured in `gemini_myapi.py` with `the_api_key` and uses `gemini-1.5-flash` model.

---

## Usage
1. **Run the Publisher** (Simulates health data and publishes via MQTT):
   ```bash
   python generate_healthvalues.py
   ```
   - Using dummy/simulated data (resting values) when prompted (e.g., "Heart Rate 70, SpO2 98, Temperature 98.2")

2. **Run the Subscriber** (Listens for data and provides insights):
   ```bash
   python gain_healthinsightswithllm.py
   ```
   - Press `Ctrl+C` to stop and enter the interaction loop.
   - Use text to request insights (e.g., type "Tell me about my health!").

---

## Code Snippets (High-Level)

### `generate_healthvalues.py` (Key Part: Voice Input for Resting Values and Publishing)
```python
# Voice input for resting values (initial setup)
recognizer = sr.Recognizer()
with sr.Microphone() as source:
    print("Please say your resting values (e.g., 'Heart Rate 70, SpO2 98, Temperature 98.2')...")
    audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio).lower()
        resting_data = {}
        for part in text.split(","):
            if "heart rate" in part:
                resting_data["Heart_Rate"] = float(part.split()[-1])
            # [Similar parsing for SpO2, Blood_Glucose, Body_Temperature]
        store_resting_values(resting_data)
    except sr.UnknownValueError:
        print("Could not understand audio, using defaults.")
        store_resting_values({"Heart_Rate": 70, "SpO2": 98.5, "Blood_Glucose": 90, "Body_Temperature": 98.2})

# Publish simulated data via MQTT
publisher = mqtt.Client()
publisher.on_connect = on_connect
publisher.connect("broker.hivemq.com", 1883, 60)
publisher.loop_start()
```

### `gain_healthinsightswithllm.py` (Key Part: Text Interaction for Insights)
```python
# Text interaction loop
while True:
    print("\nWhat would you like to know about your health?")
    print("Say 'Tell me about my health!' to get insights, or 'exit' to leave.")
    user_input = input("Your choice: ").strip().lower()

    if user_input == "exit":
        print("\nSigning off with love! 💖 Take care! 🌟")
        break
    elif user_input == "tell me about my health!":
        print(f"Metrics available: {', '.join(available_metrics)} (or 'all')")
        metrics = input("Which metrics? (comma-separated, e.g., 'Heart_Rate, SpO2' or 'all'): ").strip()
        print(f"Situations: {', '.join(POSSIBLE_CONTEXTS)}")
        context = input("What were you doing? (e.g., 'running'): ").strip()
        # [Validation, visualization, and Gemini API call for insights follow]
```

---

## System Flow (One-Liner)
The system flow (detailed in `flowchart.ipynb`) covers voice setup for resting values, simulated data publishing via MQTT, text interaction for insights, and AI-driven analysis with visualization.

---

## Technology Choices
The technology stack (detailed in `technology_choices.ipynb`) includes MQTT for real-time data, SQLite for storage, Gemini API for AI insights, Python for flexibility, Matplotlib for visualization, and SpeechRecognition for voice input.

---

## References
1. [Grok AI](https://grok.com/): Assisted in refining code, and creating documentation (Grok 3, built by xAI).
2. [Google Gemini AI](https://deepmind.google/technologies/gemini/): Powers the conversational health insights (Gemini 1.5 Flash model via Google Generative AI API).
3. **Libraries**:
  - `paho-mqtt`: [https://pypi.org/project/paho-mqtt/](https://pypi.org/project/paho-mqtt/)
  - `matplotlib`: [https://matplotlib.org/](https://matplotlib.org/)
  - `colorama`: [https://pypi.org/project/colorama/](https://pypi.org/project/colorama/)

---

📚 **Author of Notebook:** Michael Dankwah Agyeman-Prempeh [MEng. DTI '25]