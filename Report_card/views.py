from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import ReportCardsModel
from Report_notes.models import ReportNotesModel
from .serializer import ReportCardserializer
from Students.models import StudentsModel

from auth import CustomAuthenticationBackend, IsTeacherPermission, IsStudentPermission


class ReportCardStudentAPI(APIView):
    permission_classes = [IsStudentPermission]
    authentication_classes = [CustomAuthenticationBackend]
    def get(self, request, student_id):
        report_cards = ReportCardsModel.objects.filter(student_id=student_id)
        serializer = ReportCardserializer(report_cards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ReportCardsAPI(APIView):

    permission_classes = [IsTeacherPermission]
    authentication_classes = [CustomAuthenticationBackend]
    def post(self, request, student_id=None, note_id=None):
        serializer = ReportCardserializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        model = ReportCardsModel.objects.create(**request.data)

        if student_id:
            student = get_object_or_404(StudentsModel, id=student_id)
            model.student = student
            note = get_object_or_404(ReportNotesModel, id=note_id)
            model.notes.add(note) 
        
        model.save()
        serializer = ReportCardserializer(instance=model)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        report_cards = ReportCardsModel.objects.all()
        serializer = ReportCardserializer(report_cards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, report_card_id=None):
        report_card = get_object_or_404(ReportCardsModel, id=report_card_id)

        delivery_date = request.data.get('delivery_date')
        if delivery_date:
            report_card.delivery_date = delivery_date

        notes_ids = request.data.get('notes')
        if notes_ids:
            for note_id in notes_ids:
                note = get_object_or_404(ReportNotesModel, id=note_id)
                report_card.notes.add(note)

        report_card.save()

        serializer = ReportCardserializer(report_card)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)