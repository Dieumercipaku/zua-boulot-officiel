from django.urls import path
from . import views

urlpatterns = [
    # 🏠 Accueil
    path('', views.accueil, name='accueil'),

    # 👥 Membres
    path('membres/', views.membres, name='membres'),
    path('ajouter/', views.ajouter_membre, name='ajouter_membre'),

    # 📊 Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # 💼 Offres d’emploi
    path('offres/', views.offres, name='offres'),
    path('offres/ajouter/', views.ajouter_offre, name='ajouter_offre'),

    # 🔐 Authentification
    path('inscription/', views.inscription, name='inscription'),
]