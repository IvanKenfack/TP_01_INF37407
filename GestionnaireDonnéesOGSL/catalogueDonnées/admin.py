from django.contrib import admin
from .models import Jeu_De_Donnée, Ressource, Mot_Clé, Organisation, Group, ConfigMoisson


class Jeu_De_DonnéeAdmin(admin.ModelAdmin):
    list_display = ('nom','auteur','date_création','nombre_ressources','nombre_mots_clés','email_auteur','url_licence','organisation')
    list_editable = ('auteur','nombre_mots_clés','email_auteur','url_licence',)
    list_per_page = 10



class RessourceAdmin(admin.ModelAdmin):
    list_display = ('nom','description','format_ressource','type_ressource','url','taille_ressource','date_création','dernière_modification','jeu_de_donnée')
    list_editable = ('description','format_ressource','type_ressource','url','taille_ressource',)
    list_per_page = 10

class Mot_CléAdmin(admin.ModelAdmin):
    list_display = ('mot_clé','nom_dAffichage','état','jeu_de_donnée')
    list_editable = ('nom_dAffichage','état',)
    list_per_page = 10

class OrganisationAdmin(admin.ModelAdmin):
    list_display = ('nom','titre','statut_dApprobation','état')
    list_editable = ('titre','statut_dApprobation','état',)
    list_per_page = 10


class GroupAdmin(admin.ModelAdmin):
    list_display = ('nom','titre','description','jeu_de_donnée')
    list_editable = ('titre','description',)
    list_per_page = 10

class ConfigMoissonAdmin(admin.ModelAdmin):
    list_display = ('nom','source','filtres','dernier_lancement','creation',)
    list_editable = ( 'source','filtres',)
    list_per_page = 10
    actions = ['lancer_moisson']

    def lancer_moisson(self, request, queryset):
        for config in queryset:
            management.call_command('moissonner', str(config.id))
        self.message_user(request, "Moissonnage lancé pour les configurations sélectionnées.")

admin.site.register(Jeu_De_Donnée, Jeu_De_DonnéeAdmin)
admin.site.register(Ressource, RessourceAdmin)
admin.site.register(Mot_Clé, Mot_CléAdmin)
admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(Group, GroupAdmin) 
admin.site.register(ConfigMoisson, ConfigMoissonAdmin)
