from decouple import config
import requests
from datetime import datetime, timezone

from . import utils

API_KEY = config("OPEN_WEATHER_API_KEY")
CITY_NAME = "dublin"
URL = (
    "http://api.openweathermap.org/data/2.5/forecast"
    f"?q={CITY_NAME}&appid={API_KEY}"
)


def get_data(target_dt):

  target_dt = target_dt.astimezone(timezone.utc)

  try:
        response = requests.get(URL)
        response_data = response.json()["list"]
  except:
      raise ValueError("Failed to retrieve weather API data.")

  if len(response_data) == 0:
      raise ValueError("Weather API response contained no data.")

  # A prediction is returned for every 3hrs up to 5 days.
  # Choose the first one after the target time.
  for entry in response_data:
      try:
          dt = utils.utc_unix_to_dt(entry["dt"])
      except:
          raise ValueError("Failed to parse data from weather API response.")

      if target_dt < dt:
          target_weather = entry
          break
  else:
      # Default to the last entry if the target datetime is
      # beyond the forecast range.
      target_weather = response_data[-1]


  return target_weather


def get_summary():

  data = get_data(datetime.now())

  try:
    temp = float(data["main"]["temp"])
    icon = data["weather"][0]["icon"]
  except:
    raise ValueError("Failed to parse data from weather API response.")

  # Temperature is in Kelvin, we need it in Celsius
  temp -= 273.15

  return temp, icon