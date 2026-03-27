from django.urls import path
from . import views

app_name = 'reportes'

urlpatterns = [
    path('rendimiento/',     views.reporte_rendimiento,    name='rendimiento'),
    path('carga-academica/', views.reporte_carga_academica, name='carga_academica'),
]