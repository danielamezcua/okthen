from django.forms import ModelForm
from django import forms
from .models import Task, PersonaTaskRelacion
from okthen import settings
import datetime


class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'
    format(['%Y-%m-%dT%H:%M:%S'])

class ModalTask(ModelForm):
    model = Task
    tiempo_estimado = forms.FloatField(min_value=0)
    class Meta:
        model = Task
        fields = ['descripcion', 'tiempo_estimado']

    def clean_tiempo_estimado(self):
        tiempo = self.cleaned_data['tiempo_estimado']
        return datetime.timedelta(hours=tiempo)

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