from rest_framework import serializers
from catalogueDonnées.models import Jeu_De_Donnée, Ressource, Mot_Clé, Organisation, Group

class RessourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ressource
        fields = '__all__'

class MotCléSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mot_Clé
        fields = '__all__'

class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class JeuDeDonnéeSerializer(serializers.ModelSerializer):

    organisation = OrganisationSerializer()
    ressources = RessourceSerializer(many=True, source='ressource_set')
    mot_clés = MotCléSerializer(many=True, source='mot_clé_set')
    groups = GroupSerializer(many=True, source='group_set')
    class Meta:
        model = Jeu_De_Donnée
        fields = (
            'idJeuDeDonnée',
            'organisation',
            'nom',
            'auteur',
            'date_création_métadonnées',
            'date_création',
            'nombre_ressources',
            'nombre_mots_clés',
            'email_auteur',
            'url_licence',
            'ressources',
            'mot_clés',
            'groups',
        )

