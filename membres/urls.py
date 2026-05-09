from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    # 🏠 Accueil
    path('', views.accueil, name='accueil'),

    # 🔐 Auth
    path('accounts/login/', views.login_email, name='login'),
    path('inscription/', views.inscription, name='inscription'),

    # 👤 Profil
    path('profil/', views.profil, name='profil'),
    path('experience/ajouter/', views.ajouter_experience, name='ajouter_experience'),

    # 👥 Membres
    path('membres/', views.membres, name='membres'),
    path('ajouter/', views.ajouter_membre, name='ajouter_membre'),
    path('modifier/<int:id>/', views.modifier_membre, name='modifier_membre'),
    path('supprimer/<int:id>/', views.supprimer_membre, name='supprimer_membre'),

    # 📊 Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # 💼 Offres
    path('offres/', views.offres, name='offres'),
    path('offres/ajouter/', views.ajouter_offre, name='ajouter_offre'),
    path('offres/<int:offre_id>/postuler/', views.postuler, name='postuler'),

    # 📩 Candidatures
    path('candidatures/', views.candidatures, name='candidatures'),

    # 🤖 IA (⚠️ seulement si les views existent)
    # path('recommandations/', views.recommandations, name='recommandations'),
    # path('ia-cv/', views.recommandations_cv, name='recommandations_cv'),

    # 📱 PWA / APK
    path('manifest.json', views.manifest, name='manifest'),
    path('manifest.webmanifest', views.manifest),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path(
    'password-reset/',
    auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset.html'
    ),
    name='password_reset'
),

path(
    'password-reset/done/',
    auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ),
    name='password_reset_done'
),

path(
    'reset/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'
    ),
    name='password_reset_confirm'
),

path(
    'reset/done/',
    auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ),
    name='password_reset_complete'
),
    
]