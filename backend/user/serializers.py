from .models import User
from rest_framework import serializers

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','name','password','phone','academy_id','birth','role']

class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','name']