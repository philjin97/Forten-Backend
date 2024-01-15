from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserMemoSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import User

# Create your views here.

class UserRegister(APIView):

    def post(self, request):
        try: 
            user = User.objects.get(email=request.data['email'])
            return Response({'message': '존재하는 이메일입니다.'}, 
                    status=status.HTTP_400_BAD_REQUEST) 

        except User.DoesNotExist:       
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
                "user_id": user.id,
                "user_name": user.name,
		        "role": user.role,
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
    
class MemoUpdate(APIView):

    def put(self, request):
        try:
            user = User.objects.get(id=request.data['id'])
        except User.DoesNotExist:
            return Response({"message": "존재하지 않는 회원입니다."}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserMemoSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': '메모가 수정되었습니다.',
                'result': serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            'message': '유효하지 않은 입력값입니다.',
            'result': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)