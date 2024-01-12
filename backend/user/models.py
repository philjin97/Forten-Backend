from django.db import models

# Create your models here.

class Academy(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class User(models.Model):
    ROLE = [
        ('T','Teacher'), 
        ('C', 'Consultant'),
    ]
    id = models.AutoField(primary_key=True)
    academy_id = models.ForeignKey(Academy, related_name="academy_user", on_delete=models.CASCADE)
    email = models.EmailField(max_length=50, unique=True, null=False)
    name = models.CharField(max_length=20, null=False)
    password = models.CharField(max_length=50, null=False)
    phone = models.CharField(max_length=20, null=False)
    birth = models.CharField(max_length=20, null=True)
    role = models.CharField(choices=ROLE, max_length=50)
    created_at = models.DateTimeField(auto_now=True, null=False)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.email