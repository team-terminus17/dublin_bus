import requests
import pymysql
from decouple import config


def scrape():
    conn = pymysql.connect(host=config('DB_HOST'), port=3306, user=config('DB_USER'), password=config('DB_PASSWORD'), db=config('DB_NAME'))
    cursor = conn.cursor()
    url = 'http://api.openweathermap.org/data/2.5/forecast'
    payload = {'id': 2964574,
               'APPID': config('WEATHER_API')
              }
    response = requests.get(url, params=payload)
    print(response.status_code)
    if response.status_code == 200:
        weather_info = response.json()['list']
        cursor.execute('delete from futureweather')
        conn.commit()
        for weather in weather_info:
            weather_time = weather['dt']
            temp = weather['main']['temp'] - 273.15
            rain = 'rain' in weather
            icon = weather['weather'][0]['icon']
            cursor.execute("insert into futureweather values(%s, %s, %s, %s)", (weather_time, temp, rain, icon))
            conn.commit()
    cursor.close()
    conn.close()
