from django.urls import path, include
from . import views

app_name = 'student'

urlpatterns = [
    path('', views.StudentGetPostAPIView.as_view(), name='student_regist_info'),
    path('<int:student_id>/score/', views.ScoreGetPostAPIView.as_view(), name='score_regist_info'),
]