from rest_framework.views import APIView, status, Response
from catalogueDonnées.models import Jeu_De_Donnée, Ressource, Mot_Clé, Organisation, Group
from .serializers import JeuDeDonnéeSerializer, RessourceSerializer, MotCléSerializer, OrganisationSerializer, GroupSerializer
from drf_yasg.utils import swagger_auto_schema



class JeuDeDonnéeListAPIView(APIView):
    @swagger_auto_schema(responses={200: JeuDeDonnéeSerializer(many=True)})
    def get(self, request):
        # précharger l'organisation (FK) et préfetcher les relations "reverse" vers Ressource, Mot_Clé et Group
        jeux_de_données = Jeu_De_Donnée.objects.select_related('organisation').prefetch_related(
            'ressource_set', 'mot_clé_set', 'group_set'
        ).all()

        serializer = JeuDeDonnéeSerializer(jeux_de_données, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class JeuDeDonnéeDetailAPIView(APIView):
    @swagger_auto_schema(responses={200: JeuDeDonnéeSerializer()})
    def get(self, request, Id):
        try:
            jeu_de_donnée = Jeu_De_Donnée.objects.select_related('organisation').prefetch_related(
                'ressource_set', 'mot_clé_set', 'group_set'
            ).get(pk=Id)

        except Jeu_De_Donnée.DoesNotExist:
            return Response({"error": "Jeu de donnée non trouvé."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = JeuDeDonnéeSerializer(jeu_de_donnée)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = JeuDeDonnéeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RessourceListAPIView(APIView):
    def get(self, request):
        ressources = Ressource.objects.all()
        serializer = RessourceSerializer(ressources, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class RessourceDetailAPIView(APIView):
    def get(self, request, Id):
        try:
            ressource = Ressource.objects.get(pk=Id)
        except Ressource.DoesNotExist:
            return Response({"error": "Ressource non trouvée."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = RessourceSerializer(ressource)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = RessourceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class MotCléListAPIView(APIView):
    def get(self, request):
        mots_clés = Mot_Clé.objects.all()
        serializer = MotCléSerializer(mots_clés, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class MotCléDetailAPIView(APIView):
    def get(self, request, Id):
        try:
            mot_clé = Mot_Clé.objects.get(pk=Id)
        except Mot_Clé.DoesNotExist:
            return Response({"error": "Mot clé non trouvé."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = MotCléSerializer(mot_clé)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = MotCléSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class OrganisationListAPIView(APIView):
    def get(self, request):
        organisations = Organisation.objects.all()
        serializer = OrganisationSerializer(organisations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class OrganisationDetailAPIView(APIView):
    def get(self, request, Id):
        try:
            organisation = Organisation.objects.get(pk=Id)
        except Organisation.DoesNotExist:
            return Response({"error": "Organisation non trouvée."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = OrganisationSerializer(organisation)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = OrganisationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GroupListAPIView(APIView):
    def get(self, request):
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class GroupDetailAPIView(APIView):
    def get(self, request, Id):
        try:
            group = Group.objects.get(pk=Id)
        except Group.DoesNotExist:
            return Response({"error": "Groupe non trouvé."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = GroupSerializer(group)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



