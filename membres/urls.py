from django.urls import path
from . import views

urlpatterns = [
    path('membres/', views.membres, name='membres'),
    path('ajouter/', views.ajouter_membre, name='ajouter_membre'),
   path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.accueil, name='accueil'), 
]
