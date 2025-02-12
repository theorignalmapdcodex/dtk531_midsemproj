# I. EXTRA/STRETCH: Importing saved LLM responses for Testing LLM Interactions via Scripting
import random
from process_responses import * 

# II. Importing the necessary functions for the Gemini API LLM Interaction to Work
from gemini_ai_call import * 
from gemini_myapi import *

# III. Gemini API integration & Call
def __get_gemini_client__() -> genai.GenerativeModel:
    genai.configure(api_key=the_api_key)
    gemini_model = genai.GenerativeModel("gemini-1.5-flash")
    return gemini_model

gemini_model = __get_gemini_client__()


## Load previously generated LLM responses (if available and for context)
llm_responses = read_responses()

# Create a list to store all extracted school names
all_schools = []

# Extract school names from LLM responses (assuming responses are in a specific format)
if llm_responses:
    for response in llm_responses:
        try:
            school_name = response.split()[0]  # Extract school name (adjust as needed)
            all_schools.append(school_name)
        except IndexError:
            print(f"Error extracting school name from response: {response}")

# Select 5 random schools
random_schools = random.sample(all_schools, k=2)

# Creating the test prompt
test_prompt = f"""
Based on the following 5 randomly selected colleges: {', '.join(random_schools)} and after searching on them, 
craft a brief but detailed guide for high school students preparing for the US college search process, 
focusing on the five random colleges.

The guide should include:

1.  **College Search Prep:** Briefly explain how students can best prepare.
2.  **5 Success Tips:** 5 actionable tips for maximizing application success.
3.  **Handling Unexpected Interview Questions:**  Advise on approaching unexpected questions like 
"What is the expanded form of MQTT?" (or similar).  Explain how to respond gracefully even when the answer is unknown, 
avoiding a negative impression.  Include advice on admitting lack of knowledge and pivoting to showcase relevant skills. 
"""

# Generating the Response
try:
    response = gemini_model.generate_content(test_prompt).text

    # Print Response with Structure
    print("\n" + "-" * 14)  # Separator line
    print(" 💻 LLM Response:")
    print("-" * 14)  # Separator line

    for line in response.split("\n"):
        if line.strip(): # Check if line is not empty or contains only whitespace
            print(f"  - {line.strip()}")  # Added .strip() to remove leading/trailing whitespace

    print("-" * 50 + "\n")  # Separator line and extra newline for spacing

except Exception as e:
    print(f"Error calling Gemini API: {e}")

print("❤️ Ready to Support your University Journey ❤️" + "\n")