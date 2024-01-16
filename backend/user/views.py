from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserMemoSerializer, UserFavoriteSerializer, UserFavoriteGetSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import User, Favorite
from student.models import Student

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorator import api_view

# Create your views here.

class UserRegister(APIView):

    @swagger_auto_schema(
        summary="새로운 회원 등록",
        tags=["User"],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'academy_id': openapi.Schema(type=openapi.TYPE_STRING, description='학원아이디'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='이메일'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='비밀번호'),
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='회원 이름'),
                'phone': openapi.Schema(type=openapi.TYPE_STRING, description='학생 전화번호'),
                'birth': openapi.Schema(type=openapi.TYPE_STRING, description='생년'),
                'role': openapi.Schema(type=openapi.TYPE_STRING, description='강사/컨설턴트'),
                'created_at': openapi.Schema(type=openapi.TYPE_STRING, description='생성날짜'),
                'updated_at': openapi.Schema(type=openapi.TYPE_STRING, description='수정날짜'),
                'deleted_at': openapi.Schema(type=openapi.TYPE_STRING, description='삭제날짜'),
            },
            required=['email','name','password','phone','academy_id','birth','role']
        ),
        description="새로운 회원을 등록합니다",
    )
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
       
@swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['email', 'password']
        ),)
class UserLogin(APIView):

    @swagger_auto_schema(
        summary="로그인",
        tags=["User"],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='이메일'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='비밀번호'),
            },
            required=['email','password']
        ),
        description="로그인합니다",
    )
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

    @swagger_auto_schema(
            summary="로그아웃",
            tags=["User"],
            responses={
                200: openapi.Response(
                    description="로그아웃 성공",
                    examples={
                        'application/json': {"message": "로그아웃 성공"}
                    }
                ),
            }
        )
    def delete(self, request):
        request.session.flush()
        message = {
            "message": "로그아웃 성공"
        }
        return Response(message, status=status.HTTP_200_OK)
    
class MemoUpdate(APIView):
    @swagger_auto_schema(
        summary="회원이 작성한 메모 수정",
        tags=["User"],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='유저 아이디'),
                'memo': openapi.Schema(type=openapi.TYPE_INTEGER, description='메모 내용'),
            },
            required=['id'],
        ),
        description="회원이 작성한 메모를 수정합니다.",
    )
    def put(self, request):
        try:
            user = User.objects.get(id=request.data['id'])
        except User.DoesNotExist:
            return Response({"message": "존재하지 않는 회원입니다."}, status=status.HTTP_400_BAD_REQUEST)

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

class FavoriteGetAPIView(APIView):
    #즐겨찾기 목록 조회
    @swagger_auto_schema(
        summary="회원이 즐겨찾기 한 학생 목록 조회",
        tags=["User"],
        manual_parameters=[
            openapi.Parameter('user_id', in_=openapi.IN_PATH, type=openapi.TYPE_INTEGER, description='회원 ID')
        ],
        description="회원이 즐겨찾기 한 학생의 목록을 조회합니다.",
    )
    def get(self, request, user_id):
        try:
            favoriteList = Favorite.objects.filter(user_id=user_id)
            serialized_favorites = UserFavoriteGetSerializer(favoriteList, many=True)

            for favorite in serialized_favorites.data:
                student = Student.objects.get(id = favorite['student_id'])
                favorite['student_name'] = student.name

            return Response({
                'message': '즐겨찾기가 조회되었습니다.',
                'result': serialized_favorites.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'message': '오류가 발생했습니다. ({})'.format(str(e)),
            }, status=status.HTTP_400_BAD_REQUEST)


class FavoriteAPIView(APIView):
    #즐겨찾기 등록
    @swagger_auto_schema(
        summary="즐겨찾기 등록",
        tags=["User"],
        description="즐겨찾기를 합니다.",
    )
    def post(self, request, user_id, student_id):
        try:
            favorite = Favorite.objects.filter(user_id=user_id, student_id=student_id)
            if favorite:
                return Response({
                    'message': '이미 즐겨찾기를 했습니다.',
                }, status=status.HTTP_400_BAD_REQUEST)

            data = request.data
            data['user_id'] = user_id
            data['student_id'] = student_id
            serialized_favorite = UserFavoriteSerializer(data=data)

            if serialized_favorite.is_valid():
                serialized_favorite.save()
                return Response({
                    'message': '즐겨찾기가 되었습니다.',
                    'result': serialized_favorite.data
                }, status=status.HTTP_200_OK)

            return Response({
                'message': '유효하지 않은 입력값입니다.',
                'result': serialized_favorite.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'message': '오류가 발생했습니다. ({})'.format(str(e)),
            }, status=status.HTTP_400_BAD_REQUEST)

    #즐겨찾기 취소
    @swagger_auto_schema(
        summary="즐겨찾기 취소",
        tags=["User"],
        manual_parameters=[
            openapi.Parameter('user_id', in_=openapi.IN_PATH, type=openapi.TYPE_INTEGER, description='회원 ID'),
            openapi.Parameter('student_id', in_=openapi.IN_PATH, type=openapi.TYPE_INTEGER, student_id='학생 ID'),
        ],
        description="즐겨찾기를 취소합니다.",
    )
    def delete(self, request, user_id, student_id):
        try:
            favorite = Favorite.objects.get(user_id=user_id, student_id=student_id)
        except Favorite.DoesNotExist:
            return Response({"message": "존재하지 않는 즐겨찾기입니다."}, status=status.HTTP_400_BAD_REQUEST)

        favorite.delete()
        
        return Response({
            'message': '즐겨찾기가 취소되었습니다.'
        }, status=status.HTTP_200_OK)