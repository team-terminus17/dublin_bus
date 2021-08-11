from datetime import datetime
from .models import *


def get_active_services(date=None):
    """
    Returns a QuerySet which selects the IDs of services
    that are active today. It is used to filter the trips table down to
    those relevant to the give date.

    'date' will default to the current date if no value is given for it.
    """

    weekdays = ["monday", "tuesday", "wednesday", 
        "thursday", "friday", "saturday", "sunday"]

    if date is None:
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
