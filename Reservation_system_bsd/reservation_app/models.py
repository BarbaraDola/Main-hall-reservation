from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import CheckConstraint, Q

# Create your models here.
class MainHall(models.Model):
    name = models.CharField(max_length=255, unique=True)
    room_capacity = models.IntegerField()
    projector = models.BooleanField(default=False)

class Reservation(models.Model):
    date = models.DateField()
    room = models.ForeignKey(MainHall, on_delete=models.CASCADE)
    comment = models.TextField(null=True)
    class Meta:
        unique_together = ('room', 'date',)