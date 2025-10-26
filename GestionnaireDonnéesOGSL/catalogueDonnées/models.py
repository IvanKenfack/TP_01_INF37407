from django.db import models

#Tout les champs des tables en dehors des clés primaires sont nullable et peuvent être laissés vides pour accommoder les données incomplètes provenant des jeux de données moissonnés.

class Jeu_De_Donnée(models.Model):

    idJeuDeDonnée = models.AutoField(primary_key=True)
    organisation = models.ForeignKey('Organisation', on_delete=models.CASCADE)
    auteur = models.CharField(max_length=100, blank=True)
    date_création = models.DateTimeField(6,null=True, blank=True)
    email_auteur = models.CharField(max_length=100, blank=True)
    url_licence = models.CharField(max_length=200,blank=True)
    date_création_métadonnées = models.DateTimeField(6,null=True,blank=True)
    nom = models.CharField(max_length=200,blank=True)
    nombre_ressources = models.IntegerField(null=True,blank=True)
    nombre_mots_clés = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return self.nom 


class Ressource(models.Model):
    
    idRessource = models.AutoField(primary_key=True)
    jeu_de_donnée = models.ForeignKey('Jeu_De_Donnée', on_delete=models.CASCADE)
    date_création = models.DateTimeField(6,null=True, blank=True)
    description = models.TextField(2000,blank=True)
    format_ressource = models.CharField(max_length=50,blank=True)
    dernière_modification = models.DateTimeField(6,null=True, blank=True)
    nom = models.CharField(max_length=200,blank=True)
    type_ressource = models.CharField(max_length=100,blank=True)
    url  = models.CharField(max_length=200,blank=True)
    taille_ressource = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return self.nom
    

class Mot_Clé(models.Model):

    idMotClé = models.AutoField(primary_key=True)
    jeu_de_donnée = models.ForeignKey('Jeu_De_Donnée', on_delete=models.CASCADE)
    nom_dAffichage = models.CharField(max_length=100,blank=True)
    mot_clé = models.CharField(max_length=100,blank=True)
    état = models.CharField(max_length=45,blank=True)

    def __str__(self):
        return self.mot_clé
    

class Organisation(models.Model):

    idOrganisation = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=200,blank=True)
    titre = models.CharField(max_length=100,blank=True)
    statut_dApprobation = models.CharField(max_length=45,blank=True)
    état = models.CharField(max_length=45,blank=True)
   
    def __str__(self):
        return self.nom
    

class Group(models.Model):

    idGroupe = models.AutoField(primary_key=True)
    jeu_de_donnée = models.ForeignKey('Jeu_De_Donnée', on_delete=models.CASCADE)
    description = models.TextField(500,blank=True)
    nom = models.CharField(max_length=100,blank=True)
    titre = models.CharField(max_length=100,blank=True)

    def __str__(self):
        return self.nom