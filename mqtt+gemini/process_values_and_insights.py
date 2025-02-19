import json

# def analyze_insights():
#     try:
#         with open("llm_insights.json", "r") as f:
#             responses = f.readlines()
#             return responses
#     except FileNotFoundError:
#         print("No responses found in llm_insights.json")
#         return []
    
    
    
def analyze_insights(filename="llm_insights.json"):
    try:
        with open(filename, "r") as f:
            insights = []
            for line in f:
                try:
                    insight = json.loads(line)
                    insights.append(insight)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON on line: {line.strip()} - Error: {e}")
            return insights
    except FileNotFoundError:
        return []
    

if __name__ == "__main__":
    responses = analyze_insights()
    for response in responses:
        # Assuming each response is on a separate line
        print("LLM Insights:")
        print(response.strip())  # Remove leading/trailing whitespace
        print("\n")  # Add a newline after each response
        print("++++++++++++++++++++++++++++++++++++++++++++++++\n")