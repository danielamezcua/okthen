from django.shortcuts import render, get_object_or_404
from okthen.sessions import validate
from tasks.models import *
from .models import *
from django.db.models import Sum, Count
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
        #TIEMPO FASES
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
        #DEFECTOS
        defectos_inyectados = InfoDefecto.objects.values('task_asociado__tipo').filter(persona__nombre=persona.nombre).annotate(Count('task_asociado__tipo'))
        defectos_resueltos = Task.objects.values('informacion_defecto__task_asociado__tipo').filter(informacion_defecto__persona=persona).filter(estado=3).annotate(Count('informacion_defecto__task_asociado__tipo'))
        defectos = []
        total_inyectados = 0
        total_resueltos = 0
        for x in defectos_inyectados:
                for z in defectos_resueltos:
                    if x['task_asociado__tipo'] == z['informacion_defecto__task_asociado__tipo']:
                        total_inyectados+=x['task_asociado__tipo__count']
                        total_resueltos+=z['informacion_defecto__task_asociado__tipo__count']
                        porcentaje = round(((z['informacion_defecto__task_asociado__tipo__count'] * 100) / x['task_asociado__tipo__count']),2)
                        defectos.append({'tipo':x['task_asociado__tipo'],'inyectados':x['task_asociado__tipo__count'],'resueltos':z['informacion_defecto__task_asociado__tipo__count'],'porcentaje':porcentaje})
        porcentaje_total = round(((total_resueltos * 100) / total_inyectados),2)
        total_defectos = {'tipo':'TOTAL','inyectados':total_inyectados,'resueltos':total_resueltos,'porcentaje':porcentaje_total }
        return render(request, 'resumen_persona.html', {'persona':persona, 'logs':logs,'tiempos':tiempos,'total':total,'defectos':defectos,'total_defectos':total_defectos})
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

def consulta_defectos(request, id_persona):
    if request.method == 'POST':
            valores = []
            persona = get_object_or_404(Persona, pk=id_persona)
            numeros = InfoDefecto.objects.values('fecha').filter(persona__nombre=persona.nombre).annotate(Count('fecha'))
            data_defectos = []
            fechas = []
            for numero in numeros:
                data_defectos.append(numero['fecha__count'])
                fechas.append(numero['fecha'].strftime('%d/%m/%Y'))
            valores = []
            valores.append({'label':'Defectos por día','borderColor':'gray','data':data_defectos,'fill':False})
            data = {
                "labels":fechas,
                "datasets":valores
            }
            return JsonResponse(data)
