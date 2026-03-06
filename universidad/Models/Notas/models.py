from django.db import models
from universidad.Models.Alumno.models import Alumno
from universidad.Models.Curso.models import Curso

class Nota(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    nota = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.alumno} - {self.curso}: {self.nota}"

    class Meta:
        db_table = 'nota'

