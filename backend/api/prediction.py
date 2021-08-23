import traceback
import requests, pickle, io
from decouple import config

from .models import *
from . import utils
from . import gtfs
from . import weather


def model_predict(route, direction, dep_stop, arr_stop, datetime, fallback=False):
    
    dt = utils.utc_unix_to_dt(datetime)

    # Guess the planned time from the GTFS schedule.

    # The dep_stop and arr_stop might be swapped if they are found
    # to be in the wrong order.
    dep_stop, arr_stop, sequence = get_stop_sequence(
        route, direction, dep_stop, arr_stop, dt)
    
    planned_time = get_planned_time(
        route, direction, dep_stop, arr_stop, dt)

    # Predict delay.

    total_delay = 0

    try:

        dt_features = get_datetime_features(dt)
        weather_features = get_weather_features(dt)
        
        model = get_model(route, direction)

        features = [None, *dt_features, *weather_features]

        for number, expected_min, expected_max in sequence:
            features[0] = number
            delay = model.predict([features])[0]
            delay = max(expected_min, min(delay, expected_max))
            total_delay += delay

    except:
        if fallback:
            print("PREDICTION MODEL FAILURE")
            print("(Defaulting to 0 delay)")
            traceback.print_exc()
        
        # It can be better to handle this at the callsite.
        # For example, if the google time is available, 
        # that can be used instead.
        else: raise

    predicted_time = planned_time + total_delay
    return predicted_time


def get_model(route, direction):

    url = (
        "https://terminus-models.s3.amazonaws.com"
        f"/whole-route-trees/model_{route}_{direction}.pkl"
    )

    try:
        data = requests.get(url).content
        with io.BytesIO(data) as file_like:
            model = pickle.load(file_like)
    except:
        raise ValueError(
            f"Failed to retrieve model for (route:{route} dir:{direction})")

    return model


def journey_str(route, direction, dep_stop, arr_stop, dt):
    return  (
        f"route:{route} dir:{direction} dep:{dep_stop} arr:{arr_stop} dt:{dt}"
    )


#############
# GTFS Data #
#############

def get_stop_sequence(route, direction, dep_stop, arr_stop, dt):

    # Get the seqeunce numbers for the start and end stops. This assumes that 
    # the trip will be following the "main" path, which won't always be true.
    
    try:
        dep_stop_seq = RouteStops.objects.get(
            name__name=route, direction=direction, stop_id=dep_stop).sequence
        arr_stop_seq = RouteStops.objects.get(
            name__name=route, direction=direction, stop_id=arr_stop).sequence
    except:
        raise ValueError(
            "Failed to identify stop sequences for journey:"
            f" {journey_str(route, direction, dep_stop, arr_stop, dt)}."
        )

    # If the start and end stops are out of order, swap them.

    if dep_stop_seq > arr_stop_seq:
        dep_stop, arr_stop = arr_stop, dep_stop
        dep_stop_seq, arr_stop_seq = arr_stop_seq, dep_stop_seq

    # Get all the stops between the start and end stop, inclusive.

    routestops_entries = RouteStops.objects.filter(
        name__name=route, direction=direction,
        sequence__gt=dep_stop_seq, sequence__lte=arr_stop_seq
    ).select_related("stop")

    stops = dict()
    for entry in routestops_entries:
        stops[entry.stop_id] = entry.stop.number

    bounds_entries = PredictionBounds.objects.filter(
        route_name__name=route, direction=direction,
        stop_id__in=stops.keys()
    )

    bounds_lookup = dict()
    for entry in bounds_entries:
        bounds_lookup[entry.stop_id] = entry.min, entry.max

    sequence = list()
    for stop_id, number in stops.items():
        bounds = bounds_lookup.get(stop_id, None)
        if bounds is None:
            bounds = (0, 600)
        sequence.append((number, *bounds))

    return dep_stop, arr_stop, sequence


def get_planned_time(route, direction, dep_stop, arr_stop, dt):

    active_services = gtfs.get_active_services(dt)

    # Try to find a trip for the current route, which passes by the departure
    # stop either after or at the current time.

    trip_id = StopTimes.objects.select_related("trip__route__name")\
        .filter(trip__route__name__name=route, trip__direction=direction)\
        .filter(trip__service_id__in=active_services)\
        .filter(stop_id=dep_stop)\
        .filter(arrival_time__gte=dt.replace(hour=6, minute=30))\
        .order_by("arrival_time")\
        .values_list("trip_id", flat=True)[0]

    # Retrieve the times at which this trip passes the departure and
    # arrival stops.

    def get_time(stop_id):
        query =  StopTimes.objects.filter(trip_id=trip_id, stop_id=stop_id)
        return query.values_list("arrival_time", flat=True)[0]

    try:
        dep_time = get_time(dep_stop)
        arr_time = get_time(arr_stop)
    except:
        raise ValueError(
            "Failed to find planned trip for journey:"
            f" {journey_str(route, direction, dep_stop, arr_stop, dt)}."
        )

    # Subtract these to get the planned time.

    planned_time = utils.minus_time(arr_time, dep_time).total_seconds()
    return planned_time


#####################
# Datetime Features #
#####################

def get_datetime_features(target_datetime):
    
    # 'astimezone' with no arguments converts the datetime
    # to the current datetime - at some point we need to make sure that 
    # this is configured correctly in Django.
    dt = target_datetime.astimezone()

    month = dt.month
    day = dt.day
    hour = dt.hour

    school = not (6 <= month <= 8)

    # From 7:00 to 8:30 or from 16:00 to 18:00
    max_morning_hour = 8 if dt.minute <= 30 else 7
    morning_rush = 7 <= dt.hour <= max_morning_hour
    evening_rush = 16 <= dt.hour <= 18
    rush_hour = morning_rush or evening_rush

    weekday = dt.weekday
    weekend = (weekday == 5) or (weekday == 6) 

    # Yes. These are hardcoded for 2021. This should be revisited.
    # Source: https://publicholidays.ie/2021-dates/
    holiday_options_2021 = [(1,1), (17,3), (5,4), (3,5),
            (7,6), (2,8), (25,10), (25,12), (26,12)]

    holiday = False
    for h_day, h_month in holiday_options_2021:
        holiday |= dt.day == h_day and dt.month == h_month
        
    return month, day, hour, school, rush_hour, weekend, holiday


####################
# Weather Features #
####################

def get_weather_features(target_dt):

    target_weather = weather.get_data(target_dt)

    try:
        # "rain" for the model is over 1hr, not 3, hence the division here.
        rain = float(target_weather["rain"]["3hr"])/3 if "rain" in target_weather else 0
        temp = float(target_weather["main"]["temp"])
        wdsp = float(target_weather["wind"]["speed"])
        vis = float(target_weather["visibility"])

    except:
        raise ValueError("Failed to parse data from weather API response.")

    # Open Weather gives temperature in Kelvin,
    # Dublin Bus had it in Celsius.
    temp = temp - 273.15 
    
    return rain, temp, wdsp, vis
