from django.urls import path
from rest_framework import permissions
from .views import JeuDeDonnéeListAPIView, RessourceListAPIView, MotCléListAPIView, OrganisationListAPIView, GroupListAPIView, JeuDeDonnéeDetailAPIView, RessourceDetailAPIView, MotCléDetailAPIView, OrganisationDetailAPIView, GroupDetailAPIView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Gestionnaire de Données OGSL API",
      default_version='v1',
      description="API pour gérer les jeux de données, ressources, mots-clés, organisations et groupes.",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="kenfackzeuns@gmail.com"),
      license=openapi.License(name="CC BY 4.0 License"),
    ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('jeux/', JeuDeDonnéeListAPIView.as_view(), name='list-jeuxdedonnées'),
    path('ressources/', RessourceListAPIView.as_view(), name='list-ressources'),
    path('motscles/', MotCléListAPIView.as_view(), name='list-motsclés'),
    path('organisations/', OrganisationListAPIView.as_view(), name='list-organisations'),
    path('groups/', GroupListAPIView.as_view(), name='list-groups'),
    path('jeu/<int:Id>/', JeuDeDonnéeDetailAPIView.as_view(), name='jeudedonnée-detail'),
    path('ressource/<int:Id>/', RessourceDetailAPIView.as_view(), name='ressource-detail'),
    path('motcle/<int:Id>/', MotCléDetailAPIView.as_view(), name='motclé-detail'),
    path('organisation/<int:Id>/', OrganisationDetailAPIView.as_view(), name='organisation-detail'),
    path('group/<int:Id>/', GroupDetailAPIView.as_view(), name='group-detail'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]