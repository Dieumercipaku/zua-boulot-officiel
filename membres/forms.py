from django import forms
from .models import Membre

class MembreForm(forms.ModelForm):
    class Meta:
        model = Membre
        fields = ['nom', 'postnom', 'prenom', 'telephone']