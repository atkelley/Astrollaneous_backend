from django.contrib.auth import authenticate, logout
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer
  

class UserAPI(generics.RetrieveAPIView):
  permission_classes = [permissions.IsAuthenticated,]
  serializer_class = UserSerializer

  def get_object(self):
    return self.request.user  


class RegisterAPI(generics.GenericAPIView):
  serializer_class = RegisterSerializer

  def post(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    return Response({
      "user": UserSerializer(user, context=self.get_serializer_context()).data,
      "token": AuthToken.objects.create(user)[1]
    })


class LoginAPI(generics.GenericAPIView):
  serializer_class = LoginSerializer

  def post(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data
    _, token = AuthToken.objects.create(user)
    return Response({
      "user": UserSerializer(user, context=self.get_serializer_context()).data,
      "token": token
    })
  
    
class LogoutAPI(APIView):
  def post(self, request):
    logout(request)
    return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
