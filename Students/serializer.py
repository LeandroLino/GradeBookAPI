from rest_framework import serializers
from .models import StudentsModel
from Disciplines.models import DisciplinesModel

class StudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentsModel
        fields = ('id', 'name', 'email', 'registration', 'password')

class DisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisciplinesModel
        fields = ('id', 'name', 'workload')

class StudentSerializer(serializers.ModelSerializer):
    disciplines = DisciplineSerializer(many=True, read_only=True)

    class Meta:
        model = StudentsModel
        fields = ('id', 'name', 'email', 'registration', 'disciplines','inactive')

class DisciplineStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentsModel
        fields = ('id', 'name', 'email', 'registration')
