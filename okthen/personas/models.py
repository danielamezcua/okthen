from django.db import models

class Persona(models.Model):
    nombre = models.CharField(blank=False,null=True, max_length=150)

    def __str__(self):
        return self.nombre