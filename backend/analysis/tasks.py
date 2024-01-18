from backend.my_settings import openai_secret_key
from feedback.models import Feedback
# from .models import TemporaryPrompt
# from .serializers import TemporaryPromptSerializer
from rest_framework.response import Response
from rest_framework import status
from celery import shared_task
from django.core.cache import cache


@shared_task()
def save_prompt_task(student_id):
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
        "student_id": student_id,
        "prompt": response
    }

   

    # serializer = TemporaryPromptSerializer(data=message)
    # if serializer.is_valid():
    try:
        cache.delete(student_id)
        cache.set(student_id, response, 60 * 60)

    except:
        cache.set(student_id, response, 60 * 60)
        
        
        
        # try:
        #     feedback = TemporaryPrompt.objects.get(student_id=student_id)
        #     serialized_feedback = TemporaryPromptSerializer(feedback, data = message)
        #     if serialized_feedback.is_valid():
        #         serialized_feedback.save()
        #         return Response({"message": serialized_feedback.data}, status.HTTP_200_OK) 
        #     return Response({"message": "수정 형식에 맞지 않음. 수정 실패"}, status.HTTP_400_BAD_REQUEST)
        # except:
        #     serializer.save()
        #     return Response({"message": serializer.data}, status.HTTP_200_OK) 
        
    
    return Response({"message": "저장 실패"}, status.HTTP_400_BAD_REQUEST) 
