# AI-Powered Contextual Health Monitoring System

## Overview
This system provides intelligent health monitoring by combining simulated sensor data with context-aware AI analytics. Using Gemini 1.5 Flash LLM, it delivers personalized health insights based on different activity contexts while maintaining user privacy and data security.

## System Architecture

### Components
1. **Data Generation Layer**
   - Simulated health sensor data with contextual awareness
   - Supports multiple contexts: default, pregnant, exercising, working
   - Metrics monitored: SpO2, Blood Glucose, Heart Rate, Dehydration Level, Pulse, Body Temperature
   - Dynamic context switching for realistic simulation

2. **Communication Layer**
   - MQTT protocol for reliable real-time data transmission
   - Publisher service with context-aware data generation
   - Subscriber service with specialized context handling
   - Quality of Service (QoS) level 1 for reliable delivery

3. **Analytics Layer**
   - Gemini 1.5 Flash LLM for intelligent health analysis
   - Context-specific prompts for tailored insights
   - Historical data tracking and analysis
   - Non-diagnostic health insights with appropriate language

4. **User Interface**
   - Color-coded CLI with clear section demarcation
   - Real-time health status monitoring
   - Interactive query system for personalized advice
   - Historical data visualization and insights

### Context-Aware Features
- Pregnancy monitoring with adjusted vital ranges
- Exercise activity tracking with dynamic thresholds
- Workplace wellness monitoring
- Default monitoring for general health tracking

## Safety and Privacy Features
- Non-diagnostic advisory system with clear disclaimers
- Context-appropriate language processing
- Secure data transmission via MQTT
- Local data storage in JSON format
- Professional medical referral suggestions when needed

## Technical Implementation
The system consists of three main Python components:

1. `generate_healthvalues.py`: 
   - Generates context-aware health data
   - Implements dynamic context switching
   - Maintains realistic vital sign ranges per context

2. `gain_healthinsightswithllm.py`:
   - Processes incoming health data
   - Applies context-specific analysis
   - Generates tailored health insights
   - Stores historical data

3. `chat_with_gemini_ai_healthcare.py`:
   - Provides interactive user interface
   - Supports natural language queries
   - Maintains conversation context
   - Displays formatted insights

## Getting Started
1. Install required dependencies:
   ```bash
   pip install paho-mqtt google.generativeai colorama
   ```

2. Set up environment variables:
   ```bash
   export GEMINI_API_KEY='your_api_key_here'
   ```

3. Run the components in sequence:
   ```bash
   python generate_healthvalues.py
   python gain_healthinsightswithllm.py
   python chat_with_gemini_ai_healthcare.py
   ```

## Configuration
The system includes predefined health ranges for different contexts:
- Default: Standard healthy ranges
- Pregnant: Adjusted for pregnancy-related changes
- Exercising: Modified for physical activity
- Working: Tailored for workplace scenarios

## Data Storage
Health insights are stored in `llm_insights.json` with the following structure:
```json
{
    "timestamp": "ISO-8601 timestamp",
    "health_data": {
        "context": "activity context",
        "metrics": "health measurements"
    },
    "llm_response": "AI-generated insights"
}

## References
1. [Google Gemini AI](https://deepmind.google/technologies/gemini/) - Code generation
2. [ClaudeAI](https://claude.ai/new) - Image Generation

---

📚 **Author of Notebook:** Michael Dankwah Agyeman-Prempeh [MEng. DTI '25]