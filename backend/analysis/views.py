import os
from datetime import datetime

from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from feedback.models import Feedback
from student.models import Student
# from openai import OpenAI
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from xhtml2pdf import pisa
from rest_framework.parsers import FormParser, MultiPartParser

from backend.my_settings import openai_secret_key

from .tasks import save_prompt_pdf_task

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

class Prompt(APIView):
    parser_classes = (MultiPartParser, FormParser)

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
                    {"role": "system", "content": "학원의 컨설턴트가 되서 학생의 평가를 기반으로 필요한 수업을 추천해주고 수강할 수 있도록 학부모를 설득해봐."},
                    {"role": "user", "content": f"{feedbacks_content}"}
                ]
            )
            response = response.choices[0].message.content

            cache.set(str(student_id)+"_prompt", response, 60 * 60)
            message = {
                "response": response
            }
            
            save_prompt_pdf_task.delay(student_id)

            return Response(message, status.HTTP_200_OK) 

        else:
            prompt = cache.get(str(student_id)+"_prompt")
            message = {
                "response": prompt
            }
            return Response(message, status.HTTP_200_OK)


    @swagger_auto_schema(
        operation_description='Upload file...',
        summary="학생 컨설팅 내용 다운로드",
        tags=["Feedback"],
        manual_parameters=[
            openapi.Parameter('student_id', in_=openapi.IN_PATH, type=openapi.TYPE_INTEGER, description='학생 ID'),
            openapi.Parameter('image', in_=openapi.IN_FORM, type=openapi.TYPE_FILE, description='그래프'),

        ],
        consumes=["multipart/form-data"],
        description="특정 학생의 컨설팅 내용을 PDF로 다운로드합니다.",
    )

    def post(self, request, student_id):
        student = Student.objects.get(id = student_id)
        comment = cache.get(str(student_id)+"_pdf")

        if 'image' not in request.FILES:
            return Response('Empty Content', status=status.HTTP_400_BAD_REQUEST)

        image = request.FILES['image']
        image_path = os.path.join(settings.BASE_DIR, 'analysis/img/image.jpg')

        try:
            # 이미지 저장
            with open(image_path, 'wb') as f:
                f.write(image.read())
            # 이미지를 사용한 작업 수행 (예: HTML 생성 등)
            result = generate_html_function(student, comment)
            response = HttpResponse(content_type='application/pdf; charset=utf-8')
            response['Content-Disposition'] = f'attachment; filename="{student.name}.pdf"'

            pisa.CreatePDF(result, dest=response, encoding=('utf-8'))

        finally:
            # 이미지 저장 후에는 파일을 삭제
            if os.path.exists(image_path):
                os.remove(image_path)

        Response(status.HTTP_200_OK) 
        return response


def generate_html_function(student, comment):

    # 미리 만들어 둔 HTML 파일 로드
    template = loader.get_template('template.html')
    
    student_age = datetime.today().year-int(student.birth)
    
    # 템플릿에 전달할 컨텍스트 생성
    context = {
        'student_name': student.name,
        'comment': comment,
        'student_age' : student_age,
        'school' : student.school,
        'grade' : student.grade
        }
    
    # 템플릿 렌더링
    html_content = template.render(context)

    return html_content