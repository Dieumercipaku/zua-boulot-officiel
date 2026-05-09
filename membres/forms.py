from django import forms
from .models import Membre, OffreEmploi, Candidature


# 🔹 FORM MEMBRE
class MembreForm(forms.ModelForm):
    class Meta:
        model = Membre
        fields = ['nom', 'postnom', 'prenom', 'fonction', 'email']

    # 🔐 Vérifier email unique
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Membre.objects.filter(email=email).exists():
            raise forms.ValidationError("❌ Cet email est déjà utilisé")
        return email


# 🔹 FORM OFFRE
class OffreForm(forms.ModelForm):
    class Meta:
        model = OffreEmploi
        fields = ['titre', 'description', 'entreprise']


# 🔹 FORM CANDIDATURE (PRO)
class CandidatureForm(forms.ModelForm):
    class Meta:
        model = Candidature
        fields = ['message', 'cv']

    # 🔒 Sécurité fichier CV
    def clean_cv(self):
        file = self.cleaned_data.get('cv')

        if file:
            # 🔥 taille max 5MB
            if file.size > 5 * 1024 * 1024:
                raise forms.ValidationError("❌ Fichier trop lourd (max 5MB)")

            # 🔥 type fichier autorisé
            if not file.name.endswith(('.pdf', '.doc', '.docx')):
                raise forms.ValidationError("❌ Format autorisé : PDF, DOC, DOCX")

        return file