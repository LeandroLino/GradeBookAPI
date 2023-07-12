from django.urls import path
from .views import StudentsLogin, StudentsRegister, StudentsAPI
from Disciplines.views import StudentDisciplinesEnroll

urlpatterns = [
    path('register/', StudentsRegister.as_view()),
    path('login/', StudentsLogin.as_view()),
    path('list/<int:student_id>/', StudentsAPI.as_view()),
    path('list/', StudentsAPI.as_view()),
    path('delete/<int:student_id>/', StudentsAPI.as_view()),
    path('enroll/<int:discipline_id>/<int:student_id>/', StudentDisciplinesEnroll.as_view()),
]
