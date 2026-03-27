from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import AsignacionCurso
from .forms import AsignacionCursoForm


class AsignacionCursoListView(ListView):
    model = AsignacionCurso
    template_name = 'asignacion_curso/list.html'
    context_object_name = 'object_list'


class AsignacionCursoCreateView(CreateView):
    model         = AsignacionCurso
    form_class    = AsignacionCursoForm
    template_name = 'asignacion_curso/form.html'
    success_url   = reverse_lazy('asignacion_curso:list')


class AsignacionCursoUpdateView(UpdateView):
    model         = AsignacionCurso
    form_class    = AsignacionCursoForm
    template_name = 'asignacion_curso/form.html'
    success_url   = reverse_lazy('asignacion_curso:list')

    def get_initial(self):
        initial = super().get_initial()
        if self.object.alumno:
            initial['carnet'] = self.object.alumno.carnet
        return initial


class AsignacionCursoDeleteView(DeleteView):
    model         = AsignacionCurso
    template_name = 'asignacion_curso/confirm_delete.html'
    success_url   = reverse_lazy('asignacion_curso:list')