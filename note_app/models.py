from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pk}-{self.created_at}"

