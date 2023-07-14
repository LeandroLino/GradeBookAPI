from rest_framework import serializers
from .models import DisciplinesModel
from Students.serializer import DisciplineStudentSerializer
from Teachers.serializer import GetTeachersSerializer

class DisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisciplinesModel
        fields = ('id', 'name', 'workload')
        
class GetDisciplineSerializer(serializers.ModelSerializer):
    students = DisciplineStudentSerializer(many=True, read_only=True)
    teachers = GetTeachersSerializer(many=True, read_only=True)
    
    class Meta:
        model = DisciplinesModel
        fields = ('id', 'name', 'workload', 'students', 'teachers')
