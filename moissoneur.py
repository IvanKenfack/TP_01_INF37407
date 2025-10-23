
import requests

def fetch_ckan_metadata(base_url, filters=None):
    """
    Récupère les métadonnées depuis une instance CKAN via l'API.
    :param base_url: URL de base de l'instance CKAN (ex: https://donneesquebec.ca)
    :param filters: dictionnaire de filtres (tags, groupes, etc.)
    :return: liste de jeux de données normalisés
    """
    package_list_url = f"{base_url}/api/3/action/package_list"
    response = requests.get(package_list_url)
    datasets = response.json().get("result", [])

    metadata_list = []
    for dataset_id in datasets:
        show_url = f"{base_url}/api/3/action/package_show?id={dataset_id}"
        data = requests.get(show_url).json().get("result", {})
        if filters:
            if not any(tag["name"] in filters.get("tags", []) for tag in data.get("tags", [])):
                continue
        metadata_list.append(normalize_metadata(data, base_url))

    return metadata_list