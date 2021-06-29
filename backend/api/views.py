from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from django.http import HttpResponse, JsonResponse
from .models import *
import json

# Serve Vue Application
index_view = never_cache(TemplateView.as_view(template_name='index.html'))


def test_message(request):
    """Dummy message to check if the backend and frontend can communicate"""
    return HttpResponse("Hello from the backend!")


def test_db(request):
    """Dummy message to check if the database is integrated successfully"""
    stops = RouteStops.objects.all()
    return HttpResponse(stops)


def get_routes(request):
    """Return json of available bus routes"""
    with open('scrapers/routes.json', 'r') as file:
        return JsonResponse(json.load(file))


def get_stops(request, stop):
    """Return json of available bus stops for a single route"""
    route_dict = {}
    with open('scrapers/stops_by_route.json', 'r') as file:
        route_dict = json.load(file)
    stop_list = route_dict['routes'][stop]
    route_dict_detail = {}
    if len(stop_list['inbound']) != 0:
        route_dict_detail['inbound'] = {}
        for s in stop_list['inbound']:
            route_dict_detail['inbound'][s] = Stops.objects.get(stopID=int(s)).dictify()
    if len(stop_list['outbound']) != 0:
        route_dict_detail['outbound'] = {}
        for s in stop_list['outbound']:
            route_dict_detail['outbound'][s] = Stops.objects.get(stopID=int(s)).dictify()
    return JsonResponse(route_dict_detail)


def predict_time(request, route, direction, arr_stop, dep_stop, datetime):
    """Take a route, two stops indices, a datetime. Return a predicted time taken."""
    direction_full = 'inbound' if direction == 'I' else 'outbound'
    with open('scrapers/stops_by_route.json', 'r') as file:
        route_dict = json.load(file)
    dep_stop_seq = RouteStops.objects.get(routeID=route, direction=direction, stopID=dep_stop).sequence
    arr_stop_seq = RouteStops.objects.get(routeID=route, direction=direction, stopID=arr_stop).sequence
    stop_list = route_dict['routes'][route][direction_full][dep_stop_seq:arr_stop_seq+1]
    # First we need to find the predicted weather of the time closet to the input datetime.
    # If it exceeds the limit of the prediction, we just get current weather info
    weather = Weather.objects.filter(weather_time__gte=datetime).order_by('weather_time')
    if len(weather) == 0:
        weather = Weather.objects.all().order_by('weather_time')
    weather = weather[0]
    stop_ret = {'stops': stop_list, 'weather': weather.dictify()}
    return JsonResponse(stop_ret)


def get_weather(request):
    """Return weather information of current time"""
    weather = Weather.objects.all().order_by('weather_time')[0]
    return JsonResponse(weather.dictify())

