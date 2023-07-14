from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from datetime import timedelta
from django.utils import timezone
import jwt
from django.conf import settings

from .serializer import StudentsSerializer, StudentSerializer
from .models import StudentsModel, AuthToken

from Report_card.models import ReportCardsModel
from Disciplines.models import DisciplinesModel

from Disciplines.serializer import DisciplineSerializer
from Report_card.serializer import ReportCardserializer
from Report_notes.serializer import ReportNotesSerializer

from utils import generate_registration_id

class StudentDisciplineReportCardAPI(APIView):
    def get(self, request, student_id, discipline_id):
        report_cards = ReportCardsModel.objects.filter(student_id=student_id)
        report_cards = report_cards.filter(notes__discipline_id=discipline_id)
        serializer = ReportCardserializer(report_cards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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

            student = StudentsModel.objects.filter(email=serializer.data['email']).first()
            auth_token, _ = AuthToken.objects.get_or_create(user=student)
            token = jwt.encode({'email': student.__dict__['email'], 'id': student.__dict__['id'], 'type': 'Student'}, settings.SIMPLE_JWT['SIGNING_KEY'], algorithm='HS256').decode('utf-8')
            auth_token.token = token
            auth_token.expires_at = timezone.now() + timedelta(days=7)
            auth_token.save()

            return Response({'access_token': str(token)}, status=status.HTTP_201_CREATED)

class StudentsLogin(APIView):
    def post(self, request):
            email = request.data.get('email')
            password = request.data.get('password')

            student = StudentsModel.objects.filter(email=email).first()
            if student is not None and check_password(password, student.password):
                auth_token, _ = AuthToken.objects.get_or_create(user=student)
                token = jwt.encode({'email': student.__dict__['email'], 'id': student.__dict__['id'], 'type': 'Student'}, settings.SIMPLE_JWT['SIGNING_KEY'], algorithm='HS256').decode('utf-8')
                auth_token.token = token
                auth_token.expires_at = timezone.now() + timedelta(days=7)
                auth_token.save()

                return Response({'access_token': str(token)})

            return Response(status=status.HTTP_401_UNAUTHORIZED)


