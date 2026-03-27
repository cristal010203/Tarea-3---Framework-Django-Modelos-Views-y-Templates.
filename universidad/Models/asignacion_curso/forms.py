from django import forms
from django.core.exceptions import ValidationError
from .models import AsignacionCurso
from universidad.Models.Alumno.models import Alumno


class AsignacionCursoForm(forms.ModelForm):
    carnet = forms.CharField(
        max_length=10,
        label="Carné del alumno",
        help_text="Ingresa el número de carné de 10 dígitos.",
        widget=forms.TextInput(attrs={
            'maxlength': '10',
            'placeholder': '0000000000'
        })
    )

    class Meta:
        model  = AsignacionCurso
        fields = ['curso', 'horario', 'aula', 'cupo']

    def clean_carnet(self):
        carnet = self.cleaned_data.get('carnet', '').strip()

        if not carnet.isdigit():
            raise ValidationError("El carné solo puede contener dígitos.")

        if len(carnet) != 10:
            raise ValidationError("El carné debe tener exactamente 10 dígitos.")

        try:
            alumno = Alumno.objects.get(carnet=carnet)
        except Alumno.DoesNotExist:
            raise ValidationError("No existe ningún alumno con este número de carné.")

        if not alumno.is_active:
            raise ValidationError(
                f"El alumno {alumno.first_name} {alumno.last_name} no está activo."
            )

        self.instance.alumno = alumno
        return carnet

    def clean(self):
        cleaned = super().clean()
        curso   = cleaned.get('curso')
        alumno  = getattr(self.instance, 'alumno', None)

        if curso and alumno:
            existe = AsignacionCurso.objects.filter(
                curso=curso,
                alumno=alumno
            ).exclude(pk=self.instance.pk).exists()
            if existe:
                raise ValidationError(
                    "Este alumno ya está asignado a este curso."
                )
        return cleaned