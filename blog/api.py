from rest_framework.response import Response
from rest_framework import generics, status, permissions, serializers
from rest_framework.exceptions import NotFound
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

class CreatePostAPI(generics.CreateAPIView):
  queryset = Post.objects.all()
  serializer_class = PostSerializer
  permission_classes = [permissions.IsAuthenticated]

  def perform_create(self, serializer):
    serializer.save(user=self.request.user)
    
    
class UpdatePostAPI(generics.UpdateAPIView):
  queryset = Post.objects.all()
  serializer_class = PostSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_queryset(self):
    return self.queryset.filter(user=self.request.user)


class DeletePostAPI(generics.DestroyAPIView):
  queryset = Post.objects.all()
  serializer_class = PostSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_queryset(self):
    return self.queryset.filter(user=self.request.user)

  def destroy(self, request, *args, **kwargs):
    try:
      response = super().destroy(request, *args, **kwargs)
      return response
    except Exception as e:
      return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    
class CreateCommentAPI(generics.CreateAPIView):
  queryset = Comment.objects.all()
  serializer_class = CommentSerializer
  permission_classes = [permissions.IsAuthenticated]

  def perform_create(self, serializer):
    post_id = self.request.data.get('post')
    
    try:
      post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
      raise serializers.ValidationError("Post matching query does not exist.")

    serializer.save(post=post, user=self.request.user)

  
class UpdateCommentAPI(generics.UpdateAPIView):
  queryset = Comment.objects.all()
  serializer_class = CommentSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_object(self):
    comment_id = self.kwargs.get('comment_id')

    try:
      comment = Comment.objects.get(id=comment_id)

      if comment.user != self.request.user:
        raise permissions.PermissionDenied("You cannot edit this comment.")
      return comment
    except Comment.DoesNotExist:
      raise NotFound("Comment matching query does not exist.")

  def perform_update(self, serializer):
    serializer.save()


class DeleteCommentAPI(generics.DestroyAPIView):
  queryset = Comment.objects.all()
  permission_classes = [permissions.IsAuthenticated]

  def get_object(self):
    comment_id = self.kwargs.get('comment_id')

    try:
      comment = Comment.objects.get(id=comment_id)

      if comment.user != self.request.user:
        raise permissions.PermissionDenied("You cannot delete this comment.")
      return comment
    except Comment.DoesNotExist:
      raise NotFound("Comment matching query does not exist.")

  def perform_destroy(self, instance):
    instance.delete()
