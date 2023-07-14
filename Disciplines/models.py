from django.db import models

class DisciplinesModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    workload = models.CharField(max_length=255)
    students = models.ManyToManyField('Students.StudentsModel')
    teachers = models.ManyToManyField('Teachers.TeachersModel', blank=True)
    