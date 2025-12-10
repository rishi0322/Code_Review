import requests

# 1. The code you want to review goes here!
#    Use triple quotes (""") to paste multi-line code easily.
code_sample = """
def bad_math(x, y):
    print("Adding numbers")
    if x == y:
        return x + y
    else:
        eval("x + y")  # <--- The AI should catch this!
"""

# 2. Setup the API connection
BASE_URL = "http://127.0.0.1:8000"

# 3. Create the Graph (Only needs to be done once, but fine to repeat)
graph_payload = {
    "nodes": [
        { "id": "extractor", "function_name": "extract_functions" },
        { "id": "complexity", "function_name": "check_complexity" },
        { "id": "reviewer", "function_name": "detect_basic_issues" }
    ],
    "edges": [
        { "source": "START", "target": "extractor" },
        { "source": "extractor", "target": "complexity" },
        { "source": "complexity", "target": "reviewer" },
        { "source": "reviewer", "target": "END" }
    ]
}
response = requests.post(f"{BASE_URL}/graph/create", json=graph_payload)
graph_id = response.json()["graph_id"]
print(f"Graph Created: {graph_id}")

# 4. Send YOUR code to the engine
print("\nSending code for review...")
run_payload = {
    "graph_id": graph_id,
    "initial_state": {
        "code": code_sample  # <--- This passes your code to the AI
    }
}

# ... previous code ...

result = requests.post(f"{BASE_URL}/graph/run", json=run_payload)
data = result.json()

print("\n--- Full Server Response ---")
print(data)  # <--- This is the important part!

# Only try to read issues if the run was successful
if data.get("status") == "failed":
    print("\n❌ WORKFLOW FAILED")
    print("Error Logs:", data.get("logs"))
else:
    final_state = data.get("final_state", {})
    issues = final_state.get("review_issues", [])
    
    print("\n--- AI Review Results ---")
    if not issues:
        print("✅ No issues found!")
    else:
        for issue in issues:
            print(f"[{issue['severity'].upper()}] {issue['description']}")
            print(f"   👉 Suggestion: {issue['suggestion']}\n")