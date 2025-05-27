from django.contrib.auth.models import User
from django.db import models


class Run(models.Model):
    STATUS_CHOICES = [
        ("init", "Забег инициализирован"),
        ("in_progress", "Забег начат"),
        ("finished", "Забег закончен"),
    ]
    created_at = models.DateTimeField(auto_now=True)
    athlete = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="init")
    comment = models.TextField()


class AthleteInfo(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    weight = models.PositiveSmallIntegerField(default=0)
    goals = models.TextField(default=None, null=True, blank=True)
