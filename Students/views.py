from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta

from .serializer import StudentsSerializer, StudentSerializer
from Disciplines.serializer import DisciplineSerializer
from .models import StudentsModel, AuthToken
from utils import generate_registration_id

class StudentsAPI(APIView):
    def get(self, request, student_id=None):
        if student_id:
            student = get_object_or_404(StudentsModel, id=student_id)
            disciplines = student.disciplines.all()
            disciplines_serializer = DisciplineSerializer(disciplines, many=True)
            serializer = StudentSerializer(instance=student)
            serializer.data['disciplines'] = disciplines_serializer.data
        else:
            students = StudentsModel.objects.all()
            serializer = StudentSerializer(instance=students, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def delete(self, request, student_id):
        student = get_object_or_404(StudentsModel, id=student_id)
        student.inactive = True
        student.save()
        serializer = StudentSerializer(instance=student)

        return Response(serializer.data, status=status.HTTP_200_OK)

class StudentsRegister(APIView):
    def post(self, request):
            request.data['registration'] = generate_registration_id()
            serializer = StudentsSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            password = serializer.validated_data.get('password')
            hashed_password = make_password(password)
            serializer.validated_data['password'] = hashed_password

            serializer.save()
            return Response({}, status=status.HTTP_201_CREATED)

class StudentsLogin(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        student = StudentsModel.objects.filter(email=email).first()

        if student is not None and check_password(password, student.password):
            token = AuthToken.objects.filter(user=student).first()
            if not token:
                token = AuthToken(user=student)
                token.expires_at = datetime.now() + timedelta(days=1)
                token.save()
            return Response({'token': token.token})

        return Response(status=status.HTTP_404_NOT_FOUND)


