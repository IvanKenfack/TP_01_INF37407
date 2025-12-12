
from rest_framework.views import APIView, status, Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.authentication import TokenAuthentication
from catalogueDonnées.models import Jeu_De_Donnee, Ressource, Mot_Cle, Organisation, Group
from .serializers import JeuDeDonnéeSerializer, RessourceSerializer, MotCléSerializer, OrganisationSerializer, GroupSerializer, UserSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import login, logout
from rest_framework_simplejwt.tokens import RefreshToken, Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets




class JeuDeDonnéeListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Jeu_De_Donnee.objects.select_related('organisation').prefetch_related(
        'ressource_set', 'mot_cle_set', 'group_set')
    serializer_class = JeuDeDonnéeSerializer
    pagination_class = LimitOffsetPagination
    authentication_classes = [TokenAuthentication,]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {
        'organisation__nom' : ['exact'],
        'auteur' : ['exact', 'icontains'],
        'date_creation_metadonnees' : ['gte', 'lte'],
        'nombre_ressources' : ['gte', 'lte'],
    }
        
    search_fields = ['nom', 'auteur', 'organisation__nom']


    

class JeuDeDonnéeDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(responses={200: JeuDeDonnéeSerializer()})
    def get(self, request, Id):
        try:
            jeu_de_donnée = Jeu_De_Donnee.objects.distinct.select_related('organisation').prefetch_related(
                'ressource_set', 'mot_cle_set', 'group_set'
            ).get(pk=Id)

        except Jeu_De_Donnee.DoesNotExist:
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
    permission_classes = [AllowAny]
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
    
class MotCléListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Mot_Cle.objects.distinct()
    serializer_class = MotCléSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {
        'mot_cle' : ['exact'],
        'jeu_de_donnee__nom' : ['exact', 'icontains'],
    }
    search_fields = ['mot_cle', 'nom_dAffichage']
    
class MotCléDetailAPIView(APIView):
    def get(self, request, Id):
        try:
            mot_clé = Mot_Cle.objects.get(pk=Id)
        except Mot_Cle.DoesNotExist:
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


class UserInscriptionAPIView(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(request_body=UserSerializer, responses={201: UserSerializer()})

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            Token.objects.create(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request,Id):
        user = User.objects.get(pk=Id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK) 
    
class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Identifiants invalides.'}, status=status.HTTP_401_UNAUTHORIZED)
        

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        logout(request)
        #Logique de redirection

        return Response({'message': 'Déconnexion réussie.'}, status=status.HTTP_200_OK)
    

class ProfileManagementAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JeuDeDonneeInfoViewset(viewsets.ViewSet):
    permission_classes = [AllowAny]
    def list(self, request):
        queryset = Jeu_De_Donnee.objects.all()
        serializer = JeuDeDonnéeSerializer(queryset, many=True)
        return Response(serializer.data)