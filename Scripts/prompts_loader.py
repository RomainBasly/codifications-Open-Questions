import os

"""
On va aller chercher le fichier dans le dossier parallèle au nôtre (Prompts)
"""
SCRIPT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
PARENT_DIRECTORY = os.path.dirname(SCRIPT_DIRECTORY)
PROMPTS_DIRECTORY = os.path.join(PARENT_DIRECTORY, "Prompts")
print("Prompt_dir", PROMPTS_DIRECTORY)

def load(name_file):
    text_file = os.path.join(PROMPTS_DIRECTORY, f"{name_file}.txt")
    print(f"Trying to open: {text_file}")
    if os.path.exists(text_file):
        with open(text_file, "r", encoding="utf-8") as file:
            return file.read()
        
    raise FileNotFoundError(f"Prompt '{name_file}' introuvable ")