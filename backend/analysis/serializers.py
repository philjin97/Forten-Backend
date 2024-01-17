from student.models import StudentScore
from rest_framework import serializers
from .models import TemporaryPrompt

class StudentScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentScore
        fields = '__all__'


class TemporaryPromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemporaryPrompt
        fields = '__all__'
