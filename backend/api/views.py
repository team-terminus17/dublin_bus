from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from django.http import HttpResponse, JsonResponse
from .models import *
import json
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F


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

        current_stop = results.get(stop.external_id, None)
        if current_stop is None:
            current_stop = {
                "name": stop.name,
                "number": stop.number,
                "lat": stop.lat,
                "lng": stop.lon,
                "routes": list()
            }
            results[stop.external_id] = current_stop

        current_stop["routes"].append({
            "name": route_name,
            "direction": direction,
            "main": main,
            "agency": agency
        })
    
    return JsonResponse(results)


def get_shape(request, route, direction, dep_stop, arr_stop):
    """Take a route, two stops indices, return the array of shape corrdinates of the trip defined by the input"""
    dep_stop_entry = RouteStops.objects.get(name__name=route, direction=direction, stop_id=dep_stop).shape_id
    arr_stop_entry = RouteStops.objects.get(name__name=route, direction=direction, stop_id=arr_stop).shape_id
    dep_stop_entry = 100
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
