from django.shortcuts import render, redirect
from .models import Membre
from .forms import MembreForm
from collections import Counter
import json


# 🔹 LISTE MEMBRES
def membres(request):
    liste = Membre.objects.all()
    return render(request, 'membres.html', {'membres': liste})


# 🔹 AJOUT MEMBRE
def ajouter_membre(request):
    if request.method == 'POST':
        form = MembreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('membres')
    else:
        form = MembreForm()

    return render(request, 'ajouter_membre.html', {'form': form})


# 🔹 RECHERCHE MEMBRES (version corrigée UNIQUE)
def membre_list(request):
    query = request.GET.get('q')

    if query:
        membres = Membre.objects.filter(nom__icontains=query)
    else:
        membres = Membre.objects.all()

    return render(request, 'membres/list.html', {'membres': membres})


# 🔹 DASHBOARD
def dashboard(request):
    membres = Membre.objects.all()

    total = membres.count()

    # Statistiques par fonction
    fonctions = [m.fonction for m in membres]
    stats = Counter(fonctions)

    labels = list(stats.keys())
    data = list(stats.values())

    derniers = Membre.objects.order_by('-id')[:5]

    return render(request, 'dashboard.html', {
        'total': total,
        'derniers': derniers,
        'labels': json.dumps(labels),
        'data': json.dumps(data),
    })


# 🔹 ACCUEIL (IMPORTANT - manquait chez toi)
def accueil(request):
    return render(request, 'accueil.html')