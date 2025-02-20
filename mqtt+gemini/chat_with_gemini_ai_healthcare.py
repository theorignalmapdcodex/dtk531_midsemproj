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


def __get_gemini_client__() -> genai.GenerativeModel:
    genai.configure(api_key=the_api_key)
    gemini_model = genai.GenerativeModel("gemini-1.5-flash")
    return gemini_model

gemini_model = __get_gemini_client__()


# # Load historical insights at startup
health_insights = load_health_insights()

while True:
    user_input = input("👨🏾‍💻 Michael D. A-P: ")
    if user_input.lower() in ["exit", "quit", "bye"]:
        print("\n❤️ Have a great day! ❤️\n")
        break

    # Create a clean context prompt from historical data
    context_prompt = format_context_prompt(health_insights)
    
    # Combine context with user input
    full_prompt = f"{context_prompt}\n\nCurrent query: {user_input}"
    
    # Get response from Gemini
    try:
        gemini_output = query_gemini_api(full_prompt, gemini_model, conversation_history)
        
        # Display response in a clean format
        print("\n" + "─" * 14)
        print("♊ Gemini 1.5 Flash:")
        print("─" * 14)
        
        # Clean and format the output
        cleaned_lines = [line.strip() for line in gemini_output.split("\n") if line.strip()]
        for line in cleaned_lines:
            print(f"  - {line}")
        
        print("─" * 50 + "\n")
        
    except Exception as e:
        print(f"\nError generating response: {str(e)}")