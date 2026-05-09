from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# 👤 MEMBRE (PROFIL PRINCIPAL)
class Membre(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    nom = models.CharField(max_length=100)
    postnom = models.CharField(max_length=100, blank=True)
    prenom = models.CharField(max_length=100)

    telephone = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(unique=True)

    fonction = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)

    # 🖼 PHOTO & CV
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    cv = models.FileField(upload_to='cv/', null=True, blank=True)

    code_membre = models.CharField(max_length=20, unique=True, blank=True)
    date_inscription = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.code_membre:
            year = timezone.now().year
            last_id = Membre.objects.count() + 1
            self.code_membre = f"ZB-{year}-{last_id:04d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom} {self.prenom}"
    otp_code = models.CharField(max_length=6, blank=True, null=True)


# 💼 EXPERIENCE (STYLE LINKEDIN)
class Experience(models.Model):
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE, related_name="experiences")

    titre = models.CharField(max_length=100)
    entreprise = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    date_debut = models.DateField()
    date_fin = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.titre} - {self.entreprise}"


# 💰 ADHESION
class Adhesion(models.Model):
    STATUT_CHOICES = [
        ('payé', 'Payé'),
        ('en attente', 'En attente'),
    ]

    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)

    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    statut = models.CharField(max_length=20, choices=STATUT_CHOICES)

    def __str__(self):
        return f"{self.membre.nom} - {self.montant}"


# 💼 OFFRE D'EMPLOI
class OffreEmploi(models.Model):
    titre = models.CharField(max_length=150)
    description = models.TextField()
    entreprise = models.CharField(max_length=150)

    date_publication = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre


# 🔔 NOTIFICATION
class Notification(models.Model):
    message = models.TextField()
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notif pour {self.membre.nom}"


# 📩 CANDIDATURE
class Candidature(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    offre = models.ForeignKey(OffreEmploi, on_delete=models.CASCADE)

    message = models.TextField()

    cv = models.FileField(upload_to='cv/', null=True, blank=True)

    date_postulation = models.DateTimeField(auto_now_add=True)

    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"{self.utilisateur.username} → {self.offre.titre}"