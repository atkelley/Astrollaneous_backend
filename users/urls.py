from django.urls import path, include
from .api import UserAPI, RegisterAPI, LoginAPI
from knox.views import LogoutView
from . import views

app_name = "users"

urlpatterns = [
  path("", views.get_users),
  path("<int:id>", views.get_user),
  path("<int:id>/posts", views.user_posts),
  path("<int:id>/comments", views.user_comments),
  path("delete/<int:id>", views.delete_user),

  # path("auth", include("knox.urls")),
  path("auth/user", UserAPI.as_view(), name="user"),
  path("auth/login", LoginAPI.as_view(), name="login"),
  path("auth/register", RegisterAPI.as_view(), name="register"),
  path("auth/logout", LogoutView.as_view(), name="logout"),
]