import json

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
    insights = analyze_insights()
    if insights:  # Check if any insights were loaded
        for insight in insights:
            print("LLM Insights:")

            # Access and print the specific data you want
            timestamp = insight.get("timestamp")
            health_data = insight.get("health_data")
            llm_response = insight.get("llm_response")

            if timestamp:
                print(f"  Timestamp: {timestamp}")
            if health_data:
                print("  Health Data:")
                for key, value in health_data.items():
                    print(f"    {key}: {value}")
            if llm_response:
                print("  LLM Response:")
                # Print the multiline response nicely
                for line in llm_response.splitlines():  # Split into lines
                    print(f"    {line}")

            print("\n++++++++++++++++++++++++++++++++++++++++++++++++\n")
    else:
        print("No insights found.")  # Handle the case where no insights are loaded