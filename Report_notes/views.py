from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializer import ReportNotesSerializer
from Students.serializer import DisciplineStudentSerializer

from .models import ReportNotesModel
from Disciplines.models import DisciplinesModel
from Students.models import StudentsModel
from Teachers.models import TeachersModel
from auth import CustomAuthenticationBackend, IsTeacherPermission, IsStudentPermission

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

class ReportNotesAPI(APIView):
    permission_classes = [IsTeacherPermission]
    authentication_classes = [CustomAuthenticationBackend]

    def post(self, request, discipline_id=None, student_id=None):
        serializer = ReportNotesSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        teacher_id = request.user['id']
        teacher = TeachersModel.objects.get(id=teacher_id)

        serializer.validated_data['teacher'] = teacher
        registration = None
        if student_id:
            try:
                student = get_object_or_404(StudentsModel, id=student_id)
                student_serializer = DisciplineStudentSerializer(data=student.__dict__)
                student_serializer.is_valid()
                registration = student_serializer.data['registration']
            except ObjectDoesNotExist: 
                return Response({}, status=status.HTTP_404_NOT_FOUND)

        model = ReportNotesModel(**serializer.validated_data)

        if discipline_id:
            discipline = DisciplinesModel.objects.get(id=discipline_id)
            model.discipline = discipline

        if registration:
            model.registration = registration

        model.save()

        serializer = ReportNotesSerializer(instance=model)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, note_id=None):
        if note_id:
            try:
                model = ReportNotesModel.objects.get(id=note_id)
            except:
                return Response({}, status=status.HTTP_404_NOT_FOUND)
            serializer = ReportNotesSerializer(instance=model)
        else:
            model = ReportNotesModel.objects.all()
            serializer = ReportNotesSerializer(many=True, instance=model)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def put(self, request, note_id=None, student_id=None):
        if note_id:
            try:
                model = ReportNotesModel.objects.get(id=note_id)
            except:
                return Response({}, status=status.HTTP_404_NOT_FOUND)
            serializer = ReportNotesSerializer(instance=model, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            
            if student_id:
                try:
                    student = StudentsModel.objects.get(id=student_id)
                except:
                    return Response({}, status=status.HTTP_404_NOT_FOUND)
                student_serializer = DisciplineStudentSerializer(data=student.__dict__)
                student_serializer.is_valid()
                serializer.validated_data['registration'] = student_serializer.data['registration']
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, note_id=None):
        note = ReportNotesModel.objects.get(id=note_id)
        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
