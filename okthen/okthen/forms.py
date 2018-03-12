from django import forms
from personas.models import Persona
class Login(forms.Form):
    query = Persona.objects.all()
    personas = forms.ModelChoiceField(query)