from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
import misaka

class Post(models.Model):
  user = models.ForeignKey(User, related_name="blog", on_delete=models.CASCADE)
  title = models.CharField(max_length=200)
  image_url = models.CharField(max_length=200, null=True, blank=True)
  created_date = models.DateTimeField(default=timezone.now, editable=True)
  text = models.TextField()
  text_html = models.TextField(null=True, editable=False)

  def __str__(self):
    return self.title

  def save(self, *args, **kwargs):
    self.text_html = misaka.html(self.text)
    super().save(*args, **kwargs)

  def get_absolute_url(self):
    return reverse(
      "blog:post_list",
      kwargs={
        "username": self.user.username,
        "pk": self.pk
      }
    )

  def get_comments(self):
    return self.comments

  class Meta:
    ordering = ["-created_date"]
    unique_together = ["user", "text"]


class Comment(models.Model):
  post = models.ForeignKey('blog.Post', related_name='comments', on_delete=models.CASCADE)
  user = models.ForeignKey(User, default = 1, null = True, related_name="comments", on_delete=models.CASCADE)
  text = models.TextField()
  created_date = models.DateTimeField(default=timezone.now, editable=True)

  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)

  def __str__(self):
    return self.text

  def get_absolute_url(self):
    return reverse(
      "blog:post_list",
      kwargs={
        "username": self.user.username,
        "pk": self.pk
      }
    )

  class Meta:
    ordering = ["created_date"]
