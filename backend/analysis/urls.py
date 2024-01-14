from django.urls import path
from . import views

urlpatterns = [
    path('<int:student_id>/', views.Rating.as_view()),
    # path('score/<int:student_id>/<int:subject_id>/', views.Score.as_view()),
    path('prompt/<int:student_id>/', views.Prompt.as_view()),
]
