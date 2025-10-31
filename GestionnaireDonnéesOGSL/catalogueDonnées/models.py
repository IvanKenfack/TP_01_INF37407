from django.db import models

#Tout les champs des tables en dehors des clés primaires sont nullable et peuvent être laissés vides pour accommoder les données incomplètes provenant des jeux de données moissonnés.

class Jeu_De_Donnee(models.Model):

    idJeuDeDonnee = models.AutoField(verbose_name='idJeuDeDonnée',primary_key=True)
    organisation = models.ForeignKey('Organisation', on_delete=models.CASCADE)
    auteur = models.CharField(max_length=500, null=True,blank=True)
    date_creation = models.DateTimeField(verbose_name='date de création',null=True, blank=True)
    email_auteur = models.CharField(max_length=500, blank=True,null=True,)
    url_licence = models.CharField(max_length=500,blank=True,null=True,)
    date_creation_metadonnees = models.DateTimeField(verbose_name='date de création des métadonnées',null=True,blank=True)
    nom = models.CharField(max_length=500,blank=True,null=True,)
    nombre_ressources = models.IntegerField(null=True,blank=True)
    nombre_mots_cles = models.IntegerField(verbose_name='nombre de mots clés',null=True,blank=True)

    def __str__(self):
        return self.nom 
    
    class Meta:
        db_table = 'jeu_de_donnee'
        verbose_name = 'Jeu De Donnée'
        verbose_name_plural = 'Jeux De Données'



class Ressource(models.Model):
    
    idRessource = models.AutoField(primary_key=True)
    jeu_de_donnee = models.ForeignKey('Jeu_De_Donnee', on_delete=models.CASCADE,verbose_name='jeu de donnée')
    date_creation = models.DateTimeField(verbose_name='date de création',null=True, blank=True)
    description = models.TextField(2000,blank=True,null=True,)
    format_ressource = models.CharField(max_length=50,blank=True)
    derniere_modification = models.DateTimeField(verbose_name='date de dernière modification',null=True, blank=True)
    nom = models.CharField(max_length=500,blank=True,null=True,)
    type_ressource = models.CharField(max_length=100,blank=True,null=True,)
    url  = models.CharField(max_length=500,blank=True,null=True,)
    taille_ressource = models.IntegerField(null=True,blank=True)
    
    def __str__(self):
        return self.nom
    

class Mot_Cle(models.Model):

    idMotCle = models.AutoField(verbose_name='idMotClé',primary_key=True)
    jeu_de_donnee = models.ForeignKey('Jeu_De_Donnee', on_delete=models.CASCADE,verbose_name='jeu de donnée')
    nom_dAffichage = models.CharField(max_length=100,blank=True,null=True,)
    mot_cle = models.CharField('mot-clé',max_length=100,blank=True,null=True,)
    etat = models.CharField('état',max_length=45,blank=True,null=True,)

    def __str__(self):
        return self.mot_clé
    
    class Meta:
        db_table = 'mot_cle'
        verbose_name = 'Mot-Clé'
        verbose_name_plural = 'Mots-Clés'
    

class Organisation(models.Model):

    idOrganisation = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=500,blank=True,null=True,)
    titre = models.CharField(max_length=500,blank=True,null=True,)
    statut_dApprobation = models.CharField(max_length=45,blank=True,null=True,)
    etat = models.CharField('état',max_length=45,blank=True,null=True,)
   
    def __str__(self):
        return self.nom
    
    class Meta:
        db_table = 'organisation'
        verbose_name = 'Organisation'
        verbose_name_plural = 'Organisations'
    

class Group(models.Model):

    idGroupe = models.AutoField(primary_key=True)
    jeu_de_donnee = models.ForeignKey('Jeu_De_Donnee', on_delete=models.CASCADE)
    description = models.TextField(1000,blank=True,null=True,)
    nom = models.CharField(max_length=500,blank=True,null=True,)
    titre = models.CharField(max_length=500,blank=True,null=True,)

    def __str__(self):
        return self.nom
    
    class Meta:
        db_table = 'group'
        verbose_name = 'Groupe'
        verbose_name_plural = 'Groupes'


class ConfigMoisson(models.Model):
    sourceAPI = (

        ("DonneesQuebec","https://www.donneesquebec.ca/recherche/api/3/action/package_search"),
        ("CanWIN","https://canwin-datahub.ad.umanitoba.ca/data/api/3/action/package_search"),
        ("OpenGouv","https://open.canada.ca/data/api/action/package_search"),
        ("Borealis" , "https://borealisdata.ca/api/search"),

    )

    idConfigMoisson = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=200)
    source = models.CharField(max_length=500,choices=sourceAPI)
    filtres = models.CharField(max_length=300,blank=True)
    creation = models.DateTimeField(auto_now_add=True)
    dernier_lancement = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nom} - {self.source}"
    
    class Meta:
        db_table = 'config_moisson'
        verbose_name = 'Configuration de Moissonnage'
        verbose_name_plural = 'Configurations de Moissonnage'