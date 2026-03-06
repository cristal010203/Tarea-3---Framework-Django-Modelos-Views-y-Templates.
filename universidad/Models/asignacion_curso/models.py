from django.db import models
from universidad.Models.Curso.models import Curso
from universidad.Models.catedratico.models import Catedratico


class AsignacionCurso(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    catedratico = models.ForeignKey(Catedratico, on_delete=models.CASCADE)
    horario = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.curso} - {self.catedratico} ({self.horario})"

    class Meta:
        db_table = 'asignacion_curso'

