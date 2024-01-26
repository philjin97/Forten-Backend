from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from student.models import StudentScore
from feedback.models import Feedback
from user.models import User
from .serializers import StudentScoreSerializer
from openai import OpenAI
from backend.my_settings import openai_secret_key
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
# from analysis.models import TemporaryPrompt
from django.core.cache import cache
# from analysis.tasks import prompt_task
from django.shortcuts import render
from xhtml2pdf import pisa
from django.http import HttpResponse
from student.models import Student
from io import BytesIO


# Create your views here.

class Rating(APIView):

    @swagger_auto_schema(
        summary="학생 평가 조회",
        tags=["Feedback"],
        manual_parameters=[
            openapi.Parameter('student_id', in_=openapi.IN_PATH, type=openapi.TYPE_INTEGER, description='학생 ID'),
        ],
        description="특정 학생의 평가를 모두 조회합니다",
    )
    def get(self, request, student_id):
        try:
            student = Feedback.objects.filter(student_id=student_id)

            student_ratings = []
            feedback_user_name = []

            for student_feedback in student:
                student_ratings.append(student_feedback.student_rating) 

                user_name = student_feedback.user_id.name
                feedback_user_name.append(user_name)
            
            avg_parent_rating = 0
            cnt = 0

            for student_feedback in student:
                if student_feedback.parent_rating:
                    avg_parent_rating += student_feedback.parent_rating 
                    cnt += 1
                else:
                    continue
            
            avg_parent_rating = avg_parent_rating//cnt

            message = {
                "message": "평가 조회 성공",
                "result": {
                    "student_rating": student_ratings,
                    "feedback_user_name": feedback_user_name,
                    "parent_rating": avg_parent_rating
                }
            }

            return Response(message, status.HTTP_200_OK)
        except:
            message = {
                "message": "평가 조회 실패"
            }
            return Response(message, status.HTTP_400_BAD_REQUEST)
# 하나로

# class Score(APIView):

#     def get(self, request, student_id, subject_id):
#         subject_scores = Student_score.objects.filter(student_id=student_id).filter(subject_id=subject_id)

#         serializer = StudentScoreSerializer(subject_scores, many=True)

#         return Response(serializer.data, status.HTTP_200_OK)
    
# student/ ScoreGetPostAPIView

class Prompt(APIView):

    @swagger_auto_schema(
        summary="학생 프롬프트 조회",
        tags=["Feedback"],
        manual_parameters=[
            openapi.Parameter('student_id', in_=openapi.IN_PATH, type=openapi.TYPE_INTEGER, description='학생 ID'),
        ],
        description="특정 학생의 평가를 ChatGPT를 통해 요약합니다.",
    )
    def get(self, request, student_id):

        if  cache.get(student_id) == None:

            feedbacks = Feedback.objects.filter(student_id=student_id)

            feedbacks_content = ''
            for feedback in feedbacks:
                feedbacks_content += feedback.content

            client = openai_secret_key

            response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "학부모를 설득해봐."},
                {"role": "user", "content": f"{feedbacks_content}"}
            ]
            )
            response = response.choices[0].message.content
            cache.set(student_id, response, 60 * 60)

            message = {
                "response": response
            }
            
            return Response(message, status.HTTP_200_OK) 

        else:
            prompt = cache.get(student_id)
            message = {
                "response": prompt
            }
            return Response(message, status.HTTP_200_OK)
    
        # 비동기로 미리 저장된 데이터 확인
        # 캐시를 스캔
        # temporary = TemporaryPrompt.objects.filter(student_id=student_id)
        # if len(temporary) != 0:
        #     message = {
        #     "response": temporary[0].prompt
        #     }
            # return Response(message, status.HTTP_200_OK) 
        
        # 없으면 생성
    
    # def post(self, request, student_id):
    #     student_name = Student.objects.get(id = student_id).name
    #     comment = cache.get(student_id)
    #     # Generate PDF using xhtml2pdf
    #     result = generate_pdf_function(student_name,comment)
    #     response = HttpResponse(content_type='application/pdf')
    #     response['Content-Disposition'] = 'attachment; filename="output.pdf"'
        
    #     pisa.CreatePDF(result.encode('utf-8'), dest=response, encoding=('utf-8'))

    #     return response
    

class PDF(APIView):

    @swagger_auto_schema(
        summary="학생 컨설팅 내용 다운로드",
        tags=["Feedback"],
        manual_parameters=[
            openapi.Parameter('student_id', in_=openapi.IN_PATH, type=openapi.TYPE_INTEGER, description='학생 ID'),
        ],
        description="특정 학생의 컨설팅 내용을 PDF로 다운로드합니다.",
    )
    def get(self, request, student_id):
        student_name = Student.objects.get(id = student_id).name
        comment = cache.get(student_id)
        # Generate PDF using xhtml2pdf
        result = generate_html_function(student_name,comment)
        response = HttpResponse(content_type='application/pdf; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="output.pdf"'
        
        pisa.CreatePDF(result, dest=response, encoding=('utf-8'))

        return response


def generate_html_function(student_name, comment):
# Write your PDF generation code here
    html_content = '<html><head><meta charset="UTF-8" /><style>'
    html_content += 'body { font-family: HYGothic-Medium '
    html_content += '}</style></head><body>'
    html_content += '<h1>Student Name: ' + student_name + '</h1>'   
    html_content += '<p>Comments' + comment + '</p>'
    html_content += '</body></html>'
    return html_content