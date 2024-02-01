from student.models import StudentScore
from rest_framework import serializers

class StudentScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentScore
        fields = '__all__'