from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.StudentGetPostAPIView.as_view()),
    path('<int:student_id>/score/', views.ScoreGetPostAPIView.as_view()),
]