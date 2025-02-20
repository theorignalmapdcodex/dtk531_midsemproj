import json

def load_health_insights():
    """
    Reads and processes the health insights file with proper error handling.
    Returns a list of valid insight entries.
    """
    try:
        with open("llm_insights.json", "r") as f:
            # Read the file contents and split by newlines to handle multiple JSON objects
            insights = []
            for line in f:
                try:
                    if line.strip():  # Skip empty lines
                        insight = json.loads(line.strip())
                        insights.append(insight)
                except json.JSONDecodeError:
                    continue  # Skip invalid JSON entries
            return insights
    except FileNotFoundError:
        return []  # Return empty list if file doesn't exist
    except Exception as e:
        print(f"Error loading insights: {e}")
        return []

def format_context_prompt(insights):
    """
    Creates a clean, formatted context prompt from historical insights.
    Focuses on relevant information without exposing raw JSON.
    """
    if not insights:
        return ""
    
    context = "Previous health insights:\n"
    # Only use the last 3 insights to keep context relevant
    for insight in insights[-3:]:
        timestamp = insight.get('timestamp', 'Unknown time')
        health_data = insight.get('health_data', {})
        
        # Format timestamp for readability
        context += f"\nTime: {timestamp}\n"
        context += "Measurements:\n"
        
        # Add health measurements in a clean format
        for key, value in health_data.items():
            if key != 'timestamp' and key != 'context':
                context += f"- {key}: {value}\n"
    
    return context

# def analyze_insights(filename="llm_insights.json"):
#     try:
#         with open(filename, "r") as f:
#             insights = []
#             for line in f:
#                 try:
#                     insight = json.loads(line)
#                     insights.append(insight)
#                 except json.JSONDecodeError as e:
#                     print(f"Error decoding JSON on line: {line.strip()} - Error: {e}")
#             return insights
#     except FileNotFoundError:
#         return []

# if __name__ == "__main__":
#     insights = analyze_insights()
#     if insights:  # Check if any insights were loaded
#         for insight in insights:
#             print("LLM Insights:")

#             # Access and print the specific data you want
#             timestamp = insight.get("timestamp")
#             health_data = insight.get("health_data")
#             llm_response = insight.get("llm_response")

#             if timestamp:
#                 print(f"  Timestamp: {timestamp}")
#             if health_data:
#                 print("  Health Data:")
#                 for key, value in health_data.items():
#                     print(f"    {key}: {value}")
#             if llm_response:
#                 print("  LLM Response:")
#                 # Print the multiline response nicely
#                 for line in llm_response.splitlines():  # Split into lines
#                     print(f"    {line}")

#             print("\n++++++++++++++++++++++++++++++++++++++++++++++++\n")
#     else:
#         print("No insights found.")  # Handle the case where no insights are loaded