import requests

"""
L'URL est l'url de notre API. En lançant l'interface, nous avions 2 URL, l'une pour l'API
L'autre pour le front. Dans la documentation de Text Generation WebUI, 
la convention veut que l'on ajoute /v1/completions à la suite de l'url qui nous est fourni
"""
API_URL = "http://127.0.0.1:5000/v1/completions"

"""
On définit une fonction qui va tester la connexion API
"""
def test_connexion_script_and_model():
    prompt = "What is the Ultimate Answer to Life, The Universe, and Everything"
    """
    la variable payload indique deux choses : 
    1/ le maximum de token de la réponse, ici 100 mots
    2/ la température, le degré de créativité de la réponse, de 0 à 1
    0 signifiant : une réponse peu créative
    1 signifiant : un maximum de créativité dans la réponse
    """
    payload = {
        "prompt": prompt,
        "max_tokens": 500,
        "temperature": 0.1,
    }

    """
    C'est ici qu'on réalise la requête
    SI elle réussit, on retourne le résultat et on imprime le résultat dans la console
    Si elle échoue, on aura le message d'erreur pour comprendre où ça a planté
    """
    response = requests.post(API_URL, json=payload)

    if response.status_code == 200:
        data = response.json()
        print("Answer", data["choices"][0]["text"])
        return data["choices"][0]["text"]
    else: 
        print(f"Erreur {response.status_code}: {response.text}")


""" On execute la fonction qui fait notre appel API
"""
test_connexion_script_and_model()

    

