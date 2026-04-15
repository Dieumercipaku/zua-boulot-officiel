from django.db import models


from django.db import models
from django.utils import timezone
import random

def generate_code():
    return f"ZB-{timezone.now().year}-{random.randint(1000,9999)}"


# 👤 Membre
class Membre(models.Model):
    nom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    code_membre = models.CharField(max_length=20, unique=True, blank=True)
    date_inscription = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.code_membre:
            year = timezone.now().year
            last_id = Membre.objects.count() + 1
            self.code_membre = f"ZB-{year}-{last_id:04d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom

class Membre(models.Model):
    nom = models.CharField(max_length=100)
    postnom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    fonction = models.CharField(max_length=100)
    date_adhesion = models.CharField(max_length=100)
    date_adhesion = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} {self.prenom}"
    
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
class OffreEmploi(models.Model):
    titre = models.CharField(max_length=150)
    description = models.TextField()
    entreprise = models.CharField(max_length=150)
    date_publication = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre

class Notification(models.Model):
    message = models.TextField()
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notif pour {self.membre.nom}"        