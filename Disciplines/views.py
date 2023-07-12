from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .serializer import DisciplineSerializer, GetDisciplineSerializer
from .models import DisciplinesModel
from Students.models import StudentsModel
from Teachers.models import TeachersModel
from Teachers.serializer import GetdDisciplineTeachersSerializer
from Students.serializer import StudentSerializer

from Teachers.auth import CustomAuthenticationBackend, IsTeacherPermission


class DisciplinesAPI(APIView):
    permission_classes = [IsTeacherPermission]
    authentication_classes = [CustomAuthenticationBackend]
    def post(self, request):
        serializer = DisciplineSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, discipline_id=None):
        if discipline_id:
            discipline = get_object_or_404(DisciplinesModel, id=discipline_id)
            serializer = GetDisciplineSerializer(instance=discipline)
        else:
            disciplines = DisciplinesModel.objects.all()
            serializer = GetDisciplineSerializer(instance=disciplines, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class StudentDisciplinesEnroll(APIView):
    def put(self, request, discipline_id, student_id):
        discipline = get_object_or_404(DisciplinesModel, id=discipline_id)
        student = get_object_or_404(StudentsModel, id=student_id)
        disciplines = student.disciplines.all()

        if student.inactive:
            return Response({'error': 'Invalid discipline or student'}, status=status.HTTP_400_BAD_REQUEST)

        discipline.students.add(student)
        student.disciplines.add(discipline)

        disciplines = student.disciplines.all()
        disciplines_serializer = DisciplineSerializer(disciplines, many=True)
        serializer = StudentSerializer(instance=student)
        serializer.data['disciplines'] = disciplines_serializer.data

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class TeacherDisciplinesEnroll(APIView):
    permission_classes = [IsTeacherPermission]
    authentication_classes = [CustomAuthenticationBackend]

    def put(self, request, discipline_id, teacher_id):
        discipline = get_object_or_404(DisciplinesModel, id=discipline_id)
        teacher = get_object_or_404(TeachersModel, id=teacher_id)
        if teacher.inactive:
            return Response({'error': 'Invalid discipline or teacher'}, status=status.HTTP_400_BAD_REQUEST)

        if discipline and teacher:
            discipline.teacher = teacher
            discipline.save()
            teacher.discipline = discipline
            teacher.save()
            serializer = GetdDisciplineTeachersSerializer(teacher)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Invalid discipline or teacher'}, status=status.HTTP_404_NOT_FOUND)

    