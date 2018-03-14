from django.forms import ModelForm
from django import forms
from .models import Task, PersonaTaskRelacion
from workitems.models import WorkItem
from okthen import settings
import datetime


class DateTimeInput(forms.DateTimeInput):
    input_type = 'text'
    format(['%Y-%m-%dT%H:%M:%S'])

class ModalTask(ModelForm):
    model = Task
    tiempo_estimado = forms.DecimalField(max_digits=6, decimal_places=3, min_value=0)
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

class DefectoForm(forms.Form):
    workitems = WorkItem.objects.all()
    tasks = Task.objects.all()
    workitem = forms.ModelChoiceField(workitems)
    task = forms.ModelChoiceField(tasks)
    descripcion = forms.CharField(max_length=200)
    tiempo_estimado = forms.DecimalField(max_digits=6, decimal_places=3, min_value=0)
