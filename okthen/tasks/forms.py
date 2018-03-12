from django.forms import ModelForm
from django import forms
from .models import Task, PersonaTaskRelacion
from okthen import settings


class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'
    format(['%Y-%m-%dT%H:%M'])

class ModalTask(ModelForm):
    model = Task
    tiempo_estimado = forms.FloatField(min_value=0)
    class Meta:
        model = Task
        fields = ['descripcion', 'tiempo_estimado']

class AcabarTask(ModelForm):
    OPCIONES = (
                (0, 'No'),
                (1,'Sí')
                )
    acabada = forms.IntegerField(widget=forms.Select(choices=OPCIONES))

    class Meta:
        model = PersonaTaskRelacion
        fields = ['inicio', 'fin', 'acabada']
        widgets = {
            'inicio':DateTimeInput(),
            'fin':DateTimeInput()
        }