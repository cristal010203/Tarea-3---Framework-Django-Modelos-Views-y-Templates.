from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Catedratico

class CatedraticoListView(ListView):
    model = Catedratico
    template_name = 'catedratico/list.html'
    context_object_name = 'object_list'

class CatedraticoCreateView(CreateView):
    model = Catedratico
    fields = ['first_name', 'last_name', 'especialidad', 'email', 'phone']
    template_name = 'catedratico/form.html'
    success_url = reverse_lazy('catedratico:list')

class CatedraticoUpdateView(UpdateView):
    model = Catedratico
    fields = ['first_name', 'last_name', 'especialidad', 'email', 'phone']
    template_name = 'catedratico/form.html'
    success_url = reverse_lazy('catedratico:list')

class CatedraticoDeleteView(DeleteView):
    model = Catedratico
    template_name = 'catedratico/confirm_delete.html'
    success_url = reverse_lazy('catedratico:list')
