from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserRegisterSerializer, UserLoginSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import User

# Create your views here.

class UserRegister(APIView):

    def post(self, request):

        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            message = {
                "message": "회원가입 성공"
            }
            return Response(message, status=status.HTTP_200_OK)
        message = {
                "message": "회원가입 실패"
            }
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
       
        
class UserLogin(APIView):

    def post(self, request):
        input_email = request.data['email']
        input_password = request.data['password']
        
        user = User.objects.get(email=input_email)
        if input_password == user.password:
            message = {
                "message": "로그인 성공",
                "user_id": user.id
            }
            return Response(message, status=status.HTTP_200_OK)
        message = {
            "message": "로그인 실패"
        }
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    
class UserLogout(APIView):

    def delete(self, request):
        request.session.flush()
        message = {
            "message": "로그아웃 성공"
        }
        return Response(message, status=status.HTTP_200_OK)
    
