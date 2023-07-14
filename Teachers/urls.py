from django.urls import path
from .views import TeacherAPI, TeacherAccount
from Disciplines.views import TeacherDisciplinesEnroll

urlpatterns = [
    path('register/', TeacherAccount.TeacherRegister.as_view()),
    path('login/', TeacherAccount.TeacherLogin.as_view()),

    path('enroll/discipline/<int:discipline_id>/teacher/<int:teacher_id>/', TeacherDisciplinesEnroll.as_view()),
    path('list-disciplines/<int:teacher_id>/', TeacherDisciplinesEnroll.as_view()),

    path('list/<int:teacher_id>/', TeacherAPI.as_view()),
    path('list/', TeacherAPI.as_view()),
    path('delete/<int:teacher_id>/', TeacherAPI.as_view()),

]
