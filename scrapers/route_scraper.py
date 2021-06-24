import requests
from bs4 import BeautifulSoup
import json
import xmltodict
import pymysql
from decouple import config


# The route of 53a cannot be got from the api
stops_53a = {
    'outbound': [1172, 4380, 4509, 7705, 7708, 7709, 7710, 7711],
    'inbound': [512, 513, 4380, 6251, 7402, 7705, 7706, 7707]
}


def get_route():
    """Parse the html content from dublin bus webpage and return a list of all the routes"""

    url = 'https://www.dublinbus.ie/Your-Journey1/Timetables/'
    response = requests.get(url)
    resp = BeautifulSoup(response.text, "html.parser")
    routes = resp.findAll("td", attrs={"class": "RouteNumberColumn"})
    route_list = []
    for route in routes:
        r = route.find("a").text.strip()
        # There might be route like 68/a, which needs to be split into two subroutes 68 and 68a
        if '/' in r:
            num, letter = r.split('/')
            route_list.append(num)
            route_list.append(num+letter)
        else:
            route_list.append(r)
    return route_list


def get_stops(route, direction):
    """Return the stop list of input route and direction"""
    url = 'https://www.dublinbus.ie/Labs.EPiServer/GoogleMap/gmap_conf.aspx'
    payload = {'custompageid': 1219,
               'action': 'GetStops',
               'routeNumber': route,
               'direction': direction
               }
    response = requests.get(url, params=payload)
    stop_list = []
    if response.status_code == 200:
        for stop in xmltodict.parse(response.text[3:])['gmap']['data']['poi']:
            stop_id = int(stop['stopnumber'])
            stop_list.append(stop_id)
            cursor.execute("insert into RouteStops values(%s, %s, %s)", (route, direction, stop_id))
    return stop_list


conn = pymysql.connect(host=config('DB_URL'), port=3306, user=config('DB_USER'), password=config('DB_PASSWORD'), db="dublinbus")
cursor = conn.cursor()
route_list = get_route()
route_stop_dict = {}
route_stop_dict['53a'] = stops_53a
for route in route_list:
    if route == '40e':
        continue
    outbound_list = get_stops(route, 'O')
    inbound_list = get_stops(route, 'I')
    if len(outbound_list) != 0 or len(inbound_list) != 0:
        route_stop_dict[route] = {
            'outbound': outbound_list,
            'inbound': inbound_list
        }
conn.commit()
cursor.close()
conn.close()
with open('stops_by_route.json', 'w') as file:
    json.dump({'routes': route_stop_dict}, file, indent=2)
