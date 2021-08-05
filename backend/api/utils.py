from datetime import datetime, date

def add_time(time, delta):
  
  # A bit of an awkward workaround, see:
  # https://stackoverflow.com/questions/656297/python-time-timedelta-equivalent

  dt = datetime.combine(date.today(), time)
  dt += delta
  
  return dt.time()