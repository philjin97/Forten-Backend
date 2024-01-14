from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from student.models import StudentScore
from feedback.models import Feedback
from .serializers import StudentScoreSerializer
from openai import OpenAI
from backend.my_settings import openai_secret_key

# Create your views here.

class Rating(APIView):

    def get(self, request, student_id):
        try:
            student = Feedback.objects.filter(student_id=student_id)

            avg_student_rating = 0

            for student_feedback in student:
                avg_student_rating += student_feedback.student_rating 
            
            avg_student_rating = avg_student_rating//len(student)
            
            
            avg_parent_rating = 0

            for student_feedback in student:
                avg_parent_rating += student_feedback.parent_rating 
            
            avg_parent_rating = avg_parent_rating//len(student)

            message = {
                "message": "평가 조회 성공",
                "result": {
                    "student_rating": avg_student_rating,
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

    def get(self, request, student_id):
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

        message = {
            "response": response
        }
        
        return Response(message, status.HTTP_200_OK) 


    
