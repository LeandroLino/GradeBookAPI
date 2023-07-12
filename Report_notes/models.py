from django.db import models
from Disciplines.models import DisciplinesModel

class ReportNotesModel(models.Model):
    id = models.AutoField(primary_key=True)
    registration = models.CharField(max_length=255, null=True)
    discipline = models.ForeignKey(DisciplinesModel, on_delete=models.CASCADE, null=True)
    note = models.CharField(max_length=5)
    #report_card = models.ForeignKey('Report_card.ReportCardsModel', on_delete=models.CASCADE, null=True)
