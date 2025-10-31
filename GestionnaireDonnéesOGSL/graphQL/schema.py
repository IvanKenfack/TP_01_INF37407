from graphene_django import DjangoObjectType
from catalogueDonnées.models import Jeu_De_Donnee, Ressource, Mot_Cle, Organisation, Group
import graphene

class JeuDeDonneeType(DjangoObjectType):
    class Meta:
        model = Jeu_De_Donnee
        fields = '__all__'

class RessourceType(DjangoObjectType):
    class Meta:
        model = Ressource
        fields = '__all__'

class MotCleType(DjangoObjectType):
    class Meta:
        model = Mot_Cle
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
    jeuDeDonneeById = graphene.Field(JeuDeDonneeType, id=graphene.Int(required=True))

    def resolve_all_jeux_de_donnees(root, info):
        return Jeu_De_Donnee.objects.select_related('organisation').prefetch_related(
            'ressource_set', 'mot_cle_set', 'group_set'
        ).all()

    def resolve_all_ressources(root, info):
        return Ressource.objects.all()

    def resolve_all_mots_clés(root, info):
        return Mot_Cle.objects.all()

    def resolve_all_organisations(root, info):
        return Organisation.objects.all()

    def resolve_all_groups(root, info):
        return Group.objects.all()
    
    def resolve_jeuDeDonneeById(root, info, id):
        try:
            return Jeu_De_Donnee.objects.select_related('organisation').prefetch_related(
                'ressource_set', 'mot_cle_set', 'group_set'
            ).get(pk=id)
        except Jeu_De_Donnee.DoesNotExist:
            return None
    
schema = graphene.Schema(query=Query)