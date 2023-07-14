from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from auth import CustomAuthenticationBackend, IsTeacherPermission
from rest_framework_simplejwt.views import TokenObtainPairView
import jwt
from django.conf import settings

from django.utils import timezone
from datetime import timedelta

from .serializer import TeachersSerializer, GetdDisciplineTeachersSerializer, CustomTokenObtainPairSerializer
from .models import TeachersModel, AuthToken
from utils import generate_registration_id
from Disciplines.serializer import DisciplineSerializer

class TeacherAccount(TokenObtainPairView):
    class TeacherLogin(APIView):
        serializer_class = CustomTokenObtainPairSerializer
        def post(self, request):
            email = request.data.get('email')
            password = request.data.get('password')

            teacher = TeachersModel.objects.filter(email=email).first()
            if teacher is not None and check_password(password, teacher.password):
                auth_token, _ = AuthToken.objects.get_or_create(user=teacher)
                token = jwt.encode({'email': teacher.__dict__['email'], 'id': teacher.__dict__['id'], 'type': 'Teacher'}, settings.SIMPLE_JWT['SIGNING_KEY'], algorithm='HS256').decode('utf-8')
                auth_token.token = token
                auth_token.expires_at = timezone.now() + timedelta(days=7)
                auth_token.save()

                return Response({'access_token': str(token)})

            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
    class TeacherRegister(APIView):
        serializer_class = CustomTokenObtainPairSerializer
        def post(self, request):
            request.data['registration'] = generate_registration_id()
            serializer = TeachersSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            password = serializer.validated_data.get('password')
            hashed_password = make_password(password)
            serializer.validated_data['password'] = hashed_password

            serializer.save()
            teacher = TeachersModel.objects.filter(email=serializer.data['email']).first()
            auth_token, _ = AuthToken.objects.get_or_create(user=teacher)
            token = jwt.encode({'email': serializer.data['email'], 'id': serializer.data['id'], 'type': 'Teacher'}, settings.SIMPLE_JWT['SIGNING_KEY'], algorithm='HS256').decode('utf-8')
            auth_token.token = token
            auth_token.expires_at = timezone.now() + timedelta(days=7)
            auth_token.save()
            return Response({'access_token': token}, status=status.HTTP_201_CREATED)


class TeacherAPI(APIView):
    permission_classes = [IsTeacherPermission]
    authentication_classes = [CustomAuthenticationBackend]
    
    def get(self, request, teacher_id=None):
        if teacher_id:
            teacher = get_object_or_404(TeachersModel, id=teacher_id)
            disciplines = teacher.disciplines.all()
            disciplines_serializer = DisciplineSerializer(disciplines, many=True)
            serializer = GetdDisciplineTeachersSerializer(instance=teacher)
            serializer.data['disciplines'] = disciplines_serializer.data
        else:
            teachers = TeachersModel.objects.all()
            serializer = GetdDisciplineTeachersSerializer(instance=teachers, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



    def delete(self, request, teacher_id):
        teacher = get_object_or_404(TeachersModel, id=teacher_id)
        teacher.inactive = True
        teacher.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)

