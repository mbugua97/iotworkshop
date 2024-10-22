from django.db import models

class BulbState(models.Model):
    state=models.BooleanField(default=False)