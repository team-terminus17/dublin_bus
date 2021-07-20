from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.expressions import Case

from enum import Enum


class Direction(Enum):
    INBOUND = 1
    OUTBOUND = 0

DIRECTION_CHOICES = [
    (Direction.INBOUND, "inbound"),
    (Direction.OUTBOUND, "outbound")
]
    


###########
# Weather #
###########


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



#############
# Base GTFS #
#############


class RouteNames(models.Model):
    
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=10)


class Agency(models.Model):

    id = models.IntegerField(primary_key=True)
    external_id = models.CharField(max_length=5)
    name = models.CharField(max_length=30)


class Services(models.Model):

    id = models.IntegerField(primary_key=True)
    external_id = models.CharField(max_length=15)
    
    monday = models.BooleanField()
    tuesday = models.BooleanField()
    wednesday = models.BooleanField()
    thursday = models.BooleanField()
    friday = models.BooleanField()
    saturday = models.BooleanField()
    sunday = models.BooleanField()
    
    start_date = models.DateField()
    end_date = models.DateField()


class ServiceExceptions(models.Model):

    SERVICE_ADDED = 1
    SERVICE_REMOVED = 2

    id = models.IntegerField(primary_key=True)
    service = models.ForeignKey(Services, on_delete=CASCADE)

    exception_type = models.IntegerField(choices=[
        (SERVICE_ADDED, "Service added"),
        (SERVICE_REMOVED, "Service removed")
    ])    


class Routes(models.Model):

    id = models.IntegerField(primary_key=True)
    external_id = models.CharField(max_length=15)
    agency = models.ForeignKey(Agency, on_delete=CASCADE)
    name = models.ForeignKey(RouteNames, on_delete=CASCADE)
    long_name = models.CharField(max_length=150)


class Shapes(models.Model):

    id = models.IntegerField(primary_key=True)
    external_id = models.CharField(max_length=30)

    lat = models.FloatField()
    lon = models.FloatField()
    sequence = models.IntegerField()
    dist_traveled = models.FloatField()


class Stops(models.Model):

    id = models.IntegerField(primary_key=True)
    external_id = models.CharField(max_length=20)

    name = models.CharField(max_length=50)
    number = models.IntegerField(null=True)
    lon = models.FloatField()
    lat = models.FloatField()

    external_name = models.CharField(max_length=70)

    routes_names = models.ManyToManyField(RouteNames, through="RouteStops", related_name="stops")


    def dictify(self):
        """Return the model as a dictionary"""
        stop = dict()
        stop['Name'] = self.name
        stop['lon'] = self.lon
        stop['lat'] = self.lat
        return stop

    def __str__(self):
        return self.external_name


class Trips(models.Model):

    id = models.IntegerField(primary_key=True)
    external_id = models.CharField(max_length=50)

    route = models.ForeignKey(Routes, on_delete=CASCADE)
    service = models.ForeignKey(Services, on_delete=CASCADE)
    shape = models.ForeignKey(Shapes, on_delete=CASCADE)

    headsign = models.CharField(max_length=150)

    direction = models.IntegerField(choices=DIRECTION_CHOICES)


class StopTimes(models.Model):

    REGULAR = 0
    NOT_AVAILABLE = 1
    PHONE_AGENCY = 2
    COORDINATE_DRIVER = 3
    PICKUP_DROPOFF_CHOICES = [
        (REGULAR, "Regular"),
        (NOT_AVAILABLE, "Not available"),
        (PHONE_AGENCY, "Phone agency"),
        (COORDINATE_DRIVER, "Coordinate with driver")
    ]

    id = models.IntegerField(primary_key=True)
    
    trip = models.ForeignKey(Trips, on_delete=CASCADE)
    stop = models.ForeignKey(Stops, on_delete=CASCADE)

    stop_sequence = models.IntegerField()

    arrival_time = models.TimeField()
    departure_time = models.TimeField()

    stop_headsign = models.CharField(max_length=30, null=True)
    pickup_type = models.IntegerField(choices=PICKUP_DROPOFF_CHOICES)
    drop_off_type = models.IntegerField(choices=PICKUP_DROPOFF_CHOICES)

    shape_dist_traveled = models.FloatField()


#####################
# DERIVED FROM GTFS #
#####################


class RouteStops(models.Model):

    id = models.IntegerField(primary_key=True)
    name = models.ForeignKey(RouteNames, on_delete=CASCADE)

    direction = models.IntegerField(choices=DIRECTION_CHOICES)

    stop = models.ForeignKey(Stops, on_delete=CASCADE)

    main = models.BooleanField()
    sequence = models.IntegerField(null=True)
