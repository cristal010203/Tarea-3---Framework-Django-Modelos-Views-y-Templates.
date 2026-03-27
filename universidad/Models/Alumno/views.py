from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Alumno
from .forms import AlumnoForm


def alumno_list(request):
    query      = request.GET.get('q', '').strip()
    object_list = Alumno.objects.all()

    if query:
        object_list = object_list.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)  |
            Q(email__icontains=query)
        )

    return render(request, 'alumno/list.html', {
        'object_list': object_list,
        'query':       query,
    })

def alumno_detail(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk)
    return render(request, 'alumno/detail.html', {'alumno': alumno})


def alumno_create(request):
    form = AlumnoForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Alumno registrado correctamente.')
        return redirect('alumno:list')
    return render(request, 'alumno/form.html', {
        'form':  form,
        'title': 'Nuevo Alumno',
    })


def alumno_edit(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk)
    form   = AlumnoForm(request.POST or None, instance=alumno)
    if form.is_valid():
        form.save()
        messages.success(request, 'Alumno actualizado correctamente.')
        return redirect('alumno:list')
    return render(request, 'alumno/form.html', {
        'form':  form,
        'title': f'Editar: {alumno.first_name} {alumno.last_name}',
    })


def alumno_delete(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk)
    if request.method == 'POST':
        alumno.delete()
        messages.success(request, 'Alumno eliminado correctamente.')
        return redirect('alumno:list')
    return render(request, 'alumno/confirm_delete.html', {'object': alumno})