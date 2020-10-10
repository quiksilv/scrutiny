from django import forms
from .models import Politician
class PoliticianForm(forms.ModelForm):
    class Meta:
        model = Politician
        fields = ['name', 'twitter', 'facebook', 'wikipedia']
