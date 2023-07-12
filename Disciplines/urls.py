from django.urls import path
from .views import DisciplinesAPI

urlpatterns = [
    path('create/', DisciplinesAPI.as_view()),
    path('list/<int:discipline_id>/', DisciplinesAPI.as_view()),
    path('list/', DisciplinesAPI.as_view())
]
