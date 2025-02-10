from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
  # path("posts", views.index, name="index"),

  # path('user/<int:id>', views.get_user),
  # path('user/<int:id>/posts', views.user_posts),
  # path('user/<int:id>/comments', views.user_comments),

  path('posts', views.posts),
  path('posts/<int:id>', views.get_post),
  path('posts/create', views.create_post),
  path('posts/update/<int:id>', views.update_post),
  path('posts/delete/<int:id>', views.delete_post),

  path('comments/create', views.create_comment),
  path('comments/update/<int:id>', views.update_comment),
  path('comments/delete/<int:id>', views.delete_comment),
  path('comments/delete/<int:id>', views.delete_comment),
]