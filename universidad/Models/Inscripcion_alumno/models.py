from django.db import models
from universidad.Models.Alumno.models import Alumno
from universidad.Models.asignacion_curso.models import AsignacionCurso

class InscripcionAlumno(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    fecha_asignacion = models.DateField(auto_now_add=True)
    asignacion_curso = models.ManyToManyField(AsignacionCurso)

    def __str__(self):
        return f"{self.alumno} - {self.fecha_asignacion}"

    class Meta:
        db_table = 'inscripcion_alumno'

