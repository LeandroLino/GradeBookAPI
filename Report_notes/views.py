from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import ReportNotesModel
from .serializer import ReportNotesSerializer
from Disciplines.models import DisciplinesModel
from Students.models import StudentsModel
from Students.serializer import DisciplineStudentSerializer
from Teachers.auth import CustomAuthenticationBackend, IsTeacherPermission

class ReportNotesAPI(APIView):
    permission_classes = [IsTeacherPermission]
    authentication_classes = [CustomAuthenticationBackend]

    def post(self, request, discipline_id=None, student_id=None):
        serializer = ReportNotesSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if student_id:
            student = StudentsModel.objects.get(id=student_id)
            student_serializer = DisciplineStudentSerializer(data=student.__dict__)
            student_serializer.is_valid()
            request.data['registration'] = student_serializer.data['registration'] 
        model = ReportNotesModel.objects.create(**request.data)

        if discipline_id:
            discipline = DisciplinesModel.objects.get(id=discipline_id)
            model.discipline = discipline
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
        
