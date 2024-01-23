from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import *
import logging

# Create your views here.
class FeedbackGetAPIView(APIView):
    # 평가 조회
    @swagger_auto_schema(
        summary="특정 학생에 대한 회원이 작성한 피드백 조회",
        tags=["Feedback"],
        manual_parameters=[
            openapi.Parameter('user_id', in_=openapi.IN_PATH, type=openapi.TYPE_INTEGER, description='회원 ID'),
            openapi.Parameter('student_id', in_=openapi.IN_PATH, type=openapi.TYPE_INTEGER, description='학생 ID'),
        ],
        description="특정 학생에 대한 회원이 작성한 피드백 조회합니다.",
    )
    def get(self, request, user_id, student_id):
        try:
            feedback_list = Feedback.objects.filter(user_id=user_id, student_id=student_id)
            serialized_feedbacks = FeedbackSerializer(feedback_list, many=True)

            return Response({
                'message': '평가가 조회되었습니다.',
                'result': serialized_feedbacks.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'message': '오류가 발생했습니다. ({})'.format(str(e)),
            }, status=status.HTTP_400_BAD_REQUEST)

class FeedbackRegisterAPIView(APIView):
    # 평가 등록
    @swagger_auto_schema(
        summary="학생에 대한 새로운 평가 등록",
        tags=["Feedback"],
        manual_parameters=[
            openapi.Parameter('user_id', in_=openapi.IN_PATH, type=openapi.TYPE_INTEGER, description='회원 ID'),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'student_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='학생 아이디'),
                'student_rating': openapi.Schema(type=openapi.TYPE_INTEGER, description='학생 만족도'),
                'parent_rating': openapi.Schema(type=openapi.TYPE_INTEGER, description='부모 만족도'),
                'content': openapi.Schema(type=openapi.TYPE_STRING, description='평가 내용'),
            },
            required=['student_id'],
        ),
        description="학생에 대한 평가를 등록합니다.(컨설턴트가 평가시 부모평가 추가)",
    )
    def post(self, request, user_id):
        try:
            data = request.data
            data['user_id'] = user_id  # 추가: 등록한 회원의 ID
            serialized_feedback = FeedbackRegisterSerializer(data=data)

            if serialized_feedback.is_valid():
                serialized_feedback.save()
                return Response({
                    'message': '평가가 등록되었습니다.',
                    'result': serialized_feedback.data
                }, status=status.HTTP_200_OK)

            return Response({
                'message': '유효하지 않은 입력값입니다.',
                'result': serialized_feedback.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'message': '오류가 발생했습니다. ({})'.format(str(e)),
            }, status=status.HTTP_400_BAD_REQUEST)


class FeedbackPutDeleteAPIView(APIView):
    # 평가 수정
    @swagger_auto_schema(
        summary="회원이 작성한 평가 수정",
        tags=["Feedback"],
        manual_parameters=[
            openapi.Parameter('user_id', in_=openapi.IN_PATH, type=openapi.TYPE_INTEGER, description='회원 ID'),
            openapi.Parameter('feedback_id', in_=openapi.IN_PATH, type=openapi.TYPE_INTEGER, description='평가 ID'),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'student_id' : openapi.Schema(type=openapi.TYPE_INTEGER, description='학생 만족도'),
                'student_rating': openapi.Schema(type=openapi.TYPE_INTEGER, description='학생 만족도'),
                'parent_rating': openapi.Schema(type=openapi.TYPE_INTEGER, description='부모 만족도'),
                'content': openapi.Schema(type=openapi.TYPE_STRING, description='평가 내용'),
            },
        ),
        description="회원이 작성한 평가를 수정합니다.",
    )
    def put(self, request, user_id, feedback_id):
        try:
            feedback = Feedback.objects.get(id=feedback_id)
        except Feedback.DoesNotExist:
            return Response({"message": "존재하지 않는 평가입니다."}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data
        data['id'] = feedback_id
        data['user_id'] = user_id

        serialized_feedback = FeedbackRegisterSerializer(feedback, data=data)
        if serialized_feedback.is_valid():
            serialized_feedback.save() # 데이터베이스에 저장
            return Response({
                'message': '평가가 수정되었습니다.',
                'result': serialized_feedback.data
            }, status=status.HTTP_200_OK)

        return Response({
            'message': '유효하지 않은 입력값입니다.',
            'result': serialized_feedback.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    # 평가 삭제
    @swagger_auto_schema(
        summary="회원이 작성한 평가 삭제",
        tags=["Feedback"],
        manual_parameters=[
            openapi.Parameter('user_id', in_=openapi.IN_PATH, type=openapi.TYPE_INTEGER, description='회원 ID'),
            openapi.Parameter('feedback_id', in_=openapi.IN_PATH, type=openapi.TYPE_INTEGER, description='평가 ID'),
        ],
        description="회원이 작성한 평가를 삭제합니다.",
    )
    def delete(self, request, user_id, feedback_id):
        try:
            feedback = Feedback.objects.get(user_id=user_id, id=feedback_id)
        except Feedback.DoesNotExist:
            return Response({"message": "존재하지 않는 평가입니다."}, status=status.HTTP_400_BAD_REQUEST)

        feedback.delete()
        
        return Response({
            'message': '평가가 삭제되었습니다.'
        }, status=status.HTTP_200_OK)
