from django.urls import path
from .views import TeacherAPI, TeacherAccount
from Disciplines.views import TeacherDisciplinesEnroll

urlpatterns = [
    path('register/', TeacherAccount.TeacherRegister.as_view()),
    path('login/', TeacherAccount.TeacherLogin.as_view()),
    path('login/refresh/', TeacherAccount.TeacherLogin.as_view(), name='token_refresh'),

    path('enroll/<int:discipline_id>/<int:teacher_id>/', TeacherDisciplinesEnroll.as_view()),

    path('list/<int:teacher_id>/', TeacherAPI.as_view()),
    path('list/', TeacherAPI.as_view()),
    path('delete/<int:teacher_id>/', TeacherAPI.as_view()),

]
