from django.urls import path
from .views import ReportCardsAPI

urlpatterns = [
    path('create/<int:student_id>/', ReportCardsAPI.as_view()),
    path('create/<int:student_id>/<int:note_id>/', ReportCardsAPI.as_view()),
    path('list/<int:student_id>/', ReportCardsAPI.as_view()),
    path('list/', ReportCardsAPI.as_view()),
    path('update/<int:report_card_id>/', ReportCardsAPI.as_view()),
]
