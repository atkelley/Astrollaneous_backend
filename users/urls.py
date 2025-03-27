from django.urls import path, include
from .api import RegisterAPI, LoginAPI, UserAPI, LogoutAPI
from . import views

app_name = 'users'

urlpatterns = [
  path('', views.get_users),
  path('<int:id>', views.get_user),
  path('<int:id>/posts', views.user_posts),
  path('<int:id>/comments', views.user_comments),
  path('delete/<int:id>', views.delete_user),

  path('auth', include('knox.urls')),
  # path('auth/user', UserAPI.as_view()),
  path('auth/login', LoginAPI.as_view()),
  path('auth/register', RegisterAPI.as_view()),
  path('auth/logout', LogoutAPI.as_view())
]