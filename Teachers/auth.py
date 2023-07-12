from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import TeachersModel
from jose import jwt as josejwt
import jwt
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission
from django.conf import settings

class IsTeacherPermission(BasePermission):
    def has_permission(self, request, view):
        user = TeachersModel.objects.get(email=request.user.email)
        print(user.__dict__)
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
                print(decoded_token)
                user_id = decoded_token['id']
                user = TeachersModel.objects.get(id=user_id)
                return (user, None)
        except jwt.InvalidTokenError:
            raise PermissionDenied("Token inválido.")
        except (jwt.DecodeError, jwt.ExpiredSignatureError, TeachersModel.DoesNotExist):
            pass
        return None
