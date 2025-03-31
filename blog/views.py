from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework import status

from .serializers import PostSerializer, CommentSerializer
from .models import Post, Comment


# POSTS ###################################################################################
@api_view(['GET'])
def get_post(request, id):
  try:
    post = Post.objects.get(id=id)
    serializer = PostSerializer(post)
    return Response(serializer.data, status=status.HTTP_200_OK)
  except Post.DoesNotExist:
    return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_posts(request):
  if request.method == 'GET':
    try:
      data = Post.objects.all().order_by('-created_date') 
      serializer = PostSerializer(data, context={'request': request}, many=True)
      return Response(serializer.data)
    except Post.DoesNotExist: 
      return JsonResponse({'error': 'Posts not found.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def create_post(request):
  if request.method == 'POST':
    try:
      data = JSONParser().parse(request)
      title = data.get('title')
      text = data.get('text')
      image_url = data.get('image_url')
      user_data = data.get('user')
      user = User.objects.get(id=user_data.get('id'))
      post = Post(title=title, text=text, image_url=image_url, user=user)
      post.save()
      return JsonResponse(PostSerializer(post).data, status=201) 
    except ParseError:
        return JsonResponse({'error': 'Post could not be created.'}, status=status.HTTP_400_BAD_REQUEST)

  
@api_view(['PUT'])
def update_post(request, id):
  try:
    post = Post.objects.get(id=id)
    serializer = PostSerializer(post, data=request.data)
    if serializer.is_valid():
      updated_post = serializer.save()
      return JsonResponse(PostSerializer(updated_post).data, safe=False)  

    return JsonResponse(serializer.errors, status=400)

  except Post.DoesNotExist:
    return JsonResponse({"error": "Post not found"}, status=404)
  

@api_view(['DELETE'])
def delete_post(request, id):
  try:
    Post.objects.filter(id=id).delete()
    return HttpResponse(status=200)
  except Exception as e:
    return HttpResponse(e, status=status.HTTP_400_BAD_REQUEST)


# COMMENTS #################################################################################
@api_view(['POST'])
def create_comment(request, id):
  try:
    post = Post.objects.get(id=id)
  except Post.DoesNotExist:
    return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

  request.data['post'] = post.id  

  serializer = CommentSerializer(data=request.data)
  if serializer.is_valid():
    serializer.save()  # Save the comment
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  else:
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_comment(request, id):
  try:
    comment = Comment.objects.get(id=id)
  except Comment.DoesNotExist:
    return Response({"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)

  serializer = CommentSerializer(comment, data=request.data, partial=True) 
  if serializer.is_valid():
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)
  else:
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


@api_view(['DELETE'])
def delete_comment(request, id):
  try:
    Comment.objects.filter(id=id).delete()
    return HttpResponse(status=200)
  except Exception as e:
    return HttpResponse(e, status=status.HTTP_400_BAD_REQUEST)


# USER ##################################################################################
@api_view(['GET'])
def get_user(request, id):
  if request.method == 'GET':
    try:
      user_data = User.objects.get(id=id)
      user = serializers.serialize('python', [user_data,])
      return Response(user)
    except User.DoesNotExist: 
      return JsonResponse({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def user_posts(request, id):
  if request.method == 'GET':
    try:
      user = User.objects.get(id=id)
      data = Post.objects.filter(user=user)
      serializer = PostSerializer(data, context={'request': request}, many=True)
      return Response(serializer.data)
    except Post.DoesNotExist: 
      return JsonResponse({'error': 'Posts not found.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def user_comments(request, id):
  if request.method == 'GET':
    try:
      user = User.objects.get(id=id)
      data = Comment.objects.filter(user=user)
      serializer = CommentSerializer(data, context={'request': request}, many=True)
      return Response(serializer.data)
    except Comment.DoesNotExist: 
      return JsonResponse({'error': 'Comments not found.'}, status=status.HTTP_404_NOT_FOUND)

