#Créer un fichier texte avec vote clé api. plus d'infos sur rapidapi.com
import requests
import pandas
import time
from colorama import init, Fore, Style

# Initialisation de colorama
init(autoreset=True)

# Fonction pour afficher un message avec animation et couleur
def afficher_message(message, couleur=Fore.CYAN, delay=0.02):
    for char in message:
        print(couleur + char,flush=True,end='')
        time.sleep(delay)
    print()  # saut de ligne à la fin



def Extract(url,Fore):
	
	try :
		with open("api.txt") as file:
			api = file.read().strip()
	except Exception as e:
		afficher_message("La clé api n'as pas pu etre récupérer...", Fore.RED)
		afficher_message(e)
		
	querystring = {"referenceCurrencyUuid":"yhjMzLPhuIDl","timePeriod":"24h","tiers":"1","orderBy":"marketCap","orderDirection":"desc","limit":"60","offset":"0"}
	headers = {
		"x-rapidapi-key": api,
		"x-rapidapi-host": "coinranking1.p.rapidapi.com"
	}
	try :
		#Requète pour se connecter au serveur
		response = requests.get(url, headers=headers, params=querystring)
	except Exception as e:
		afficher_message("Connexion vers le serveur echoué...", Fore.RED)
		afficher_message(e)
		
	afficher_message("Récupération des données depuis l'api ok!")
	return response

def Transform(response,Fore):
	#Créer le Dataframe a partir de la réponse json
	data = response.json()
	coins = data['data']['coins']
	df = pandas.DataFrame(coins)

	colonnes = ["symbol","name","marketCap","price"]
	df_mod = df[colonnes]
	afficher_message("Transformation des données Ok!")
	return df_mod
	
def Load(df_arg,Fore):
	#Sauvegarder le résultat dans un fichier csv
	df_arg.to_csv('crypto_coins.csv')
	afficher_message("Chargement des données ok dans le fichier CSV!")

def main(url):
	data = Extract(url,Fore)
	data_frame = Transform(data,Fore)
	Load(data_frame,Fore)
	
if __name__ == "__main__" :
	afficher_message("Démarrage du script de récupération des données cryptomonnaies...", Fore.GREEN)
	url = "https://coinranking1.p.rapidapi.com/coins"
	main(url)
	afficher_message("Fin du programme...", Fore.GREEN)
