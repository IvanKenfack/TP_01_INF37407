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
def moissoneurJeuDeDonnées(source, mot_clé="", nombre_de_jeux=None, max_rows=100, verbose=False):
    """
    Récupère les jeux correspondant à mot_clé depuis l'API CKAN (package_search).
    - nombre_de_jeux=None -> récupère tous les résultats disponibles (jusqu'à épuisement de la pagination)
    - max_rows limite le nombre d'items par requête (CKAN accepte typiquement >=100)
    - verbose affiche les URLs de requête
    """
    résultats = []
    start = 0
    # s'assurer que rows est un entier raisonnable
    rows = max(1, int(max_rows))

    while True:
        # si un nombre de jeux est demandé, ajuster rows pour ne pas surcharger
        if nombre_de_jeux:
            rows = min(rows, max(1, nombre_de_jeux - len(résultats)))

        params = {"q": mot_clé, "rows": rows, "start": start}
        try:
            r = requests.get(source, params=params, timeout=15)
        except requests.exceptions.RequestException as e:
            print(f"Erreur réseau: {e}")
            break

        if verbose:
            print(f"Requête: {r.url}")

        if r.status_code != 200:
            print(f"La requête a échoué avec le code: {r.status_code}")
            break

        try:
            données = r.json()
        except ValueError:
            print("Réponse non JSON reçue")
            break

        page = données.get("result", {}).get("results", [])
        if not page:
            # plus de résultats
            break

        résultats.extend(page)
        start += len(page)

        # si on a récupéré le nombre demandé, ou si la page est incomplète -> fin
        if nombre_de_jeux and len(résultats) >= nombre_de_jeux:
            break
        if len(page) < rows:
            break

    return résultats if nombre_de_jeux is None else résultats[:nombre_de_jeux]


jeuDeDonnées = moissoneurJeuDeDonnées(
    source="https://www.donneesquebec.ca/recherche/api/3/action/package_search",
    mot_clé="fleuve Saint-Laurent",
    nombre_de_jeux=5
)   

for jeuDeDonnée in jeuDeDonnées:
    print(f"Title: {jeuDeDonnée['title']}")
    print(f"Description: {jeuDeDonnée['notes']}")
    print(f"URL: https://www.donneesquebec.ca/recherche/dataset/{jeuDeDonnée['name']}")
    print("-" * 50)


def stockageJeuDeDonnée(jeuDeDonnée):
    # Fonction pour stocker un jeu de données dans la base de données Django
    # À implémenter: création des instances de Jeu_De_Donnée, Ressource, Mot_Clé, Organisation
    
    pass