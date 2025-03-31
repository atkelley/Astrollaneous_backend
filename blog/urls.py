from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
  path('', views.get_posts),
  path('<int:id>', views.get_post),
  path('create', views.create_post),
  path('update/<int:id>', views.update_post),
  path('delete/<int:id>', views.delete_post),

  path('comment/create/<int:id>', views.create_comment),
  path('comment/update/<int:id>', views.update_comment),
  path('comment/delete/<int:id>', views.delete_comment),
]