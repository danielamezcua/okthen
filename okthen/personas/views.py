from django.shortcuts import render, get_object_or_404
from okthen.sessions import validate
from tasks.models import Task, PersonaTaskRelacion
from .models import Persona

def index(request):
    valid = validate(request)
    if valid == True:
        personas = Persona.objects.all()
        return render(request, 'index_personas.html', {'personas':personas})
    return valid


def resumen(request, id_persona):
    valid = validate(request)
    if valid == True:
        persona = get_object_or_404(Persona, pk=id_persona)
        logs = PersonaTaskRelacion.objects.filter(persona=persona)
        return render(request, 'resumen_persona.html', {'persona':persona, 'logs':logs})
    return valid
