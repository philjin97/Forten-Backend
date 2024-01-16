from django.db import models
from user.models import Academy

# Create your models here.
# 학생 테이블
class Student(models.Model):
  id = models.AutoField(primary_key=True)
  academy_id = models.ForeignKey(Academy, related_name="academy_student", on_delete=models.CASCADE, null=False, db_column="academy_id")
  name = models.CharField(max_length=20, null=False)
  birth = models.CharField(max_length=20, null=False)
  phone = models.CharField(max_length=20, null=True)
  school = models.CharField(max_length=50, null=True)
  grade = models.CharField(max_length=50, null=True)
  parent_name = models.CharField(max_length=20, null=False)
  parent_phone = models.CharField(max_length=20, null=False)
  created_at = models.DateTimeField(auto_now_add=True, null=False)
  updated_at = models.DateTimeField(auto_now=True, null=True)
  deleted_at = models.DateTimeField(blank=True, null=True)

  # 시험 테이블
  # 내신 1학기 중간
  # 내신 1학기  기말
  # 내신 2학기 중간
  # 내신 2학기  기말
  # 모의고사 6월
  # 모의고사 9월
class Exam(models.Model):
  id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=50, null=False)

  # 과목 테이블
  # 국어
  # 영어
  # 수학
  # 토플
class Subject(models.Model):
  id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=50, null=False)

  # 학생 성적 테이블   
class StudentScore(models.Model):
  id = models.AutoField(primary_key=True)
  student_id = models.ForeignKey(Student, related_name="student_studentScore", on_delete=models.CASCADE, null=False, db_column="student_id")
  subject_id = models.ForeignKey(Subject, related_name="subject_studentScore", on_delete=models.CASCADE, null=False, db_column="exam_id")
  exam_id = models.ForeignKey(Exam, related_name="exam", on_delete=models.CASCADE, null=False)
  type = models.CharField(max_length=20, null=False)
  score = models.BigIntegerField(null=False)
  grade = models.CharField(max_length=20, null=False)
  created_at = models.DateTimeField(auto_now_add=True, null=False)
  updated_at = models.DateTimeField(auto_now=True, null=True)