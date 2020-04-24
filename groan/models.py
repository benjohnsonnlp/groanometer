from django.db import models

class Groan(models.Model):
    magnitude = models.IntegerField()

