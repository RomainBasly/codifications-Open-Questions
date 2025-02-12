import requests
import pandas
from prompts_loader import load
import re
import numpy as np

API_URL = "http://127.0.0.1:5000/v1/completions"
CSV_URL = "Data/first-iterations/Amazon-global-dresses-sample50-0bis.csv"

CHARGED_FILE = pandas.read_csv(CSV_URL, delimiter=";")
PROMPT = load("v3")

def process_verbatims_and_extract_csv():
    max_columns = 12

    if "Analysis" not in CHARGED_FILE.columns:
        CHARGED_FILE["Analysis"] = pandas.Series([np.nan] * len(CHARGED_FILE), dtype="object")

    for i in range(1, 13):
        if f"review_{i}" not in CHARGED_FILE.columns:
            CHARGED_FILE[f"review_{i}"] = np.nan
        CHARGED_FILE[f"review_{i}"] = CHARGED_FILE[f"review_{i}"].astype(pandas.Int64Dtype())

    for index, row in CHARGED_FILE.iterrows():
        verbatim = row.review_text
        print("verbatim treated", verbatim)
        answer = generate_llm_answer(verbatim)
        print("answer of the LLM", answer)
        codes_list = extract_code_response(answer)
        CHARGED_FILE.at[index, "Analysis"] = answer

        for i in range(max_columns):
            if i < len(codes_list):
                try:
                    code_as_int = int(codes_list[i])
                    CHARGED_FILE.at[index, f"review_{i+1}"] = code_as_int
                except ValueError: 
                    print(f"Warning: could not convert {codes_list[i]} to an integer")
            else: 
                CHARGED_FILE.at[index, f"review_{i+1}"]  = np.nan

    output_file = "Prompts/Outputs/new.csv"
    CHARGED_FILE.to_csv(output_file, index=False, sep=";")
    print(f"Updated CSV saved to: {output_file}")

def extract_code_response(model_reply):
    match = re.search(r"Expected_Answer\s*:\s*(\[[^\]]*])", model_reply)
    if match:
        response_str = match.group(1)
        print("response_str in first part", response_str)
        return eval(match.group(1))
    
    match = re.search(r"\[[^\]]*]", model_reply)
    if match:
        print("response_str in other part", match.group(0))
        return eval(match.group(0))
    return []

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
        return data["choices"][0]["text"]
    else: 
        print(f"Erreur {response.status_code}: {response.text}")

process_verbatims_and_extract_csv()

    

