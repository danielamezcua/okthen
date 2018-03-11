from django.db import models
from personas.models import Persona
from workitems.models import WorkItem

class Task(models.Model):
    ESTADO_CHOICES = ((0,'Pendiente'),
                      (1,'En proceso'),
                      (2, "Calidad"),
                      (3, "Terminada"))
    descripcion = models.CharField(blank=False,null=True, max_length=600)
    tiempo_estimado = models.DurationField()
    estado = models.IntegerField(choices=ESTADO_CHOICES)
    defecto = models.BooleanField(default=False)
    personas = models.ManyToManyField(Persona, through='PersonaTaskRelacion')
    work_item = models.ForeignKey(WorkItem, on_delete=models.CASCADE)

class PersonaTaskRelacion(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    tiempo = models.DurationField()
    inicio = models.DateTimeField()
    fin = models.DateTimeField()