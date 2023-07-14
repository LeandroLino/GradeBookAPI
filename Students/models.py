from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from Disciplines.models import DisciplinesModel
from datetime import datetime, timedelta

class StudentsModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    registration = models.CharField(max_length=255)
    disciplines = models.ManyToManyField(DisciplinesModel)
    inactive = models.BooleanField(default=False)

class AuthToken(models.Model):
    user = models.OneToOneField(StudentsModel, on_delete=models.CASCADE)
    token = models.CharField(max_length=40, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField(default=timezone.now() + timedelta(days=7))

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.generate_token()
        return super().save(*args, **kwargs)

    def generate_token(self):
        return get_random_string(40)
    
    def is_expired(self):
        return timezone.now() > self.expires_at