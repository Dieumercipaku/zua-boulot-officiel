from django.contrib import admin
from django.urls import path, include
from membres import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # 🔥 PAGE D'ACCUEIL
    path('', views.accueil, name='accueil'),

    # 🔥 TOUT LE RESTE
    path('', include('membres.urls')),

    # 🔐 AUTH
    path('accounts/', include('django.contrib.auth.urls')),
]