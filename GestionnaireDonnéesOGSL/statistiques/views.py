from django.shortcuts import render
from django.db.models import Count
from catalogueDonnées.models import Jeu_De_Donnee, Group
import json
import requests
from django.http import JsonResponse


def index(request):
    thematiques = Group.objects.values_list('nom', flat=True).distinct()
    thematiques = list(thematiques)

    nombreJeuxParThematique = Group.objects.values('nom').annotate(total = Count('pk'))
    nombreJeuxParThematique = list(nombreJeuxParThematique)

    context = {
        'thematiques' : json.dumps(thematiques),
        'nombreJeuxParThematique': json.dumps(nombreJeuxParThematique)
    }

    return render(request, 'index.html', context)


def canWin(request):
    response = requests.get("https://canwin-datahub.ad.umanitoba.ca/data/api/3/action/package_search?q=fleuve+Saint-Laurent")
    return JsonResponse(response.json())

def DonneeQuebec(request):
    response = requests.get("https://www.donneesquebec.ca/recherche/api/3/action/package_search?q=fleuve+Saint-Laurent")
    return JsonResponse(response.json())

def OpenGouv(request):
    response = requests.get("https://open.canada.ca/data/api/action/package_list?q=fleuve+Saint-Laurent")
    return JsonResponse(response.json())
