from django.db import models

from wingtel.contrib.mixins import DateTimeStampedModel


class Plan(DateTimeStampedModel):
    """Represents a mobile phone plan for an att/sprint subscription"""
    name = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2, max_digits=5, default=0)
    data_available = models.BigIntegerField(default=0)

    def __str__(self):
        return self.name
