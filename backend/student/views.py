from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import *
import logging

class StudentGetPostAPIView(APIView):
    # 학생 조회
    @swagger_auto_schema(operation_id='학생 조회(이름/아이디)', operation_description='학생을 이름 혹은 아이디로 조회합니다.', tags=['Student'],
                    manual_parameters=[
                        openapi.Parameter('id', openapi.IN_QUERY, description="User ID", type=openapi.TYPE_INTEGER),
                        openapi.Parameter('student_id', openapi.IN_QUERY, description="Student ID", type=openapi.TYPE_INTEGER),
                        openapi.Parameter('name', openapi.IN_QUERY, description="Student Name", type=openapi.TYPE_STRING),
                    ])
    def get(self, request):
        # 쿼리 매개변수 가져오기
        user_id = request.GET.get('id', '')
        student_id = request.GET.get('student_id', '')
        student_name = request.GET.get('name', '')

        students = None
        try:
            # 데이터베이스 조회
            if student_id:
                students = Student.objects.filter(id=student_id)
            elif student_name:
                students = Student.objects.filter(name=student_name)
            else:
                return Response({'message': '학생 아이디 혹은 학생 이름을 입력해주세요.'}, 
                status=status.HTTP_400_BAD_REQUEST)

            # 결과 직렬화
            serialized_students = StudentSerializer(students, many=True).data

            # if serialized_students.is_valid():
            for student in serialized_students:
                feedbacks = Feedback.objects.filter(user_id = user_id, student_id = student['id'])
                student['isFeedback'] = feedbacks.exists()

            return Response({
                'message': '학생이 조회되었습니다.',
                'data': serialized_students
            }, status=status.HTTP_200_OK)

            # return Response({
            #     'message': '유효하지 않은 입력값입니다.',
            #     'data': serialized_students.errors
            # }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'message': '오류가 발생했습니다. ({})'.format(str(e)),
                'data': []
            }, status=status.HTTP_400_BAD_REQUEST)

    # 학생 등록
    @swagger_auto_schema(tags=['Student'],
                    request_body=StudentRegisterSerializer, query_serializer=StudentRegisterSerializer)
    def post(self, request):
        try:
            # body 데이터 serializer
            serialized_student = StudentRegisterSerializer(data=request.data)

            if serialized_student.is_valid():
                serialized_student.save()
                # 로깅
                logging.info(serialized_student.data)
                return Response({
                    'message': '학생이 등록되었습니다.',
                    'student_id': serialized_student.instance.pk
                }, status=status.HTTP_200_OK)
            
            return Response({
                'message': '유효하지 않은 입력값입니다.',
                'data': serialized_student.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'message': '오류가 발생했습니다. ({})'.format(str(e)),
                'data': []
            }, status=status.HTTP_400_BAD_REQUEST)


class ScoreGetPostAPIView(APIView):
    # 성적 조회
    def get(self, request, student_id):
        # 쿼리 매개변수 가져오기
        subject_id = request.GET.get('subject_id', '')
        scores = None
        try:
            # 데이터베이스 조회
            if subject_id:
                scores = StudentScore.objects.filter(student_id=student_id,subject_id=subject_id)
            else:
                scores = StudentScore.objects.filter(student_id=student_id)

            # 결과 직렬화
            serialized_scores = ScoreSerializer(scores, many=True)

            # if serialized_scores.is_valid():
            return Response({
                'message': '학생 성적이 조회되었습니다.',
                'data': serialized_scores.data
            }, status=status.HTTP_200_OK)
            
            # return Response({
            #     'message': '입력이 올바르지 않습니다.',
            #     'data': []
            # }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'message': '오류가 발생했습니다. ({})'.format(str(e)),
                'data': []
            }, status=status.HTTP_400_BAD_REQUEST)

    # 성적 등록
    def post(self, request, student_id):
        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return Response({"detail": "존재하지 않는 학생입니다."}, status=status.HTTP_404_NOT_FOUND)

        try:
            # body 데이터 serializer
            serialized_scores = ScoretRegisterSerializer(data=request.data, many=True)

            if serialized_scores.is_valid():
                # 모든 객체에 student_id를 추가
                for score in serialized_scores.validated_data:
                    score['student_id'] = student

                # 데이터베이스에 저장
                serialized_scores.save()

                return Response({
                    'message': '학생 성적이 등록되었습니다.',
                    'data': serialized_scores.data
                }, status=status.HTTP_200_OK)

            return Response({
                'message': '입력이 올바르지 않습니다.',
                'data': []
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'message': '오류가 발생했습니다. ({})'.format(str(e)),
                'data': []
            }, status=status.HTTP_400_BAD_REQUEST)