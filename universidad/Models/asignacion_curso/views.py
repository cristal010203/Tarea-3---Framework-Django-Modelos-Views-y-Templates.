from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import AsignacionCurso

class AsignacionCursoListView(ListView):
    model = AsignacionCurso
    template_name = 'asignacion_curso/list.html'

class AsignacionCursoCreateView(CreateView):
    model = AsignacionCurso
    fields = ['curso', 'catedratico', 'horario']
    template_name = 'asignacion_curso/form.html'
    success_url = reverse_lazy('asignacion_curso:list')

class AsignacionCursoUpdateView(UpdateView):
    model = AsignacionCurso
    fields = ['curso', 'catedratico', 'horario']
    template_name = 'asignacion_curso/form.html'
    success_url = reverse_lazy('asignacion_curso:list')

class AsignacionCursoDeleteView(DeleteView):
    model = AsignacionCurso
    template_name = 'asignacion_curso/confirm_delete.html'
    success_url = reverse_lazy('asignacion_curso:list')
