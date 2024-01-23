from rest_framework import serializers
from .models import Feedback

class FeedbackSerializer(serializers.ModelSerializer):
  class Meta:
    model = Feedback
    fields = '__all__'

class FeedbackRegisterSerializer(serializers.ModelSerializer):
  parent_rating = serializers.IntegerField(required=False, allow_null=True)
  content = serializers.CharField(required=False, allow_blank=True)
  
  class Meta:
    model = Feedback
    fields = ["id", "user_id", "student_id", "student_rating", "parent_rating", "content"]