from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken
import re

class UserSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True)
  password2 = serializers.CharField(write_only=True)

  class Meta:
    model = User
    fields = ['email', 'name', 'password', 'password2']
    
    def validate_email(self, value):
      if User.objects.filter(email=value).exists():
        raise serializers.ValidationError("Email already exists")
      email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
      if not re.match(email_regex, value):
        raise serializers.ValidationError('Enter a valid email address.')
      return value

    def validate(self, data):
      if data['password'] != data['password2']:
          raise serializers.ValidationError("Passwords do not match")
      return data

  def create(self, validated_data):
    validated_data.pop('password2')
    user = User.objects.create_user(
      email=validated_data['email'],
      name=validated_data['name'],
      password=validated_data['password']
    )
    return user

class ThirdPartyUserSerializer(serializers.Serializer):
  name = serializers.CharField()
  email = serializers.EmailField()
  
class SignInSerializer(serializers.Serializer):
  email = serializers.EmailField()
  password = serializers.CharField(write_only=True)
  
  def validate_email(self, value):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, value):
        raise serializers.ValidationError('Enter a valid email address.')
    return value

  def validate(self, data):
    email = data.get('email')
    password = data.get('password')
    print('the data is', data)
    if email and password:
      user = authenticate(request=self.context.get('request'), email=email, password=password)
      if not user:
        raise serializers.ValidationError('Invalid credentials')
    else:
      raise serializers.ValidationError('Must include "email" and "password"')

    data['user'] = user
    return data
  
class ListUserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'email', 'name', 'is_admin']
    
class AccessTokenSerializer(serializers.Serializer):
  token = serializers.CharField()

  def validate_token(self, value):
    try:
      access_token = AccessToken(value)
      user_id = access_token['user_id']
      user = User.objects.get(id=user_id)
    except Exception as e:
      raise serializers.ValidationError('Invalid token')
    return value

  def get_user(self):
    token = self.validated_data['token']
    access_token = AccessToken(token)
    user_id = access_token['user_id']
    user = User.objects.get(id=user_id)
    return user
  