import requests
from prompts_loader import load
import json
from API.multiply import multiply_tool

API_URL = "http://127.0.0.1:5000/v1/completions"

PROMPT = """
You are a helpful AI. When a user asks for a calculation, do not perform the calculation yourself—instead, respond strictly in the following JSON format:

{"action": "multiply", "parameters": {"a": <first_number>, "b": <second_number>}}

Only use the "multiply" action for this test and do not include any additional text or actions. For example, for "What is 3 times 4?" respond exactly with:

{"action": "multiply", "parameters": {"a": 3, "b": 4}}

Do not include a "result" field or any other keys.
User: What is 3 times 4?

"""

def execute_tool(response_json):
    if response_json["action"] == "multiply":
        params = response_json["parameters"]
        return multiply_tool.func(params)

def generate_llm_answer():
    payload = {
        "prompt": PROMPT,
        "max_tokens": 500,
        "temperature": 0.1,
    }

    response = requests.post(API_URL, json=payload)

    if response.status_code == 200:
        data = response.json()
        result = data["choices"][0]["text"].strip()
        print("RAW LLM Response:", result)

        try:
            response_json = json.loads(result)
            if "action" in response_json:
                tool_result = execute_tool(response_json)
                print("tool execution result", tool_result)
                return tool_result
        except json.JSONDecodeError:
            pass

        return result
    else: 
        print(f"Erreur {response.status_code}: {response.text}")

generate_llm_answer()

    

