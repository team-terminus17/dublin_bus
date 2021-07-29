import requests, os
from decouple import config

def get_realtime_data():
  
    headers = {
        'Cache-Control': 'no-cache',
        'x-api-key': config("GTFSR_API_KEY")
    }

    response = requests.get("https://gtfsr.transportforireland.ie/v1/?format=json", headers=headers)
    data = response.json()

    try:
        data = parse(data)
    except:
        # This could be because the incoming data has been corrupted 
        # in some way. Or because I've not considered an edge case. Or
        # maybe because the standard changed. (This is unlikely in the
        # space of a few weeks)
        raise ValueError("Unable to parse incoming GTFS-R data")

    return data


def parse(data):
    
    result = dict()
    
    for update_item in data["entity"]:
        
        try:
            stop_times = update_item["trip_update"]["stop_time_update"]
            trip_id = update_item["trip_update"]["trip"]["trip_id"]
        except:
          # There is nothing much we can do if there is this data is missing
          # At some point, it might be worth creating proper logging
          # here, in case the GTFS-R standard changes or something like that?
          continue
        
        for trip_stop in stop_times:
        
            sequence = trip_stop["stop_sequence"]

            try:
                arrival_delay = trip_stop["arrival"]["delay"]
            except:
                arrival_delay = 0
            
            try:
                departure_delay = trip_stop["departure"]["delay"]
            except:
                departure_delay = 0

            if arrival_delay == 0 and departure_delay == 0:
                continue

            result[(trip_id, sequence)] = (arrival_delay, departure_delay)

    return result
    