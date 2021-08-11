from datetime import datetime, date, timedelta, timezone


def add_time(time, delta):
  
  # A bit of an awkward workaround, see:
  # https://stackoverflow.com/questions/656297/python-time-timedelta-equivalent

  dt = datetime.combine(date.today(), time)
  dt += delta
  
  return dt.time()


def minus_time(time1, time2):

  dt1 = datetime.combine(date.today(), time1)
  dt2 = datetime.combine(date.today(), time2)

  return dt1-dt2


def utc_unix_to_dt(unix_seconds):

    # 'Unix time' is the number of seconds since 1/1/1970
    
    dt = datetime(1970, 1, 1, tzinfo=timezone.utc) 
    dt += timedelta(seconds=unix_seconds)

    return dt
