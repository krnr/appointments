from datetime import date, timedelta

from django.shortcuts import render

# Create your views here.


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
    return render(
        request, 
        'main.html.j2',
        {
            'week': list(get_week(today)),
        }
    )
