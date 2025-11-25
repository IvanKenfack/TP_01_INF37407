from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path
from .models import Jeu_De_Donnee, Ressource, Mot_Cle, Organisation, Group, ConfigMoisson, LogMoissonage
from django.contrib import messages
from services.core import stockageJeuDeDonnée
import threading

class Jeu_De_DonnéeAdmin(admin.ModelAdmin):
    list_display = ('nom','auteur','date_creation','nombre_ressources','nombre_mots_cles','email_auteur','url_licence','organisation')
    list_editable = ('auteur','nombre_mots_cles','email_auteur','url_licence',)
    list_per_page = 10



class RessourceAdmin(admin.ModelAdmin):
    list_display = ('nom','description','format_ressource','type_ressource','url','taille_ressource','date_creation','derniere_modification','jeu_de_donnee')
    list_editable = ('description','format_ressource','type_ressource','url','taille_ressource',)
    list_per_page = 10

class Mot_CléAdmin(admin.ModelAdmin):
    list_display = ('mot_cle','nom_dAffichage','etat','jeu_de_donnee')
    list_editable = ('nom_dAffichage','etat',)
    list_per_page = 10

class OrganisationAdmin(admin.ModelAdmin):
    list_display = ('nom','titre','statut_dApprobation','etat')
    list_editable = ('titre','statut_dApprobation','etat',)
    list_per_page = 10


class GroupAdmin(admin.ModelAdmin):
    list_display = ('nom','titre','description','jeu_de_donnee')
    list_editable = ('titre','description',)
    list_per_page = 10

class ConfigMoissonAdmin(admin.ModelAdmin):
    list_display = ('nom','source','filtres','dernier_lancement','creation',)
    list_editable = ( 'source','filtres',)
    list_per_page = 10
    actions = ['lancer_moisson']

    change_form_template = "admin/config_moisson_changeform.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<path:object_id>/lancer_vue_moisson/',
                self.admin_site.admin_view(self.lancer_vue_moisson),
                name= 'lancer_vue_moisson', 
            ),
        ]
        return custom_urls + urls
    
    def lancer_vue_moisson(self, request, object_id):
       
        # Vue pour executer le moissonage depuis l'admin
        config = ConfigMoisson.objects.get(idConfigMoisson = object_id)
        self.message_user(request, f"Moissonage lancer pour {config.nom}", messages.SUCCESS)

        #Je lance le script dans un thread pour ne pas bloquer l'interface admin
        thread = threading.Thread(target = stockageJeuDeDonnée, args = (config,))
        thread.start()
        thread.join()

        self.message_user(request, f"Moissonage terminé pour {config.nom}", messages.SUCCESS)

        return HttpResponseRedirect(f"../../{object_id}/")
    
    def lancer_moisson(self, request,queryset):
       
        #Action pour executer le moissonage sur plusieurs configurations
        for config in queryset:
            stockageJeuDeDonnée(config)
        self.message_user(
            request,
            f"Moissonnage lancé pour {queryset.count()} configuration(s)",
            messages.SUCCESS
        )

    
    
class LogMoissonageAdmin(admin.ModelAdmin):
    list_display = ('configuration','commence','complete','statut','records_harvested')
    list_editable = ('configuration','commence','complete')
    list_per_page = 10
    readonly_fields = ('commence','complete','statut','records_harvested')

    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj = ...):
        return False
    
    


admin.site.register(Jeu_De_Donnee, Jeu_De_DonnéeAdmin)
admin.site.register(Ressource, RessourceAdmin)
admin.site.register(Mot_Cle, Mot_CléAdmin)
admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(Group, GroupAdmin) 
admin.site.register(ConfigMoisson, ConfigMoissonAdmin)
admin.site.register(LogMoissonage)