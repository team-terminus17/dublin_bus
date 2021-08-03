from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F, Subquery

from datetime import datetime
import json

from .models import *
from . import gtfs_r


# Serve Vue Application
index_view = never_cache(TemplateView.as_view(template_name='index.html'))


def get_routes(request):
    """Return json of available bus routes"""
    route_list = list(Routes.objects.filter(agency__external_id="978").distinct().values_list('name__name', flat=True))
    route_dict = {'routes': sorted(route_list)}
    return JsonResponse(route_dict)


def get_stops(request, stop, direction):
    """Return json of available bus stops for a single route and direction"""
    stop_list = list(RouteStops.objects.filter(name__name=stop, direction=direction, main=True, agency__external_id="978")
                     .order_by('sequence').values(stopID=F('stop_id'), stopNumber=F('stop__number'), stopName=F('stop__name')))
    stop_dict = {'stops': stop_list}
    return HttpResponse(json.dumps(stop_dict, ensure_ascii=False), content_type='application/json')


def get_coordinates(request, direction, route, stop_dep, stop_arr):
    """First verify if the route is valid, then get the coordinates of the arrival and departure stops"""
    res = dict()
    if stop_dep == stop_arr:
        res['valid'] = 2
        return JsonResponse(res)
    seq_dep = RouteStops.objects.get(name__name=route, direction=direction, stop_id=stop_dep).sequence
    seq_arr = RouteStops.objects.get(name__name=route, direction=direction, stop_id=stop_arr).sequence
    # If the arrival stop is ahead of departure stop, the input route is invalid
    if seq_dep > seq_arr:
        res['valid'] = 1
        return JsonResponse(res)
    res['valid'] = 0
    res['stop_dep'] = Stops.objects.get(id=stop_dep).dictify()
    res['stop_arr'] = Stops.objects.get(id=stop_arr).dictify()
    return HttpResponse(json.dumps(res, ensure_ascii=False), content_type='application/json')


def predict_time(request, route, direction, dep_stop, arr_stop, datetime):
    """Return the predicted time from model in json format"""
    time_predict = model_predict(route, direction, dep_stop, arr_stop, datetime)
    dummy = dict()
    dummy['time'] = time_predict
    return JsonResponse(dummy)


def get_weather(request):
    """Return weather information of current time"""
    weather = Weather.objects.all().order_by('weather_time')[0]
    return JsonResponse(weather.dictify())


@csrf_exempt
def get_journey_time(request):
    """Retrieve information given by google directions api and returns the predicted time from the model"""
    if request.method == 'POST':
        routes = json.loads(request.body.decode())
        route = routes['routeID']
        time_predict = routes['googleTime']
        timestamp = routes['datetime']
        # Direction info is not provided by google so we need to get it ourselves

        for direction in [0, 1]:
            # For each direction, check if we could find the departure stop and arrival stop given the corresponding
            # names given by google.
            dep_stop = RouteStops.objects.filter(name__name=route,
                                                 stop__external_name__contains=routes['departureStop'],
                                                 agency__external_id="978", main=True, direction=direction)
            arr_stop = RouteStops.objects.filter(name__name=route, stop__external_name__contains=routes['arrStop'],
                                                 agency__external_id="978", main=True, direction=direction)

            if dep_stop.count() == 1 and arr_stop.count() == 1:
                # To confirm the queried result is valid
                if dep_stop.first().sequence < arr_stop.first().sequence:
                    dep_stop_id = dep_stop.first().stop_id
                    arr_stop_id = arr_stop.first().stop_id
                    time_predict = model_predict(route, direction, dep_stop_id, arr_stop_id, timestamp)
                    break
        # If we could not find a valid id pair for departure stop and arrival stop, return the
        # predicted time given by google
    return JsonResponse({'time': time_predict})


