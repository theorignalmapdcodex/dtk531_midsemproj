import json

# II. Importing the necessary functions for the Gemini API LLM Interaction to Work
from gemini_ai_call import *
from gemini_myapi import *

from process_values_and_insights import *

# III. Gemini API integration & Call
def __get_gemini_client__() -> genai.GenerativeModel:
    genai.configure(api_key=the_api_key)
    gemini_model = genai.GenerativeModel("gemini-1.5-flash")
    return gemini_model

gemini_model = __get_gemini_client__()

## Load previously generated LLM responses (if available and for context)
the_llm_health_insights = analyze_insights()


def __get_gemini_client__() -> genai.GenerativeModel:
    genai.configure(api_key=the_api_key)
    gemini_model = genai.GenerativeModel("gemini-1.5-flash")
    return gemini_model

gemini_model = __get_gemini_client__()

while True:
    user_input = input("👨🏾‍💻 Michael D. A-P: ")
    if user_input.lower() in ["exit", "quit", "bye"]:
        print("\n❤️ Have a great day! ❤️\n")
        break

    context_prompt = ""
    if the_llm_health_insights:
        context_prompt += "Here are some previous health insights and advice:\n"
        for insight_data in the_llm_health_insights:
            context_prompt += f"- Timestamp: {insight_data.get('timestamp')}\n"
            health_data = insight_data.get('health_data')
            if health_data:
                for key, value in health_data.items():
                    if key != 'timestamp':
                        context_prompt += f"  {key}: {value}\n"
            context_prompt += f"  Response: {insight_data.get('llm_response')}\n\n"

    full_prompt = context_prompt + user_input

    gemini_output = query_gemini_api(full_prompt, gemini_model, conversation_history)

    print("-" * 14)
    print("♊ Gemini 1.5 Flash:")
    print("-" * 14)
    for line in gemini_output.split("\n"):
        if line.strip():
            print(f"  - {line.strip()}")
    print("-" * 50 + "\n")