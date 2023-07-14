from django.urls import path
from .views import StudentsLogin, StudentsRegister, StudentsAPI, StudentDisciplineReportCardAPI
from Disciplines.views import StudentDisciplinesEnroll
from Report_card.views import ReportCardStudentAPI
urlpatterns = [
    path('register/', StudentsRegister.as_view()),
    path('login/', StudentsLogin.as_view()),
    path('list/<int:student_id>/', StudentsAPI.as_view()),
    path('list/', StudentsAPI.as_view()),
    path('delete/<int:student_id>/', StudentsAPI.as_view()),

    path('enroll/discipline/<int:discipline_id>/student/<int:student_id>/', StudentDisciplinesEnroll.as_view()),
    path('list-disciplines/<int:student_id>/', StudentDisciplinesEnroll.as_view()),
    path('list-report-cards/<int:student_id>/', ReportCardStudentAPI.as_view()),
    path('list/student/<int:student_id>/discipline/<int:discipline_id>/', StudentDisciplineReportCardAPI.as_view()),
]
