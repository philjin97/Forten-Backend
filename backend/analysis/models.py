from django.db import models
from student.models import Student

# Create your models here.

# class TemporaryPrompt(models.Model):
#     id = models.AutoField(primary_key=True)
#     student_id = models.ForeignKey(Student, related_name="student_prompt", on_delete=models.CASCADE, null=False, db_column="student_id")
#     prompt = models.TextField()