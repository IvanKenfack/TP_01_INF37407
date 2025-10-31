from rest_framework import serializers
from catalogueDonnées.models import Jeu_De_Donnee, Ressource, Mot_Cle, Organisation, Group

class RessourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ressource
        fields = '__all__'

class MotCléSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mot_Cle
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
    mot_cles = MotCléSerializer(many=True, source='mot_cle_set')
    groups = GroupSerializer(many=True, source='group_set')
    class Meta:
        model = Jeu_De_Donnee
        fields = (
            'idJeuDeDonnee',
            'organisation',
            'nom',
            'auteur',
            'date_creation_metadonnees',
            'date_creation',
            'nombre_ressources',
            'nombre_mots_cles',
            'email_auteur',
            'url_licence',
            'ressources',
            'mot_cles',
            'groups',
        )

