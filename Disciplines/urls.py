from django.urls import path
from .views import DisciplinesAPI

urlpatterns = [
    path('create/', DisciplinesAPI.as_view()),
    path('list/discipline/<int:discipline_id>/', DisciplinesAPI.GetDiscipline.as_view()),
    path('list/discipline/', DisciplinesAPI.GetDiscipline.as_view()),
    path('list/teacher/<int:teacher_id>/', DisciplinesAPI.GetTeacherDisciplines.as_view()),
]
