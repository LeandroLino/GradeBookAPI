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


from auth import CustomAuthenticationBackend, IsTeacherPermission

class DisciplinesAPI(APIView):
    permission_classes = [IsTeacherPermission]
    authentication_classes = [CustomAuthenticationBackend]
    def post(self, request):
        discipline = DisciplinesModel.objects.create(**request.data)
        teacher = get_object_or_404(TeachersModel, id=request.user['id'])
        if teacher.inactive:
            return Response({'error': 'Invalid discipline or teacher'}, status=status.HTTP_400_BAD_REQUEST)

        if discipline and teacher:
            discipline.teachers.add(teacher)
            teacher.disciplines.add(discipline)
            discipline.save()
            teacher.save()
            serializer = GetDisciplineSerializer(discipline)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Invalid discipline or teacher'}, status=status.HTTP_404_NOT_FOUND)



    class GetDiscipline(APIView):
        def get(self, request, discipline_id=None, page=2, limit=20):
            if discipline_id:
                discipline = get_object_or_404(DisciplinesModel, id=discipline_id)
                serializer = GetDisciplineSerializer(instance=discipline)
            else:
                start_index = (page - 1) * limit
                end_index = start_index + limit
                disciplines = DisciplinesModel.objects.all()
                disciplines = disciplines[start_index:end_index]
                serializer = GetDisciplineSerializer(instance=disciplines, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

    class GetTeacherDisciplines(APIView):
        def get(self, request, teacher_id):
            teacher = get_object_or_404(TeachersModel, id=teacher_id)
            disciplines = teacher.disciplines.all()
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
    
    def get(self, request, student_id):
        disciplines = DisciplinesModel.objects.filter(students=student_id)
        disciplines_serializer = GetDisciplineSerializer(instance=disciplines, many=True)
        return Response(disciplines_serializer.data, status=status.HTTP_200_OK)


class TeacherDisciplinesEnroll(APIView):
    permission_classes = [IsTeacherPermission]
    authentication_classes = [CustomAuthenticationBackend]

    def put(self, request, discipline_id, teacher_id):
        discipline = get_object_or_404(DisciplinesModel, id=discipline_id)
        teacher = get_object_or_404(TeachersModel, id=teacher_id)
        if teacher.inactive:
            return Response({'error': 'Invalid discipline or teacher'}, status=status.HTTP_400_BAD_REQUEST)

        if discipline and teacher:
            discipline.teachers.add(teacher)
            teacher.disciplines.add(discipline)
            discipline.save()
            teacher.save()
            serializer = GetDisciplineSerializer(discipline)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Invalid discipline or teacher'}, status=status.HTTP_404_NOT_FOUND)

        
    def get(self, request, teacher_id):
        disciplines = DisciplinesModel.objects.filter(teachers=teacher_id)
        disciplines_serializer = GetDisciplineSerializer(instance=disciplines, many=True)
        return Response(disciplines_serializer.data, status=status.HTTP_200_OK)

    