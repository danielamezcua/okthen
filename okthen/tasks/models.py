from django.db import models
from personas.models import Persona
from workitems.models import WorkItem
#try
class Task(models.Model):
    ESTADO_CHOICES = ((0,'Pendiente'),
                      (1,'En proceso'),
                      (2, "Calidad"),
                      (3, "Terminada"))
    descripcion = models.CharField(blank=False,null=True, max_length=600)
    tiempo_estimado = models.DecimalField(max_digits=6, decimal_places=3)
    estado = models.IntegerField(choices=ESTADO_CHOICES, default=0)
    informacion_defecto = models.ForeignKey('tasks.InfoDefecto', on_delete=models.CASCADE, null=True)
    personas = models.ManyToManyField(Persona, through='PersonaTaskRelacion')
    work_item = models.ForeignKey(WorkItem, on_delete=models.CASCADE)
    fecha_termino = models.DateField(null= True)

    def obtener_logs(self):
        logs = PersonaTaskRelacion.objects.filter(task=self)
        return logs

    def __str__(self):
        return self.descripcion

class InfoDefecto(models.Model):
    #Quién encontró el defecto
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name="persona_detecta_defecto")
    #Task que tiene el defecto
    task_asociado = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="task_origen_defecto", null=True)
    #Task donde se encontró el defcto
    task_encontrado = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="task_encuentra_defecto", null=True)


class PersonaTaskRelacion(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    tiempo = models.DecimalField(max_digits=6, decimal_places=3)
    inicio = models.DateTimeField()
    fin = models.DateTimeField()