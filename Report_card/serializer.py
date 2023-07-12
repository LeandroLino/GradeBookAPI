from rest_framework import serializers
from .models import ReportCardsModel
from Report_notes.serializer import ReportNotesSerializer
class ReportCardserializer(serializers.ModelSerializer):
    notes = ReportNotesSerializer(many=True, read_only=True)
    class Meta:
        model = ReportCardsModel
        fields = ('id', 'delivery_date', 'student', 'notes')
    