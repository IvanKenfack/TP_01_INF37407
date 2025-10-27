import requests

# Fonction pour moissonner des jeux de données à partir d'une API donnée
def moissoneurJeuDeDonnées(source, mot_clé="", nombre_de_jeux=10):

    # Effectuer une requête GET à l'API avec le mot clé
    r = requests.get(source, params={"q": mot_clé})
    print()
    print(f"Requête effectuée à l'URL: {r.url}")
    print()
    print(r.text)
    print()
    
    #si la requête reussie, on parse les données
    if r.status_code == 200:
        données = r.json()
        # Retourner la liste des jeux de données
        return données.get("result", {}).get("results", [])
    
    else:
        print(f"La requette a échoué avec le code d'érreur:\n {r.status_code}") 
        return []


datasets = moissoneurJeuDeDonnées(
    source="https://www.donneesquebec.ca/recherche/api/3/action/package_search",
    mot_clé="fleuve Saint-Laurent",
    nombre_de_jeux=5
)

for ds in datasets:
    print(f"Title: {ds['title']}")
    print(f"Description: {ds['notes']}")
    print(f"URL: https://www.donneesquebec.ca/recherche/dataset/{ds['name']}")
    print("-" * 50)
