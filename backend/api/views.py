from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from django.http import HttpResponse, JsonResponse
from .models import *
import json
from django.views.decorators.csrf import csrf_exempt


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
    with open('scrapers/stops_by_route.json', 'r', encoding='utf-8') as file:
        route_dict = json.load(file)
    stop_list = route_dict[stop]
    stop_dict = {'stops': stop_list}
    # route_dict_detail = {}
    # if len(stop_list['inbound']) != 0:
    #     route_dict_detail['inbound'] = {}
    #     for s in stop_list['inbound']:
    #         route_dict_detail['inbound'][s] = Stops.objects.get(stopID=int(s)).dictify()
    # if len(stop_list['outbound']) != 0:
    #     route_dict_detail['outbound'] = {}
    #     for s in stop_list['outbound']:
    #         route_dict_detail['outbound'][s] = Stops.objects.get(stopID=int(s)).dictify()
    return HttpResponse(json.dumps(stop_dict, ensure_ascii=False), content_type='application/json')


def get_coordinates(request, route, stop_dep, stop_arr):
    """First verify if the route is valid, then get the coordinates of the arrival and departure stops"""
    res = dict()
    res['valid'] = 1
    if stop_dep == stop_arr:
        res['valid'] = 2
        return JsonResponse(res)
    stop_dep_list = RouteStops.objects.filter(routeID=route, stopID=int(stop_dep))
    if len(stop_dep_list) == 1:
        stop_arr_list = RouteStops.objects.filter(routeID=route, stopID=int(stop_arr), direction=stop_dep_list[0].direction)
        if len(stop_arr_list) == 0 or stop_dep_list[0].sequence > stop_arr_list[0].sequence:
            return JsonResponse(res)
    else:
        stop_dep_I = RouteStops.objects.get(routeID=route, stopID=int(stop_dep), direction='I')
        stop_dep_O = RouteStops.objects.get(routeID=route, stopID=int(stop_dep), direction='O')
        stop_arr_list = RouteStops.objects.filter(routeID=route, stopID=stop_arr)
        if stop_arr_list[0].direction == 'I':
            if stop_dep_I > stop_arr_list[0].sequence:
                return JsonResponse(res)
        else:
            if stop_dep_O > stop_arr_list[0].sequence:
                return JsonResponse(res)
    res['valid'] = 0
    res['stop_dep'] = Stops.objects.get(stopID=int(stop_dep)).dictify()
    res['stop_arr'] = Stops.objects.get(stopID=int(stop_arr)).dictify()
    return HttpResponse(json.dumps(res, ensure_ascii=False), content_type='application/json')


def predict_time(request, route, direction, arr_stop, dep_stop, datetime):
    """Take a route, two stops indices, a datetime. Return a predicted time taken."""
    direction_full = 'inbound' if direction == 'I' else 'outbound'
    with open('scrapers/stops_by_route2.json', 'r') as file:
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
    dummy = dict()
    dummy['time'] = 1
    return JsonResponse(dummy)


def get_weather(request):
    """Return weather information of current time"""
    weather = Weather.objects.all().order_by('weather_time')[0]
    return JsonResponse(weather.dictify())


@csrf_exempt
def get_journey_time(request):
    if request.method == 'POST':
        routes = json.loads(request.body.decode())
        print(routes)
    return HttpResponse(1)