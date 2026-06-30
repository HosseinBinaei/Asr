from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_time, name='get_time'),
    path('elapsed/<str:pk>', views.elapsed_view, name='elapsed'),
]