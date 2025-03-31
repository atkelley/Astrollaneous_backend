from rest_framework import serializers 
from .models import Post, Comment
from django.contrib.auth.models import User
from users.serializers import UserSerializer

class CommentSerializer(serializers.ModelSerializer):
  user = UserSerializer(read_only=True)
  post_title = serializers.SerializerMethodField()
  # post = serializers.PrimaryKeyRelatedField(read_only=True) 
  
  class Meta:
    model = Comment
    fields = ('id',
              'post',
              'user',
              'text',
              'post_title',
              'created_date')
    
  def get_post_title(self, obj):
    return obj.post.title
 
class PostSerializer(serializers.ModelSerializer):
  user = UserSerializer(read_only=True)
  comments = CommentSerializer(many=True, read_only=True)
 
  class Meta:
    model = Post
    fields = ('id',
              'user',
              'title',
              'image_url',
              'created_date',
              'text',
              'text_html',
              'comments')