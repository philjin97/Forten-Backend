from django.contrib import admin
from .models import Student, Exam, Subject, StudentScore

admin.site.register(Student)
admin.site.register(Exam)
admin.site.register(Subject)
admin.site.register(StudentScore)

# Register your models here.
