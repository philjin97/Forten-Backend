from backend.my_settings import openai_secret_key
from feedback.models import Feedback
from student.models import StudentScore, Subject
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
            {"role": "system", "content": "넌 학원의 컨설턴트야. 학생의 평가를 기반으로 필요한 수업을 추천해주고 수강할 수 있도록 학부모를 설득해봐."},
            {"role": "user", "content": f"학생의 평가는 {feedbacks_content}"}
        ]
    )
    response = response.choices[0].message.content

    try:
        cache.delete(str(student_id)+"_prompt")
        cache.set(str(student_id)+"_prompt", response, 60 * 60)

    except:
        cache.set(str(student_id)+"_prompt", response, 60 * 60)
    
    
@shared_task()
def save_prompt_pdf_task(student_id):
    feedbacks = Feedback.objects.filter(student_id=student_id)
    feedbacks_content = ''
    for feedback in feedbacks:
        feedbacks_content += feedback.content

    scores = StudentScore.objects.filter(student_id=student_id)
    scores_content = ''
    for score in scores:
        subject = Subject.objects.get(score.subject_id).name
        scores_content += '과목 : '+ subject + " / 점수 : " + score.score + "\n"

    client = openai_secret_key

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "넌 학원에서 학생의 담당선생님이야. 학생의 성적과 평가를 참고해서 학부모가 학원에 신뢰를 가질 수 있도록 학생을 좋은 쪽으로 평가해줘"},
            {"role": "user", "content": f"학생의 평가는 {feedbacks_content}, 학생의 점수는 {scores_content}입니다."}
        ]
    )
    response = response.choices[0].message.content

    try:
        cache.delete(str(student_id)+"_pdf")
        cache.set(str(student_id)+"_pdf", response, 60 * 60)

    except:
        cache.set(str(student_id)+"_pdf", response, 60 * 60)