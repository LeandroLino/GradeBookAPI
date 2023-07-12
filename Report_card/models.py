from django.db import models

class ReportCardsModel(models.Model):
    id = models.AutoField(primary_key=True)
    delivery_date = models.DateTimeField()
    student = models.ForeignKey('Students.StudentsModel', on_delete=models.CASCADE, null=True)
    notes = models.ManyToManyField('Report_notes.ReportNotesModel', null=True)


