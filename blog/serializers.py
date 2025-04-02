from rest_framework import serializers 
from .models import Post, Comment
from users.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
  user = UserSerializer(read_only=True)
  post_title = serializers.SerializerMethodField()
  
  class Meta:
    model = Comment
    fields = ('id',
              'post',
              'user',
              'text',
              'post_title',
              'created_date')
    read_only_fields = ['user', 'created_at']
    
  def get_post_title(self, obj):
    return obj.post.title
  
  def create(self, validated_data):
    return super().create(validated_data)

  def update(self, instance, validated_data):
    instance.text = validated_data.get('text', instance.text)
    instance.save()
    return instance
  
 
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