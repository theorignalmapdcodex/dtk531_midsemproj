import google.generativeai as genai
from typing import List, Optional

# Function to query Gemini API (Text)
def query_gemini_api(user_text: str, gemini_model: genai.GenerativeModel) -> str:
    """
    Calls the Gemini API with the user's text input and returns the response.

    Args:
        user_text (str): The text input from the user.
        gemini_model (GenerativeModel): Initialized Gemini model instance.

    Returns:
        str: The generated response from the Gemini API.
    """
    try:
        # Generate content using Gemini model's structured prompt
        response = gemini_model.generate_content(user_text)  # User's query
        
        # Resolve the response to ensure all processing is completed
        response.resolve()
        
        # Return the text content from the response
        return response

    except Exception as e:
        # Handle and return any errors
        return f"An error occurred: {e}"