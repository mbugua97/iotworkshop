from django.db import models


class BulbState(models.Model):
    state=models.BooleanField(default=False)


class TempratureHumidity(models.Model):
    temp=models.CharField(max_length=100),
    humidity=models.CharField(max_length=100),
    pressure=models.CharField(max_length=100),
    moisture=models.CharField(max_length=100),
    frequency=models.CharField(max_length=100),