from django.urls import path
from . import views

app_name = 'notas'

urlpatterns = [
    path('', views.NotaListView.as_view(), name='list'),
    path('create/', views.NotaCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.NotaUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.NotaDeleteView.as_view(), name='delete'),
]
