from django.db import models


# Create your models here.
class Stops(models.Model):
    stopID = models.IntegerField(primary_key=True)
    stopName = models.CharField(max_length=50, null=True)
    lon = models.FloatField(null=True)
    lat = models.FloatField(null=True)

    class Meta:
        db_table = 'stops'

    def dictify(self):
        """Return the model as a dictionary"""
        stop = dict()
        stop['Name'] = self.stopName
        stop['lon'] = self.lon
        stop['lat'] = self.lat
        return stop

    def __str__(self):
        return str(self.stopID) + self.stopName


class RouteStops(models.Model):
    routeID = models.CharField(primary_key=True, max_length=10)
    direction = models.CharField(max_length=1)
    stopID = models.IntegerField()
    sequence = models.IntegerField()

    class Meta:
        db_table = 'routestops'
        unique_together = ("routeID", "direction", "stopID")


class Weather(models.Model):
    weather_time = models.IntegerField(primary_key=True)
    temp = models.FloatField()
    rain = models.BooleanField()
    icon = models.CharField(max_length=6)

    class Meta:
        db_table = 'futureweather'

    def dictify(self):
        weather = dict()
        weather['temp'] = self.temp
        weather['rain'] = self.rain
        weather['icon'] = self.icon
        return weather
