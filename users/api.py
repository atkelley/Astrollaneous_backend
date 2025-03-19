from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, logout

class LoginView(APIView):
  def post(self, request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    
    if user is not None:
      refresh = RefreshToken.for_user(user)
      return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
      }, status=status.HTTP_200_OK)
    else:
      return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
    
class LogoutAPI(APIView):
  def post(self, request):
    logout(request)
    return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)


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


class UserAPI(generics.RetrieveAPIView):
  permission_classes = [permissions.IsAuthenticated,]
  serializer_class = UserSerializer

  def get_object(self):
    return self.request.user
