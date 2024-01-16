from .models import User, Favorite
from rest_framework import serializers

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','name','password','phone','academy_id','birth','role']

class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','name']

class UserMemoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'memo']

class UserFavoriteGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['student_id']

class UserFavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'