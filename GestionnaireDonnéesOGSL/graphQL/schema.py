from graphene_django import DjangoObjectType
from catalogueDonnées.models import Jeu_De_Donnée, Ressource, Mot_Clé, Organisation, Group
import graphene

class JeuDeDonneeType(DjangoObjectType):
    class Meta:
        model = Jeu_De_Donnée
        fields = '__all__'

class RessourceType(DjangoObjectType):
    class Meta:
        model = Ressource
        fields = '__all__'

class MotCleType(DjangoObjectType):
    class Meta:
        model = Mot_Clé
        fields = '__all__'

class OrganisationType(DjangoObjectType):
    class Meta:
        model = Organisation
        fields = '__all__'

class GroupType(DjangoObjectType):
    class Meta:
        model = Group
        fields = '__all__'


class Query(graphene.ObjectType):
    all_jeux_de_donnees = graphene.List(JeuDeDonneeType)
    all_ressources = graphene.List(RessourceType)
    all_mots_cles = graphene.List(MotCleType)
    all_organisations = graphene.List(OrganisationType)
    all_groups = graphene.List(GroupType)

    def resolve_all_jeux_de_donnees(root, info):
        return Jeu_De_Donnée.objects.select_related('organisation').prefetch_related(
            'ressource_set', 'mot_cle_set', 'group_set'
        ).all()

    def resolve_all_ressources(root, info):
        return Ressource.objects.all()

    def resolve_all_mots_clés(root, info):
        return Mot_Clé.objects.all()

    def resolve_all_organisations(root, info):
        return Organisation.objects.all()

    def resolve_all_groups(root, info):
        return Group.objects.all()
    
schema = graphene.Schema(query=Query)