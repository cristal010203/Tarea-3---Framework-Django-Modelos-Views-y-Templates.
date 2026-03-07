from django.urls import path
from . import views

app_name = 'catedratico'

urlpatterns = [
    path('', views.CatedraticoListView.as_view(), name='list'),
    path('create/', views.CatedraticoCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.CatedraticoUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.CatedraticoDeleteView.as_view(), name='delete'),
]