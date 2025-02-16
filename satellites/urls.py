from django.urls import path, include
from . import views

urlpatterns = [
  path('space', views.satellites),
  path('space/<str:name>', views.satellite),
]