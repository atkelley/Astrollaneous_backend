from django.urls import path
from .api import CreatePostAPI, UpdatePostAPI, DeletePostAPI, CreateCommentAPI, UpdateCommentAPI, DeleteCommentAPI
from . import views

app_name = "blog"

urlpatterns = [
  path("", views.get_posts),
  path("<int:id>", views.get_post),
  path("create", CreatePostAPI.as_view(), name="create_post"),
  path("update/<int:pk>", UpdatePostAPI.as_view(), name="update_post"),
  path("delete/<int:pk>", DeletePostAPI.as_view(), name="delete_post"),

  path("comment/create", CreateCommentAPI.as_view(), name="create_comment"),
  path("comment/update/<int:comment_id>", UpdateCommentAPI.as_view(), name="update_comment"),
  path("comment/delete/<int:comment_id>", DeleteCommentAPI.as_view(), name="delete_comment"),
]