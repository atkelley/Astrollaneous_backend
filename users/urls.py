from django.urls import path, include
from .api import RegisterAPI, LoginAPI, UserAPI, LoginView, LogoutAPI
from knox import views as knox_views
from . import views

app_name = 'users'

urlpatterns = [
  path('', views.get_users),
  path('<int:id>', views.get_user),
  # path('create', views.create_user),
  path('<int:id>/posts', views.user_posts),
  path('<int:id>/comments', views.user_comments),
  # path('update/<int:id>', views.update_user),
  # path('delete/<int:id>', views.delete_user),

  # path('login/', LoginView.as_view(), name='login'),

  # path('auth', include('knox.urls')),
  path('auth/user', UserAPI.as_view()),
  path('auth/login', LoginAPI.as_view()),
  path('auth/register', RegisterAPI.as_view()),
  path('auth/logout', LogoutAPI.as_view()),
  # path('auth/logout', knox_views.LogoutView.as_view(), name='knox_logout')
]