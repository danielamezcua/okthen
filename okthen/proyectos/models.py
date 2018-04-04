from django.db import models
from personas.models import Persona

class Proyecto(models.Model):
    nombre = models.CharField(blank=False, null=True, max_length=300)
    integrantes = models.ManyToManyField(Persona)

    def __str__(self):
        return self.nombre