def get_stop_info(request, agency="all", route="all"):
    """
    Retrieve information on stops. Returns all stops by default,
    but has optional filters for agency and route.

    The agency filter should be the GTFS ID for the agency - e.g. '978' for Dublin Bus.
    The route filter should be the short name for the route, with caps - e.g. '46A'.

    Returns stop names, positions, and the routes/agencies they are associated.
    """

    # Retrieve the info in a single query with 3 inner joins and up to two
    # where clauses.

    entries = RouteStops.objects.select_related("stop", "name", "agency").all()

    if agency != "all":
        entries = entries.filter(agency__external_id=agency)

    if route != "all":
        entries = entries.filter(name__name=route)

    # Format the results for the frontend.

    results = dict()

    for entry in entries:

        stop = entry.stop
        route_name = entry.name.name
        direction = entry.direction
        main = entry.main
        agency = entry.agency.external_id
        sequence = entry.sequence

        current_stop = results.get(stop.id, None)
        if current_stop is None:
            current_stop = {
                "ID": stop.id,
                "gtfsID": stop.external_id,
                "name": stop.name,
                "number": stop.number,
                "lat": stop.lat,
                "lng": stop.lon,
                "routes": list()
            }
            results[stop.id] = current_stop

        current_stop["routes"].append({
            "name": route_name,
            "direction": direction,
            "main": main,
            "agency": agency,
            "sequence": sequence
        })

    # Sending lists as opposed to objects is actually insecure, hence
    # django's requirement that safe=False be passed.
    # This is not sensitive data though, so that is fine.
    return JsonResponse(list(results.values()), safe=False)


def get_bus_positions(request, agency, route):
    """
    Retrieve information on active trips for a given route.

    The agency should be the GTFS ID - 978 for Dublin bus for example.
    The route should be a short name in capitals - 46A for example.

    Returns a json array. Each object contains the trip id, start stop, end
    stop, and departure/arrival times for the segment the trip is currently
    on.
    """

    # Retrieve all trip stops for this route in two queries.
    # First, determine active services

    services = get_active_services()

    # Define a subquery for trips for the given services, route and agency

    trips = Trips.objects.select_related("route", 
        "route__agency", "route__name")
    trips = trips.filter(service_id__in=services, 
        route__agency__external_id=agency, route__name__name=route)

    # Collect stoptime entries whose trip id is in the result of
    # the above subquery. (Django does the subquery and this in one go.)

    trip_ids = trips.values_list("id", flat=True)
    trip_stops = StopTimes.objects.filter(trip_id__in=trip_ids)
    trip_stops = trip_stops.select_related("trip").only("trip__external_id", 
        "trip_id", "stop_sequence", "trip__direction",
        "stop_id", "arrival_time", "departure_time")

    # Collect all results, allow lookup by trip_id and sequence number

    trip_times = dict()
    trip_directions = dict()

    for entry in trip_stops:
        trip = trip_times.setdefault(entry.trip_id, dict())
        trip[entry.stop_sequence] = {
            "ID": entry.stop_id, 
            "gtfsID": entry.trip.external_id,
            "arrivalTime": entry.arrival_time,
            "departureTime": entry.departure_time,
        }
        trip_directions[entry.trip_id] = entry.trip.direction

    # Collect realtime adjustments to the schedule

    realtime_lookup = gtfs_r.get_realtime_data()

    for trip in trip_times.values():
        for seq, stop in trip.items():
            update = realtime_lookup.get((stop["gtfsID"], seq), None)
            if update is not None:
                arr, dep = update
                stop["arrivalTime"] += arr
                stop["departureTime"] += dep

    # The sequence numbers aren't perfect, they can jump sometimes.
    # Fix that here by storing them as a list

    trip_times_v2 = dict()

    for trip_id, trip in trip_times.items():
        stop_sequence = list()
        for seq in sorted(trip.keys()):
            stop_sequence.append(trip[seq])
        trip_times_v2[trip_id] = stop_sequence

    # Extract the next and current stops for each trip.
    # Format the result for the frontend.

    current_time = datetime.now().time()
    data = list()

    for trip_id, trip in trip_times_v2.items():

        next_stop_index = None
        for i, stop in enumerate(trip):
            if stop["arrivalTime"] >= current_time:
                next_stop_index = i
                break

        # None means the trip is over, 0 means the trip
        # has yet to start.
        if next_stop_index is None or next_stop_index == 0:
            continue

        current_stop = trip[next_stop_index - 1]
        next_stop = trip[next_stop_index]

        data.append({
            "trip": trip_id,
            "currentStop":  current_stop["ID"],
            "nextStop": next_stop["ID"],
            "departureTime": current_stop["departureTime"],
            "arrivalTime": next_stop["arrivalTime"],
            "direction": trip_directions[trip_id]
        })

    return JsonResponse(data, safe=False)


