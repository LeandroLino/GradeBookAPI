from django.db import models
from Disciplines.models import DisciplinesModel
from Teachers.models import TeachersModel

class ReportNotesModel(models.Model):
    id = models.AutoField(primary_key=True)
    registration = models.CharField(max_length=255, null=True)
    discipline = models.ForeignKey(DisciplinesModel, on_delete=models.CASCADE, null=True)
    note = models.CharField(max_length=5)
    teacher = models.ForeignKey(TeachersModel, on_delete=models.CASCADE)
