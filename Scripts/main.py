import requests
import pandas
from prompts_loader import load

API_URL = "http://127.0.0.1:5000/v1/completions"
CSV_URL = "Data/first-iterations/Amazon-global-dresses-sample50-0bis.csv"

CHARGED_FILE = pandas.read_csv(CSV_URL, delimiter=";")
PROMPT = load("v1")

def process_verbatim():
    for row in CHARGED_FILE.itertuples():
        print(row)
        verbatim = row.review_text
        generate_llm_answer(verbatim)

def generate_llm_answer(verbatim):
    formatted_prompt = PROMPT.format(verbatim=verbatim)

    payload = {
        "prompt": formatted_prompt,
        "max_tokens": 500,
        "temperature": 0.1,
    }

    response = requests.post(API_URL, json=payload)

    if response.status_code == 200:
        data = response.json()
        print("Answer", data["choices"][0]["text"])
        return data["choices"][0]["text"]
    else: 
        print(f"Erreur {response.status_code}: {response.text}")

process_verbatim()

    

