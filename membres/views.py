from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from collections import Counter
import json
from django.core.mail import send_mail

from .models import Membre, OffreEmploi, Candidature, Experience
from .forms import MembreForm, OffreForm, CandidatureForm
from twilio.rest import Client


# 🔹 ACCUEIL
def accueil(request):
    return render(request, 'accueil.html')


# 🔹 LISTE MEMBRES
def membres(request):
    membres = Membre.objects.all()
    return render(request, 'membres.html', {'membres': membres})


# 🔹 AJOUT MEMBRE
def ajouter_membre(request):
    if request.method == 'POST':
        form = MembreForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')

            if email and Membre.objects.filter(email=email).exists():
                messages.error(request, "❌ Cet email existe déjà !")
            else:
                form.save()
                messages.success(request, "✅ Membre ajouté avec succès !")
                return redirect('membres')
    else:
        form = MembreForm()

    return render(request, 'ajouter_membre.html', {'form': form})


# 🔹 DASHBOARD
@login_required
def dashboard(request):
    membres = Membre.objects.all()
    offres = OffreEmploi.objects.all()
    candidatures = Candidature.objects.all()

    fonctions = [m.fonction for m in membres]
    stats = Counter(fonctions)

    return render(request, 'dashboard.html', {
        'total_membres': membres.count(),
        'total_offres': offres.count(),
        'total_candidatures': candidatures.count(),
        'labels': json.dumps(list(stats.keys())),
        'data': json.dumps(list(stats.values())),
    })


from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator

def inscription(request):

    if request.method == 'POST':

        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # verifier mot de passe
        if password != confirm_password:
            messages.error(request, "Les mots de passe ne correspondent pas")
            return redirect('/inscription/')

        # verifier email existe deja
        if User.objects.filter(username=email).exists():
            messages.error(request, "Ce compte existe déjà")
            return redirect('/accounts/login/')

        # creer utilisateur
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password
        )

        # connexion automatique
        login(request, user)

        # redirect profil
        return redirect('/profil/')

    return render(request, 'inscription.html')
# 💼 OFFRES
def offres(request):
    query = request.GET.get('q')

    if query:
        offres = OffreEmploi.objects.filter(
            Q(titre__icontains=query) |
            Q(entreprise__icontains=query)
        )
    else:
        offres = OffreEmploi.objects.all()

    return render(request, 'offres.html', {
        'offres': offres.order_by('-date_publication'),
        'query': query
    })
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()

        login(request, user)
        return redirect('profil')

    return render(request, 'activation_failed.html')

# ➕ AJOUTER OFFRE
@login_required
def ajouter_offre(request):
    if request.method == 'POST':
        form = OffreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('offres')
    else:
        form = OffreForm()

    return render(request, 'ajouter_offre.html', {'form': form})


# 📩 POSTULER
@login_required
def postuler(request, offre_id):
    offre = get_object_or_404(OffreEmploi, id=offre_id)

    if request.method == 'POST':
        form = CandidatureForm(request.POST, request.FILES)
        if form.is_valid():
            candidature = form.save(commit=False)
            candidature.utilisateur = request.user
            candidature.offre = offre
            candidature.save()

            messages.success(request, "📩 Candidature envoyée !")
            return redirect('offres')
    else:
        form = CandidatureForm()

    return render(request, 'postuler.html', {'form': form, 'offre': offre})


# 📊 CANDIDATURES
@login_required
def candidatures(request):
    candidatures = Candidature.objects.all().order_by('-date_postulation')
    return render(request, 'candidatures.html', {'candidatures': candidatures})


# 👤 PROFIL LINKEDIN
@login_required
def profil(request):
    membre = Membre.objects.filter(user=request.user).first()
    experiences = Experience.objects.filter(membre=membre)

    return render(request, 'profil.html', {
        'membre': membre,
        'experiences': experiences
    })


# ➕ AJOUT EXPERIENCE
@login_required
def ajouter_experience(request):
    membre = Membre.objects.get(user=request.user)

    if request.method == 'POST':
        Experience.objects.create(
            membre=membre,
            titre=request.POST.get('titre'),
            entreprise=request.POST.get('entreprise'),
            description=request.POST.get('description'),
            date_debut=request.POST.get('date_debut'),
            date_fin=request.POST.get('date_fin') or None
        )
        return redirect('profil')

    return render(request, 'ajouter_experience.html')


# 🔧 MODIFIER MEMBRE
@login_required
def modifier_membre(request, id):
    membre = get_object_or_404(Membre, id=id)

    if request.method == 'POST':
        form = MembreForm(request.POST, instance=membre)
        if form.is_valid():
            form.save()
            return redirect('membres')
    else:
        form = MembreForm(instance=membre)

    return render(request, 'modifier_membre.html', {'form': form})


# 🗑 SUPPRIMER MEMBRE
@login_required
def supprimer_membre(request, id):
    membre = get_object_or_404(Membre, id=id)
    membre.delete()
    return redirect('membres')


# 🔐 LOGIN EMAIL
def login_email(request):
    if request.method == 'POST':
        step = request.POST.get('step')

        # STEP 1 : EMAIL
        if step == "1":
            email = request.POST.get('email')

            user = User.objects.filter(email=email).first()
            if user:
                request.session['email'] = email
                return render(request, 'registration/login_password.html', {'email': email})
            else:
                messages.error(request, "Email introuvable")

        # STEP 2 : PASSWORD
        if step == "2":
            email = request.session.get('email')
            password = request.POST.get('password')

            user = User.objects.filter(email=email).first()

            if user:
                user = authenticate(request, username=user.username, password=password)

                if user:
                    login(request, user)
                    return redirect('profil')
                else:
                    messages.error(request, "Mot de passe incorrect")

    return render(request, 'registration/login.html')
from django.http import JsonResponse

def manifest(request):
    return JsonResponse({
        "name": "Zua Boulot",
        "short_name": "ZuaBoulot",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#ffffff",
        "theme_color": "#0d6efd",
        "icons": []
    })
def envoyer_sms(numero, message):
    try:
        client = Client("TON_SID", "TON_TOKEN")

        client.messages.create(
            body=message,
            from_="+1234567890",
            to=numero
        )
    except Exception as e:
        print("Erreur SMS:", e)
        
    