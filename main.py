import requests
import pandas

API_URL = "http://127.0.0.1:5000/v1/completions"
CSV_URL = "Data/first-iterations/Amazon-global-dresses-sample50-1.csv"

CHARGED_FILE = pandas.read_csv(CSV_URL, delimiter=";")

def read_csv_to_extract_verbatim():
    for row in CHARGED_FILE.itertuples():
        print("verbatim", row.review_text)

def generate_llm_answer():
    prompt = "What is the Ultimate Answer to Life, The Universe, and Everything"

    payload = {
        "prompt": prompt,
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

read_csv_to_extract_verbatim()

    

