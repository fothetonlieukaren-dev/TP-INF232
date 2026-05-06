import requests
import time
import random
from datetime import datetime

# Votre lien Streamlit
URL = "https://votrenom.streamlit.app"

# Liste de produits aléatoires pour simuler de vraies ventes
produits = [
    {"nom": "Coca-Cola 33cl", "prix": 2.0},
    {"nom": "Fanta Orange", "prix": 1.8},
    {"nom": "Sprite Citron", "prix": 1.8},
    {"nom": "Chips Nature", "prix": 1.5},
    {"nom": "Chips Barbecue", "prix": 1.5},
    {"nom": "Bonbons Haribo", "prix": 1.0},
    {"nom": "Chocolat Milka", "prix": 2.5},
    {"nom": "Bouteille Eau 1L", "prix": 0.8},
    {"nom": "Sandwich Poulet", "prix": 3.5},
    {"nom": "Salade César", "prix": 4.0},
]

compteur = 0

while True:
    compteur += 1
    
    try:
        # Visite la page d'accueil (réveille l'app)
        requests.get(URL)
        
        # Simule un clic sur l'analyse (interaction réelle)
        requests.get(URL + "/?analyse=true")
        
        print(f"✅ [{compteur}] Page visitée - {datetime.now().strftime('%H:%M:%S')}")
        
    except Exception as e:
        print(f"❌ [{compteur}] Erreur : {e}")
    
    # Attendre 30 minutes
    print(f"⏳ Prochaine visite dans 30 minutes...")
    time.sleep(1800)
