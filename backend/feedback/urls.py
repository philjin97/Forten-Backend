from django.urls import path
from . import views

app_name = 'feedback'

urlpatterns = [
    path('<int:user_id>/', views.FeedbackGetPostAPIView.as_view(), name='feedback_register_info'),
    path('<int:user_id>/<int:feedback_id>/', views.FeedbackPutDeleteAPIView.as_view(), name='feedback_update_delete'),

]