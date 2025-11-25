import os,sys, django
from datetime import datetime
from django.utils import timezone

# ajout du répertoire parent au PYTHONPATH pour que "GestionnaireDonnéesOGSL.settings" soit trouvable
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Configuration de l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GestionnaireDonnéesOGSL.settings')
django.setup()

# Importation des modèles Django après la configuration de Django pour éviter les erreurs d'importation
from catalogueDonnées.models import ConfigMoisson

from services.core import stockageJeuDeDonnée


config = ConfigMoisson.objects.first()

stockageJeuDeDonnée(config)

