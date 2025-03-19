from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
  path('', views.get_posts),
  path('<int:id>', views.get_post),
  path('create', views.create_post),
  path('update/<int:id>', views.update_post),
  path('delete/<int:id>', views.delete_post),

  path('comments/create', views.create_comment),
  path('comments/update/<int:id>', views.update_comment),
  path('comments/delete/<int:id>', views.delete_comment),
  path('comments/delete/<int:id>', views.delete_comment),
]