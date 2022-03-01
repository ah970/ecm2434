from django.db import models
from django.contrib.auth.models import User


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    is_game_master = models.BooleanField(default=False)


class Event(models.Model):
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=200)
    start = models.DateTimeField()
    end = models.DateTimeField()
    latitude = models.DecimalField(max_digits=22, decimal_places=16)
    longitude = models.DecimalField(max_digits=22, decimal_places=16)


class Participation(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
