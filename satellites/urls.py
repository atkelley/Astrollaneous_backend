from django.urls import path, include
from . import views

urlpatterns = [
  path('', views.satellites),
  path('<str:name>', views.satellite),
]