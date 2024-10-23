from django.db import models

class BulbState(models.Model):
    state=models.BooleanField(default=False)


class TempratureHumidity(models.Model):
    temprature=models.CharField(max_length=100)
    humidity=models.CharField(max_length=100)
    pressure=models.CharField(max_length=100)
    moisture=models.CharField(max_length=100)
    frequency=models.CharField(max_length=100)


class power(models.Model):
    voltage=models.CharField(max_length=100)
    current=models.CharField(max_length=100)