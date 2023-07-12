from rest_framework import serializers
from .models import TeachersModel
from Disciplines.models import DisciplinesModel
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class TeachersSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeachersModel
        fields = ('id','name', 'email', 'password', 'inactive')

class GetTeachersSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeachersModel
        fields = ('id','name', 'email', 'inactive')

class DisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisciplinesModel
        fields = ('id', 'name', 'workload')

class GetdDisciplineTeachersSerializer(serializers.ModelSerializer):
    discipline = DisciplineSerializer(read_only=True)

    class Meta:
        model = TeachersModel
        fields = ('id','name', 'email', 'discipline', 'inactive')


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Customize o payload do token, se necessário
        token['username'] = user.username
        token['email'] = user.email
        # ...

        return token