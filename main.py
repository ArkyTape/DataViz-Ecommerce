import requests
import pandas as pd
import time
from colorama import init, Fore

# Initialisation de colorama
init(autoreset=True)

# Fonction pour afficher un message animé coloré
def afficher_message(message, couleur=Fore.CYAN, delay=0.02):
    for char in message:
        print(couleur + char, flush=True, end='')
        time.sleep(delay)
    print()

def Extract(url, Fore):
    try:
        with open("api.txt") as file:
            api = file.read().strip()
    except Exception as e:
        afficher_message("La clé API n'a pas pu être récupérée...", Fore.RED)
        afficher_message(str(e), Fore.RED)
        return None

    querystring = {
        "query": "Phone",
        "page": "1",
        "country": "FR",
	"sort_by": "RELEVANCE",
        "product_condition": "ALL",
        "is_prime": "false",
        "deals_and_discounts": "NONE"
    }

    headers = {
        "x-rapidapi-key": api,
        "x-rapidapi-host": "real-time-amazon-data.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
    except Exception as e:
        afficher_message("Connexion vers le serveur échouée...", Fore.RED)
        afficher_message(str(e), Fore.RED)
        return None

    afficher_message("Récupération des données depuis l'API Amazon OK !", Fore.GREEN)
    return response


def Transform(response, Fore):
    if response is None:
        return None

    data = response.json()
    products = data.get('data', {}).get('products', [])

    if not products:
        afficher_message("Aucun produit trouvé dans la réponse.", Fore.YELLOW)
        return None

    df = pd.DataFrame(products)

    colonnes = ["title", "price", "product_url", "asin", "is_prime", "rating", "reviews_count"]
    df_mod = df[colonnes] if all(col in df.columns for col in colonnes) else df
    afficher_message("Transformation des données OK !", Fore.GREEN)
    return df_mod


def Load(df_arg, Fore):
    if df_arg is None:
        afficher_message("Aucune donnée à sauvegarder.", Fore.YELLOW)
        return
    df_arg.to_csv('amazon_fr_phones.csv', index=False)
    afficher_message("Chargement des données OK dans le fichier CSV !", Fore.GREEN)


def main(url):
    data = Extract(url, Fore)
    data_frame = Transform(data, Fore)
    Load(data_frame, Fore)

if __name__ == "__main__":
    afficher_message("Démarrage du script de récupération des produits Amazon France...", Fore.GREEN)
    url = "https://real-time-amazon-data.p.rapidapi.com/search"
    main(url)
    afficher_message("Fin du programme...", Fore.GREEN)
