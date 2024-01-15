from django.urls import path
from . import views

app_name = 'feedback'

urlpatterns = [
    path('<int:user_id>/<int:student_id>/', views.FeedbackGetAPIView.as_view()),
    path('<int:user_id>/', views.FeedbackRegisterAPIView.as_view()),
    path('<int:user_id>/<int:feedback_id>/', views.FeedbackPutDeleteAPIView.as_view()),

]