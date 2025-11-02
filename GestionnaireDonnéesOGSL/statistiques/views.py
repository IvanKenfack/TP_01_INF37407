from django.shortcuts import render
from django.db.models import Count
from catalogueDonnées.models import Jeu_De_Donnee, Group
import json

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