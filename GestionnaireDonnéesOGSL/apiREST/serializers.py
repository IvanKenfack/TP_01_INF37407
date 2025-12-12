from rest_framework import serializers
from catalogueDonnées.models import Jeu_De_Donnee, Ressource, Mot_Cle, Organisation, Group
from django.contrib.auth.models import User, Permission, Group as AuthGroup


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



class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'

class GroupAuthSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = AuthGroup
        fields = '__all__'  

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,required=True)
    last_login = serializers.DateTimeField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=False)
    user_permissions = PermissionSerializer(many=True, read_only=True)
    groups = GroupAuthSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data.get('last_name', ''),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def update(self, instance, validated_data):
        email_changed = instance.email != validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance
    