def get_stop_trips(request, stop):

    active_services = get_active_services()
    active_trips = Trips.objects\
        .filter(service_id__in=active_services)\
        .values_list("id", flat=True)

    # There are about 30,000 trips that are active at any given time. 
    # Ideally this would be used as a subquery, though I'm not sure how to
    # get Django to do so. The speedup would only be aout 150ms though
    # so it's not a major concern.

    stoptimes = StopTimes.objects.select_related("trip")\
        .filter(trip_id__in=Subquery(active_trips), stop_id=stop)\
        .select_related("trip__route__name")\
        .order_by("arrival_time")

    realtime_lookup = gtfs_r.get_realtime_data()

    trips = list()

    for entry in stoptimes:
        
        arrival_time = entry.arrival_time
        
        update = realtime_lookup.get((entry.trip_id, entry.stop_sequence), None)
        if update is not None:
            arrival_delay = update[0]
            arrival_time += arrival_delay

        if arrival_time < datetime.now().time():
            continue

        trips.append({
            "tripID": entry.trip_id,
            "arrivalTime": arrival_time,
            "routeName": entry.trip.route.name.name,
            "tripHeadsign": entry.trip.headsign
        })

    return JsonResponse(trips, safe=False)



def get_active_services():
    """
    Returns a QuerySet which selects the IDs of services
    that are active today. It is used to filter the trips table down to
    those relevant to today.
    """
    # At some point this will need to work on a day that is not today?
    # That's easy enough to change when the need arises though.

    weekdays = ["monday", "tuesday", "wednesday", 
        "thursday", "friday", "saturday", "sunday"]

    date = datetime.now()
    weekday = weekdays[date.weekday()]

    # It's unfortunate to have raw SQL here,
    # but I don't think the Django ORM feature supports anything like the
    # multiple left join below.

    services = Services.objects.raw(
        "SELECT api_services.id FROM api_services"
        # Optionally include an exception corresponding to today.
        " LEFT JOIN api_serviceexceptions"
            " ON api_services.id = api_serviceexceptions.service_id"
            " AND api_serviceexceptions.date = %s"
        " WHERE start_date <= %s" 
            " AND end_date >= %s"
            f" AND {weekday} = 1"
            # The service is active if the optional exception is null.
            " AND api_serviceexceptions.id IS NULL",
        [date, date, date]
    )

    return services


def get_shape(request, route, direction, dep_stop, arr_stop):
    """Take a route, two stops indices, return the array of shape corrdinates of the trip defined by the input"""
    dep_stop_entry = RouteStops.objects.get(name__name=route, direction=direction, stop_id=dep_stop).shape_id
    arr_stop_entry = RouteStops.objects.get(name__name=route, direction=direction, stop_id=arr_stop).shape_id
    coordinates_list = list(Shapes.objects.filter(id__gte=dep_stop_entry, id__lte=arr_stop_entry)
                            .values('lat', lng=F('lon')))
    coordinates_dict = {'coordinates': coordinates_list}
    return JsonResponse(coordinates_dict)


def model_predict(route, direction, dep_stop, arr_stop, datetime):
    """Take a route, two stops indices, a datetime. Return a predicted time taken."""
    dep_stop_seq = RouteStops.objects.get(name__name=route, direction=direction, stop_id=dep_stop).sequence
    arr_stop_seq = RouteStops.objects.get(name__name=route, direction=direction, stop_id=arr_stop).sequence
    stop_list = list(RouteStops.objects.filter(name__name=route, direction=direction,
                                               sequence__gte=dep_stop_seq, sequence__lte=arr_stop_seq)
                     .values_list('stop__number', flat=True))
    # First we need to find the predicted weather of the time closet to the input datetime.
    # If it exceeds the limit of the prediction, we just get current weather info
    weather = Weather.objects.filter(weather_time__gte=datetime).order_by('weather_time')
    if len(weather) == 0:
        weather = Weather.objects.all().order_by('weather_time')
    weather = weather[0]
    stop_ret = {'stops': stop_list, 'weather': weather.dictify()}
    time_predict = 1
    return time_predict
