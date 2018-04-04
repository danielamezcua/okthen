from django.shortcuts import render, get_object_or_404
from okthen.sessions import validate
from tasks.models import Task, PersonaTaskRelacion
from .models import *
from django.db.models import Sum
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
import json

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
        tiempo_planeado = Task.objects.values('tipo').filter(personas__nombre=persona.nombre).annotate(planeado=Sum('tiempo_estimado')).exclude(tipo=None)
        tiempo_real = PersonaTaskRelacion.objects.values('task__tipo').filter(task__personas__nombre=persona.nombre).annotate(real=Sum('tiempo')).exclude(task__tipo=None)
        tiempos = []
        tiempo_planeado_total = 0
        tiempo_real_total = 0
        for tiempo in tiempo_planeado:
            for registro in tiempo_real:
                if tiempo["tipo"] == registro["task__tipo"]:
                    tiempo_planeado_total+=tiempo['planeado']
                    tiempo_real_total+=registro['real']
                    porcentaje = round(((registro['real'] * 100) / tiempo['planeado']),2)
                    tiempos.append({'tipo':tiempo["tipo"],'planeado':tiempo['planeado'],'real':registro["real"],'porcentaje':porcentaje})
        porcentaje_total = round(tiempo_real_total * 100 / tiempo_planeado_total,2)
        total = {'tipo':'TOTAL','planeado':tiempo_planeado_total,'real':tiempo_real_total,'porcentaje':porcentaje_total }
        return render(request, 'resumen_persona.html', {'persona':persona, 'logs':logs,'tiempos':tiempos,'total':total})
    return valid

def consulta_fases(request, id_persona):
    if request.method == 'POST':
            valores = []
            persona = get_object_or_404(Persona, pk=id_persona)
            tiempo_planeado = Task.objects.values('tipo').filter(personas__nombre=persona.nombre).annotate(planeado=Sum('tiempo_estimado')).exclude(tipo=None)
            tiempo_real = PersonaTaskRelacion.objects.values('task__tipo').filter(task__personas__nombre=persona.nombre).annotate(real=Sum('tiempo')).exclude(task__tipo=None)
            data_planeado = []
            data_real = []
            fases = []
            for tiempo in tiempo_planeado:
                data_planeado.append(float(tiempo['planeado']))
                fases.append(tiempo['tipo'])
            valores.append({'label':'Planeado','backgroundColor':'gray','data':data_planeado})
            for tiempo in tiempo_real:
                data_real.append(float(tiempo['real']))
            valores.append({'label':'Real','backgroundColor':'black','data':data_real})
            data = {
                "labels":fases,
                "datasets":valores
            }
            return JsonResponse(data)
