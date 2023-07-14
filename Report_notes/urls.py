from django.urls import path
from .views import ReportNotesAPI

urlpatterns = [
    path('create/', ReportNotesAPI.as_view()),
    path('create/<int:student_id>/', ReportNotesAPI.as_view()),
    path('create/discipline/<int:discipline_id>/student/<int:student_id>/', ReportNotesAPI.as_view()),
    path('list/', ReportNotesAPI.as_view()),
    path('list/<int:note_id>/', ReportNotesAPI.as_view()),
    path('update/<int:note_id>/', ReportNotesAPI.as_view()),
    path('update/<int:note_id>/<int:student_id>/', ReportNotesAPI.as_view()),
    path('delete/<int:note_id>/', ReportNotesAPI.as_view()),
]
