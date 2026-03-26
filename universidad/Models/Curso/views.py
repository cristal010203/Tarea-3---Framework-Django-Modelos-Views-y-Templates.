from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Curso

class CursoListView(ListView):
    model = Curso
    template_name = 'curso/list.html'
    context_object_name = 'object_list'

class CursoCreateView(CreateView):
    model = Curso
    fields = ['nombre', 'descripcion', 'creditos', 'docente']
    template_name = 'curso/form.html'
    success_url = reverse_lazy('curso:list')

class CursoUpdateView(UpdateView):
    model = Curso
    fields = ['nombre', 'descripcion', 'creditos', 'docente']
    template_name = 'curso/form.html'
    success_url = reverse_lazy('curso:list')

class CursoDeleteView(DeleteView):
    model = Curso
    template_name = 'curso/confirm_delete.html'
    success_url = reverse_lazy('curso:list')

