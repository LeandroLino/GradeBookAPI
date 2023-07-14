from rest_framework.authentication import BaseAuthentication
from jose import jwt as josejwt
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission
from django.conf import settings

from Teachers.models import TeachersModel
from Students.models import StudentsModel


class IsTeacherPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user['type'] == "Student":
            return False
        user = TeachersModel.objects.get(email=request.user['email'])
        if user:
            return True
        return False
        
class IsStudentPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user['type'] == "Teacher":
            return False
        print(request.user['email'])
        user = StudentsModel.objects.get(email=request.user['email'])
        if user:
            return True
        return False

class CustomAuthenticationBackend(BaseAuthentication):
    def authenticate(self, request):
        try:
            token = request.headers.get('Authorization')
            if token is not None and token.startswith('Bearer '):
                auth_token = token.split(' ')[1]
                decoded_token = josejwt.decode(auth_token, settings.SIMPLE_JWT['SIGNING_KEY'], options={"verify_signature": False})
                return (decoded_token, None)
        except:
            raise PermissionDenied("Token inválido.")
        return None
