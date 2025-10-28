import requests, os,sys, django

# ajout du répertoire parent au PYTHONPATH pour que "GestionnaireDonnéesOGSL.settings" soit trouvable
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Configuration de l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GestionnaireDonnéesOGSL.settings')
django.setup()

# Importation des modèles Django après la configuration de Django pour éviter les erreurs d'importation
from catalogueDonnées.models import Jeu_De_Donnée, Ressource, Mot_Clé, Organisation, Group
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware,is_naive



sourceAPI = {
    "DonneesQuebec":"https://www.donneesquebec.ca/recherche/api/3/action/package_search",
    "CanWIN":"https://canwin-datahub.ad.umanitoba.ca/data/api/3/action/package_search",
    "OpenGouv":"https://open.canada.ca/data/api/action/package_search",
    "Borealis" : "https://borealisdata.ca/api/search"
}


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

    print(f"Moissonnage terminé. Total des jeux de données récupérés: {len(résultats)}")
    print()
    print("-" * 80)
    print()
    print()
    return résultats

# Fonction pour parser les dates CKAN en objets datetime de Django
def parsageDateCKAN(dateString):
    if dateString:
        dt = parse_datetime(dateString)
        if dt and is_naive(dt):
            dt = make_aware(dt)
        return dt
    return None



def stockageJeuDeDonnée():

    jeuDeDonnées = moissoneurJeuDeDonnées(
    source=sourceAPI["DonneesQuebec"],
    mot_clé="fleuve Saint-Laurent"
    )

    i = 1
    for jeuDeDonnée in jeuDeDonnées:
        print()
        print()
        print(f"Stockage du Jeu de donnée {i}:")
        print()

        org = Organisation.objects.get_or_create(
            nom=jeuDeDonnée.get("organization", {}).get("name",""),
            titre=jeuDeDonnée.get("organization", {}).get("title",""),
            statut_dApprobation=jeuDeDonnée.get("organization", {}).get("approval_status",""),
            état=jeuDeDonnée.get("organization", {}).get("state",""),
        # [0] pour obtenir l'instance créée uniquement
        )[0]

        j = Jeu_De_Donnée.objects.create(
            organisation=org,
            nom=jeuDeDonnée.get("name",""),
            auteur=jeuDeDonnée.get("author",""),
            date_création_métadonnées=parsageDateCKAN(jeuDeDonnée.get("metadata_created","")),
            date_création=parsageDateCKAN(jeuDeDonnée.get("metadata_created","")),
            nombre_ressources=jeuDeDonnée.get("num_resources",0),
            nombre_mots_clés=jeuDeDonnée.get("num_tags",0),
            email_auteur=jeuDeDonnée.get("author_email",""),
            url_licence=jeuDeDonnée.get("license_url",""),
        )
        ressources_data = jeuDeDonnée.get("resources", [])
        ressources_objs = [
            Ressource(
                jeu_de_donnée=j,
                nom=rdata.get("name",""),
                description=rdata.get("description",""),
                format_ressource=rdata.get("format",""),
                url=rdata.get("url",""),
                taille_ressource=rdata.get("size",0),
                type_ressource=rdata.get("resource_type",""),
                date_création=parsageDateCKAN(rdata.get("created", None)),
                dernière_modification=parsageDateCKAN(rdata.get("last_modified", None)),
            )
            for rdata in ressources_data
        ]

        # Insérer en une ou plusieurs requêtes (batch_size aide pour des très grandes listes)
        if ressources_objs:
            Ressource.objects.bulk_create(ressources_objs, batch_size=100)

        motsClés = jeuDeDonnée.get("tags", [])
        mots_objs = [
            Mot_Clé(
                jeu_de_donnée=j,
                nom_dAffichage=motClé.get("display_name",""),
                mot_clé=motClé.get("name",""),
                état=motClé.get("state",""), 
            ) 
            for motClé in motsClés
        ]
        if mots_objs:
            Mot_Clé.objects.bulk_create(mots_objs, batch_size=100)

        groups = jeuDeDonnée.get("groups", [])
        groups_objs = [
            Group(
                jeu_de_donnée=j,
                nom=group.get("name",""),
                titre=group.get("title",""),
                description=group.get("description",""),
            )
            for group in groups
        ]

        if groups_objs:
            Group.objects.bulk_create(groups_objs, batch_size=100)

        print()
        print(f"Jeu de donnée '{j.nom}' stocké avec {len(ressources_objs)} ressources, {len(mots_objs)} mots-clés et {len(groups_objs)} groupes.")
        print()
        print("-" * 50)
        i+=1
    print()
    print("Stockage terminé pour tous les jeux de données moissonnés.")

    return  

if __name__ == "__main__":
    stockageJeuDeDonnée()
