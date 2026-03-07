from django.urls import path
from . import views

app_name = 'inscripcion_alumno'

urlpatterns = [
    path('', views.InscripcionAlumnoListView.as_view(), name='list'),
    path('create/', views.InscripcionAlumnoCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.InscripcionAlumnoUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.InscripcionAlumnoDeleteView.as_view(), name='delete'),
]