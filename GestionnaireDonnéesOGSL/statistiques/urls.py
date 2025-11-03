from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='stats-index'), 
    path('canwin/',views.canWin),
    path('dq/',views.DonneeQuebec),
    path('og/',views.OpenGouv),
]