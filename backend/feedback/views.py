from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import *
import logging

# Create your views here.
class FeedbackGetPostAPIView(APIView):
    # 평가 조회
    def get(self, request, user_id):
        try:
            feedback_list = Feedback.objects.filter(user_id=user_id)
            serialized_feedbacks = FeedbackSerializer(feedback_list, many=True)

            return Response({
                'message': '평가가 조회되었습니다.',
                'result': serialized_feedbacks.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'message': '오류가 발생했습니다. ({})'.format(str(e)),
            }, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(tags=['Student'],
                    request_body=FeedbackRegisterSerializer, query_serializer=FeedbackRegisterSerializer)
    # 평가 등록
    def post(self, request, user_id):
        try:
            data = request.data
            data['user_id'] = user_id  # 추가: 등록한 사용자의 ID
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
    def put(self, request, user_id, feedback_id):
        try:
            feedback = Feedback.objects.get(user_id=user_id, id=feedback_id)
        except Feedback.DoesNotExist:
            return Response({"message": "존재하지 않는 평가입니다."}, status=status.HTTP_404_NOT_FOUND)

        serialized_feedback = FeedbackSerializer(feedback, data=request.data)
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
    def delete(self, request, user_id, feedback_id):
        try:
            feedback = Feedback.objects.get(user_id=user_id, id=feedback_id)
        except Feedback.DoesNotExist:
            return Response({"message": "존재하지 않는 평가입니다."}, status=status.HTTP_404_NOT_FOUND)

        feedback.delete()
        
        return Response({
            'message': '평가가 삭제되었습니다.'
        }, status=status.HTTP_200_OK)
