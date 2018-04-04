from django.db import models
from personas.models import Persona
from workitems.models import WorkItem
from django.db.models import Sum, F
from decimal import Decimal
import math
import datetime

#try
class Task(models.Model):
    ESTADO_CHOICES = ((0,'Pendiente'),
                      (1,'En proceso'),
                      (2, "Calidad"),
                      (3, "Terminada"))
    FASES = (('PLAN','PLAN'),
            ('DISEÑO','DISEÑO'),
            ('DESARROLLO','DESARROLLO'),
            ('PRUEBAS', "PRUEBAS"),
            ('POSTMORTEM', "POSTMORTEM"),
            ('DEFECTOS', "DEFECTOS"))

    descripcion = models.CharField(blank=False,null=True, max_length=600)
    tiempo_estimado = models.DecimalField(max_digits=6, decimal_places=3)
    estado = models.IntegerField(choices=ESTADO_CHOICES, default=0)
    informacion_defecto = models.ForeignKey('tasks.InfoDefecto', on_delete=models.CASCADE, null=True)
    personas = models.ManyToManyField(Persona, through='PersonaTaskRelacion')
    work_item = models.ForeignKey(WorkItem, on_delete=models.CASCADE)
    fecha_termino = models.DateField(null= True)
    tipo = models.CharField(max_length=50, choices=FASES, null=True)

    def obtener_logs(self):
        logs = PersonaTaskRelacion.objects.filter(task=self)
        return logs

    def obtener_defectos(self):
        defectos = Task.objects.filter(informacion_defecto__isnull=False).filter(informacion_defecto__task_asociado=self)
        return defectos

    def obtener_tiempo(self):
        return PersonaTaskRelacion.objects.filter(task=self).aggregate(total=Sum('tiempo'))['total'] or 0

    def obtener_tiempo_defectos(self):
        defectos = self.obtener_defectos()
        tiempo = Decimal(0)
        for defecto in defectos:
            tiempo+=defecto.obtener_tiempo()
        return tiempo or 0

    def obtener_tiempo_total(self):
        return self.obtener_tiempo_defectos() + self.obtener_tiempo()

    def contar_defectos(self):
        return self.obtener_defectos().count()

    def obtener_error(self):
        return round(Decimal(math.fabs(self.tiempo_estimado - self.obtener_tiempo_total()))/self.tiempo_estimado,4)

    def __str__(self):
        return self.descripcion

class InfoDefecto(models.Model):
    TIPOS = (('Documentación','Documentación'),
            ('Sintaxis','Sintaxis'),
            ('Interfaz','Interfaz'),
            ('Funcionalidad', 'Funcionalidad'),
            ('Sistema', 'Sistema'),
            ('Ambiente', 'Ambiente'))
    #Quién encontró el defecto
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name="persona_detecta_defecto")
    #Task que tiene el defecto
    task_asociado = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="task_origen_defecto", null=True)
    #Task donde se encontró el defcto
    task_encontrado = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="task_encuentra_defecto", null=True)
    fecha = models.DateField(null= True, default=datetime.date.today)
    tipo = models.CharField(max_length=50, choices=TIPOS, null=True)

class PersonaTaskRelacion(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    tiempo = models.DecimalField(max_digits=6, decimal_places=3)
    inicio = models.DateTimeField()
    fin = models.DateTimeField()
