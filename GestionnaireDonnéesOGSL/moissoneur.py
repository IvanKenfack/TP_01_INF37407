import requests, os,sys, django

# ajout du répertoire parent au PYTHONPATH pour que "GestionnaireDonnéesOGSL.settings" soit trouvable
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Configuration de l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GestionnaireDonnéesOGSL.settings')
django.setup()

# Importation des modèles Django
from catalogueDonnées.models import Jeu_De_Donnée, Ressource, Mot_Clé, Organisation, Group


# Fonction pour moissonner des jeux de données à partir d'une API donnée
def moissoneurJeuDeDonnées(source, mot_clé="", nombre_de_jeux=None,afficherRequette=True):

    résultats = []

    # Le décalage dans le résultat complet à partir duquel l’ensemble des ensembles de données retournés doit commencer.
    start = 0
    
    # Le paramètre rows dans CKAN détermine le nombre d'items par page(données renvoyées par requête)
    rows = 100

    while True:

        # Construction des paramètres de la requête
        
        if source == "https://borealisdata.ca/api/search":
            params = {"q": mot_clé, "type": "dataset", "rows": rows, "start": start}

        else:
            params = {"q": mot_clé, "rows": rows, "start": start}

        try:
            r = requests.get(source, params=params, timeout=15)
            print()
        except requests.exceptions.RequestException as e:
            print(f"Erreur réseau: {e}")
            break

        if afficherRequette:
            print()
            print(f"Requête: {r.url}")
            print()

        if r.status_code != 200:
            print(f"La requête a échoué avec le code: {r.status_code}")
            break

        try:
            données = r.json()
        except ValueError:
            print("Réponse non JSON reçue")
            break

        #Si la source est Borealis, les résultats sont dans une structure différente
        if source == "https://borealisdata.ca/api/search":
            page = données.get("data", {}).get("items", [])
        else:
            page = données.get("result", {}).get("results", [])

        if not page:
            # plus de résultats
            break
        
        # Ajout des résultats de la page courante
        résultats.extend(page)
        print(f"Récupéré {len(résultats)} jeux de données jusqu'à présent.")

        # Mise à jour du décalage pour la prochaine page
        start += len(page)
        print(f"Prochain start: {start}")

        # Si la source est Borealis, le comptage total est différent
        if source == "https://borealisdata.ca/api/search": 
            print(f"Nombre de jeux: {données.get("data", {}).get("total_count")}")
            if len(résultats) >= données.get("data", {}).get("total_count"):
                break

        else:
            print(f"Nombre de jeux: {données.get("result", {}).get("count")}")

             # si on a récupéré le nombre demandé -> fin
            if len(résultats) >= données.get("result", {}).get("count"):
                break


    return résultats


sourceAPI = {
    "DonneesQuebec":"https://www.donneesquebec.ca/recherche/api/3/action/package_search",
    "CanWIN":"https://canwin-datahub.ad.umanitoba.ca/data/api/3/action/package_search",
    "OpenGouv":"https://open.canada.ca/data/api/action/package_search",
    "Borealis" : "https://borealisdata.ca/api/search"
}


jeuDeDonnées = moissoneurJeuDeDonnées(
    source=sourceAPI["Borealis"],
    mot_clé="fleuve Saint-Laurent"
)   

"""
for jeuDeDonnée in jeuDeDonnées:
    print(f"name: {jeuDeDonnée['name']}")
    print(f"Description: {jeuDeDonnée['description']}")
    print(f"URL: {jeuDeDonnée['url']}")
    print("-" * 50)
"""

def stockageJeuDeDonnée(jeuDeDonnée):
    # Fonction pour stocker un jeu de données dans la base de données Django
    # À implémenter: création des instances de Jeu_De_Donnée, Ressource, Mot_Clé, Organisation
    
    pass