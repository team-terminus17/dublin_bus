from django.db import models


# Create your models here.
class Stops(models.Model):
    stopID = models.IntegerField(primary_key=True)
    stopName = models.CharField(max_length=50, null=True)
    lon = models.FloatField(null=True)
    lat = models.FloatField(null=True)

    class Meta:
        db_table = 'stops'

    def __str__(self):
        return str(self.stopID) + self.stopName


class RouteStops(models.Model):
    routeID = models.CharField(max_length=10)
    direction = models.CharField(max_length=1)
    stopID = models.IntegerField()

    class Meta:
        db_table = 'route_stops'
        unique_together = ("routeID", "direction", "stopID")


class Weather(models.Model):
    weather_time = models.IntegerField(primary_key=True)
    temp = models.FloatField()
    rain = models.BooleanField()
    icon = models.CharField(max_length=6)

    class Meta:
        db_table = 'futureweather'
