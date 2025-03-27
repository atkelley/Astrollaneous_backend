from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .serializers import UserSerializer
from blog.serializers import PostSerializer, CommentSerializer
from blog.models import Post, Comment


@api_view(['GET'])
def get_users(request):
  if request.method == 'GET':
    try:
      data = User.objects.all()
      serializer = UserSerializer(data, context={'request': request}, many=True)
      return Response(serializer.data)
    except User.DoesNotExist: 
      return JsonResponse({'error': 'Users not found.'}, status=status.HTTP_404_NOT_FOUND)
    

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
    

@api_view(['DELETE'])  
def delete_user(request, id):
  if request.method == 'DELETE':
    try:
      user = User.objects.get(pk=id)
    except User.DoesNotExist:
      return False  

    Comment.objects.filter(user=user).delete()
    Post.objects.filter(author=user).delete()
    user.delete()
    return True