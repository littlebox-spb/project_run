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
    distance = models.FloatField(default=0)
    speed = models.FloatField(default=0)
    comment = models.TextField()
    run_time_seconds = models.PositiveIntegerField(null=True, blank=True)


class AthleteInfo(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    weight = models.PositiveSmallIntegerField(default=0)
    goals = models.TextField(default=None, null=True, blank=True)

class Challenge(models.Model):
    full_name = models.CharField(max_length=200)
    athlete = models.ForeignKey(User, on_delete=models.CASCADE)

class Position(models.Model):
    run = models.ForeignKey(Run, on_delete=models.CASCADE)
    latitude = models.FloatField(blank=False)
    longitude = models.FloatField(blank=False)
    date_time = models.DateTimeField(null=True, blank=True)
    distance = models.FloatField(default=0)
    speed = models.FloatField(default=0)


class CollectibleItem(models.Model):
    name = models.CharField(max_length=200)
    uid = models.CharField(max_length=20)
    latitude = models.FloatField()
    longitude = models.FloatField()
    picture = models.URLField()
    value = models.IntegerField()
    items = models.ManyToManyField(User, related_name='collectible_items')
    
class Subscriber(models.Model):
    coach = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coach')
    athlete = models.ForeignKey(User, on_delete=models.CASCADE, related_name='athlete')