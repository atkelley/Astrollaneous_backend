from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'username', 'email')






from django.contrib.auth.models import User
from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


# class RegisterSerializer(serializers.ModelSerializer):
#   class Meta:
#     model = User
#     fields = ('id', 'username', 'email', 'password')

#   def to_representation(self, instance):
#     data = super().to_representation(instance)
#     for field, value in data.items():
#       if value is None:
#         raise SomeExceptionHere({field: "This field is required."})
#     return data

#   def create(self, validated_data):
#     user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
#     return user


class LoginSerializer(serializers.Serializer):
  username = serializers.CharField()
  password = serializers.CharField()

  def validate(self, data):
    user = authenticate(**data)
    if user and user.is_active:
      return user
    raise serializers.ValidationError("Please enter a correct username and password. Note that both fields may be case-sensitive.")