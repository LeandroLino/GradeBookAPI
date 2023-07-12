from rest_framework import serializers
from .models import ReportNotesModel
from Disciplines.serializer import DisciplineSerializer

class ReportNotesSerializer(serializers.ModelSerializer):
    #discipline = DisciplineSerializer(many=True, read_only=True)

    class Meta:
        model = ReportNotesModel
        fields = ('id', 'note', 'discipline', 'registration')
    