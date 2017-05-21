import json

from datetime import date, timedelta

from django.shortcuts import render

from .models import Appointment
from .serializers import FrameSerializer


def get_week(date):
    """
    Return the working days of the week containing the given date.

    @returns: iterator (!) of working days
    """
    day = date - timedelta(days=date.weekday())

    if date.weekday() > 4:
        # we vist the site on weekend, go to next week
        day += timedelta(days=7)
        
    for n in range(5):
        yield day
        day += timedelta(days=1)


def main_view(request):
    today = date.today()
    all_week = list(get_week(today))
    busy = Appointment.objects.get_for_period(all_week)
    serializer = FrameSerializer(busy, many=True)
    return render(
        request, 
        'main.html.j2',
        {
            'week': all_week,
            'appointments': [json.dumps(dict(data)) for data in serializer.data],
        }
    )
