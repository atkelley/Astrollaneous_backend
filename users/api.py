from django.contrib.auth import authenticate, login
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from knox.models import AuthToken
from knox.auth import TokenAuthentication
from .serializers import RegisterSerializer


class UserAPI(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [permissions.IsAuthenticated]

  def get(self, request):
    user = request.user
    return Response({
      "id": user.id,
      "username": user.username,
      "email": user.email,
    })

  
class RegisterAPI(generics.GenericAPIView):
  serializer_class = RegisterSerializer

  def post(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    return Response({
      "user": {
        "id": user.id,
        "username": user.username,
        "email": user.email,
      },
      "token": AuthToken.objects.create(user)[1]
    })
  

class LoginAPI(APIView):
  def post(self, request, format=None):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)

    if user is None:
      raise AuthenticationFailed("Invalid credentials")

    login(request, user)
    token = AuthToken.objects.create(user)[1]

    return Response({
      "user": {
        "id": user.id,
        "username": user.username,
        "email": user.email,
      },
      "token": token,
    })


# class LoginAPI(generics.GenericAPIView):
#   serializer_class = LoginSerializer

#   def post(self, request, *args, **kwargs):
#     serializer = self.get_serializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     user = serializer.validated_data
#     _, token = AuthToken.objects.create(user)
#     return Response({
#       "user": UserSerializer(user, context=self.get_serializer_context()).data,
#       "token": token
#     })
  
    
# class LogoutAPI(APIView):
#   def post(self, request):
#     logout(request)
#     return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
