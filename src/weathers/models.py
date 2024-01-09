from django.db import models


class Weather(models.Model):
    city = models.CharField(max_length=100, unique=True)
    temperature = models.FloatField()
    pressure = models.FloatField()
    wind_speed = models.FloatField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.city
