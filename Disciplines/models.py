from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string

class DisciplinesModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    workload = models.CharField(max_length=255)
    students = models.ManyToManyField('Students.StudentsModel')
    teacher = models.OneToOneField('Teachers.TeachersModel', on_delete=models.CASCADE, null=True)
    