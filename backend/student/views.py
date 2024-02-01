# from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from user.models import User

from .serializers import *


class StudentGetPostAPIView(APIView):
    # 학생 조회
    @swagger_auto_schema(
        summary="학생 아이디 혹은 검색어(이름/학교)로 학생 정보 및 피드백 여부 조회",
        tags=["Student"],
        manual_parameters=[
            openapi.Parameter('id', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='회원 ID'),
            openapi.Parameter('student_id', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='학생 ID (선택)'),
            openapi.Parameter('search', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description='검색어 (선택)'),
        ],
        description="학생 아이디 혹은 검색어(이름/학교)로 학생 정보를 조회하고 해당 학생에 대한 피드백 여부를 확인합니다.",
    )
    def get(self, request):
        user_id = request.GET.get('id', '')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'message': '존재하지 않는 회원입니다.'}, status=status.HTTP_400_BAD_REQUEST)

        student_id = request.GET.get('student_id', '')
        search = request.GET.get('search', '')

        students = None
        try:
            if student_id:
                students = Student.objects.filter(id=student_id)
            elif search:
                students = Student.objects.filter(Q(name__icontains=search)|Q(school__icontains=search)).distinct()
            else:
                students = Student.objects.filter()

            serialized_students = StudentSerializer(students, many=True).data

            for student in serialized_students:
                feedbacks = Feedback.objects.filter(user_id = user_id, student_id = student['id'])
                student['isFeedback'] = feedbacks.exists()

            return Response({
                'message': '학생이 조회되었습니다.',
                'result': serialized_students
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'message': '오류가 발생했습니다. ({})'.format(str(e)),
            }, status=status.HTTP_400_BAD_REQUEST)

    # 학생 등록
    @swagger_auto_schema(
        summary="새로운 학생 등록",
        tags=["Student"],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'academy_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='학원아이디'),
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='학생 이름'),
                'birth': openapi.Schema(type=openapi.TYPE_STRING, description='생년'),
                'phone': openapi.Schema(type=openapi.TYPE_STRING, description='학생 전화번호'),
                'school': openapi.Schema(type=openapi.TYPE_STRING, description='학교'),
                'grade': openapi.Schema(type=openapi.TYPE_STRING, description='학년'),
                'parent_name': openapi.Schema(type=openapi.TYPE_STRING, description='부모님 성함'),
                'parent_phone': openapi.Schema(type=openapi.TYPE_STRING, description='부모님 전화번호'),
            },
            required=['academy_id','name','birth','school','grade','parent_name','parent_phone'],
        ),
        description="새로운 학생을 등록합니다.",
    )
    def post(self, request):
        try:
            serialized_student = StudentRegisterSerializer(data=request.data)

            if serialized_student.is_valid():
                serialized_student.save()
                return Response({
                    'message': '학생이 등록되었습니다.',
                    'result': serialized_student.data
                }, status=status.HTTP_200_OK)
            
            return Response({
                'message': '유효하지 않은 입력값입니다.',
                'result': serialized_student.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'message': '오류가 발생했습니다. ({})'.format(str(e)),
            }, status=status.HTTP_400_BAD_REQUEST)


class ScoreGetPostAPIView(APIView):
    # 성적 조회
    @swagger_auto_schema(
        summary="학생 성적 조회",
        tags=["Student"],
        manual_parameters=[
            openapi.Parameter('student_id', in_=openapi.IN_PATH, type=openapi.TYPE_INTEGER, description='학생 ID'),
            openapi.Parameter('subject_id', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='과목 ID (선택)'),
        ],
        description="특정 학생의 성적을 (과목별로) 조회합니다.",
    )
    def get(self, request, student_id):
        subject_id = request.GET.get('subject_id', '')
        scores = None
        try:
            if subject_id:
                scores = StudentScore.objects.filter(student_id=student_id,subject_id=subject_id)
            else:
                scores = StudentScore.objects.filter(student_id=student_id)

            serialized_scores = ScoreSerializer(scores, many=True)

            return Response({
                'message': '학생 성적이 조회되었습니다.',
                'result': serialized_scores.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'message': '오류가 발생했습니다. ({})'.format(str(e))
            }, status=status.HTTP_400_BAD_REQUEST)

    # 성적 등록
    @swagger_auto_schema(
        summary="학생 성적 등록",
        tags=["Student"],
        manual_parameters=[
            openapi.Parameter('student_id', in_=openapi.IN_PATH, type=openapi.TYPE_INTEGER, description='학생 ID'),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'scoreList': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'subject_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='과목 아이디'),
                            'exam_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='시험 아이디'),
                            'type': openapi.Schema(type=openapi.TYPE_STRING, description='구분(상대/절대)'),
                            'score': openapi.Schema(type=openapi.TYPE_INTEGER, description='성적'),
                            'grade': openapi.Schema(type=openapi.TYPE_STRING, description='학년'),
                        },
                        required=['subject_id', 'exam_id', 'type', 'score', 'grade'],
                    ),
                ),
            },
            required=['scoreList'],
        ),
        description="학생의 성적을 등록합니다.",
    )
    def post(self, request, student_id):
        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return Response({"message": "존재하지 않는 학생입니다."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            scoreList = request.data.get('scoreList', [])
            for num in range(len(scoreList)):
                getScore = StudentScore.objects.filter(student_id=student_id,subject_id=scoreList[num]['subject_id'], exam_id=scoreList[num]['exam_id'], grade=scoreList[num]['grade'])
                if(getScore):
                    scoreList[num]['score'] = scoreList[num]['score']
                    scoreList[num]['id'] = getScore[0].id

            serialized_scores = ScoretRegisterSerializer(data=scoreList, many=True)

            if serialized_scores.is_valid():
                for score in serialized_scores.validated_data:
                    score['student_id'] = student
                    subject_id = score['subject_id']
                    exam_id = score['exam_id']
                    grade = score['grade']
                    defaults = {'score': score['score']}

                    obj, created = StudentScore.objects.update_or_create(
                        student_id=student,
                        subject_id=subject_id,
                        exam_id=exam_id,
                        grade=grade,
                        defaults=defaults
                    )

                    # 업데이트된 객체의 id를 저장합니다.
                    score['id'] = obj.id

                return Response({
                    'message': '학생 성적이 등록되었습니다.',
                    'result': serialized_scores.data
                }, status=status.HTTP_200_OK)

            return Response({
                'message': '입력이 올바르지 않습니다.'
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'message': '오류가 발생했습니다. ({})'.format(str(e))
            }, status=status.HTTP_400_BAD_REQUEST)