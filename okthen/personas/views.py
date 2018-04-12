from django.shortcuts import render, get_object_or_404
from okthen.sessions import validate
from tasks.models import *
from .models import *
from django.db.models import Sum, Count
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
import json
from django.db import connection

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
        cursor = connection.cursor()
        #TIEMPO FASES
        cursor.execute(
        '''
        SELECT tipo, SUM(tiempo_estimado) as planeado
        FROM (SELECT tasks_task.id, tipo, tiempo_estimado
        FROM "tasks_task"
        INNER JOIN "tasks_personataskrelacion" ON ("tasks_task"."id" = "tasks_personataskrelacion"."task_id")
        INNER JOIN "personas_persona" ON ("tasks_personataskrelacion"."persona_id" = "personas_persona"."id")
        WHERE ("personas_persona"."nombre" = %s AND NOT ("tasks_task"."tipo" IS NULL))) as sub
        GROUP BY tipo''',[persona.nombre])
        tiempo_planeado = cursor.fetchall()
        cursor.execute(
        '''
        SELECT tipo, SUM(tiempo) as valor
        FROM (SELECT tasks_task.id, tipo, tiempo
        FROM "tasks_task"
        INNER JOIN "tasks_personataskrelacion" ON ("tasks_task"."id" = "tasks_personataskrelacion"."task_id")
        INNER JOIN "personas_persona" ON ("tasks_personataskrelacion"."persona_id" = "personas_persona"."id")
        WHERE ("personas_persona"."nombre" = %s AND NOT ("tasks_task"."tipo" IS NULL))) as sub
        GROUP BY tipo''',[persona.nombre])
        tiempo_real = cursor.fetchall()
        tiempos = []
        tiempo_planeado_total = 0
        tiempo_real_total = 0
        for tiempo in tiempo_planeado:
            for registro in tiempo_real:
                if tiempo[0]== registro[0]:
                    tiempo_planeado_total+=tiempo[1]
                    tiempo_real_total+=registro[1]
                    try:
                        porcentaje = round(((registro[1] * 100) / tiempo[1]),2)
                    except ZeroDivisionError:
                        porcentaje = 0
                    tiempos.append({'tipo':tiempo[0],'planeado':tiempo[1],'real':registro[1],'porcentaje':porcentaje})
        try:
            porcentaje_total = round(tiempo_real_total * 100 / tiempo_planeado_total,2)
        except ZeroDivisionError:
            porcentaje_total = 0
        total = {'tipo':'TOTAL','planeado':tiempo_planeado_total,'real':tiempo_real_total,'porcentaje':porcentaje_total }
        #DEFECTOS
        defectos_inyectados = InfoDefecto.objects.values('task_asociado__tipo').filter(persona__nombre=persona.nombre).annotate(Count('task_asociado__tipo')).exclude(task_asociado__tipo=None)
        defectos_resueltos = Task.objects.values('informacion_defecto__task_asociado__tipo').filter(informacion_defecto__persona=persona).filter(estado=3).annotate(Count('informacion_defecto__task_asociado__tipo')).exclude(informacion_defecto__task_asociado__tipo=None)
        defectos = []
        total_inyectados = 0
        total_resueltos = 0
        for x in defectos_inyectados:
                for z in defectos_resueltos:
                    if x['task_asociado__tipo'] == z['informacion_defecto__task_asociado__tipo']:
                        total_inyectados+=x['task_asociado__tipo__count']
                        total_resueltos+=z['informacion_defecto__task_asociado__tipo__count']
                        try:
                            porcentaje = round(((z['informacion_defecto__task_asociado__tipo__count'] * 100) / x['task_asociado__tipo__count']),2)
                        except ZeroDivisionError:
                            porcentaje = 0
                        defectos.append({'tipo':x['task_asociado__tipo'],'inyectados':x['task_asociado__tipo__count'],'resueltos':z['informacion_defecto__task_asociado__tipo__count'],'porcentaje':porcentaje})
        try:
            porcentaje_total = round(((total_resueltos * 100) / total_inyectados),2)
        except ZeroDivisionError:
            porcentaje_total = 0
        total_defectos = {'tipo':'TOTAL','inyectados':total_inyectados,'resueltos':total_resueltos,'porcentaje':porcentaje_total }
        return render(request, 'resumen_persona.html', {'persona':persona, 'logs':logs,'tiempos':tiempos,'total':total,'defectos':defectos,'total_defectos':total_defectos})
    return valid

def consulta_fases(request, id_persona):
    if request.method == 'POST':
            valores = []
            persona = get_object_or_404(Persona, pk=id_persona)
            cursor = connection.cursor()
            #TIEMPO FASES
            cursor.execute(
            '''
            SELECT tipo, SUM(tiempo_estimado) as planeado
            FROM (SELECT tasks_task.id, tipo, tiempo_estimado
            FROM "tasks_task"
            INNER JOIN "tasks_personataskrelacion" ON ("tasks_task"."id" = "tasks_personataskrelacion"."task_id")
            INNER JOIN "personas_persona" ON ("tasks_personataskrelacion"."persona_id" = "personas_persona"."id")
            WHERE ("personas_persona"."nombre" = %s AND NOT ("tasks_task"."tipo" IS NULL))) as sub
            GROUP BY tipo''',[persona.nombre])
            tiempo_planeado = cursor.fetchall()
            cursor.execute(
            '''
            SELECT tipo, SUM(tiempo) as valor
            FROM (SELECT tasks_task.id, tipo, tiempo
            FROM "tasks_task"
            INNER JOIN "tasks_personataskrelacion" ON ("tasks_task"."id" = "tasks_personataskrelacion"."task_id")
            INNER JOIN "personas_persona" ON ("tasks_personataskrelacion"."persona_id" = "personas_persona"."id")
            WHERE ("personas_persona"."nombre" = %s AND NOT ("tasks_task"."tipo" IS NULL))) as sub
            GROUP BY tipo''',[persona.nombre])
            tiempo_real = cursor.fetchall()
            data_planeado = []
            data_real = []
            fases = []
            for tiempo in tiempo_planeado:
                data_planeado.append(float(tiempo[1]))
                fases.append(tiempo[0])
            valores.append({'label':'Planeado','backgroundColor':'gray','data':data_planeado})
            for tiempo in tiempo_real:
                data_real.append(float(tiempo[1]))
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
            numeros = InfoDefecto.objects.values('fecha').filter(persona__nombre=persona.nombre).annotate(Count('fecha')).exclude(task_asociado__tipo=None)
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
