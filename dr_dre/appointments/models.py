import datetime

from django.conf import settings
from django.db import models


def add_mins_to_time(time_str, mins):
    """

    >>> add_mins_to_time("13:01", 20)
    datetime.time(13, 21)

    >>> add_mins_to_time("23:59", 20)
    datetime.time(1, 19)

    @param time_obj: str in format "%H:%M"
    @param mins: int of mins to add
    """
    dummy = datetime.datetime.strptime(time_str, "%H:%M")
    added = dummy + datetime.timedelta(minutes=mins)
    return added.time()


class Appointment(models.Model):
    """docstring for Appointment"""
    visitor = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    non_recurring = models.CharField(max_length=127, blank=True, null=True)
    date = models.DateField(default=datetime.date.today, db_index=True)
    time_start = models.TimeField(db_index=True)
    time_end = models.TimeField(blank=True, db_index=True)
    reason = models.TextField(default='Not stated')

    class Meta:
        unique_together = (
            ('date', 'time_start'),
        )

    def __str__(self):
        visitor = self.non_recurring or self.visitor
        return 'Appointment for {} at {} {}'.format(
            visitor, self.time_start, self.date
        )

    def save(self, **kwargs):
        # all visits last 30 mins by default
        if not self.time_end:
            try:
                time = self.time_start.strftime('%H:%M')
                self.time_end = add_mins_to_time(time, 29)
            except AttributeError:
                # string instead of time() case
                self.time_end = add_mins_to_time(self.time_start, 29)

        super(Appointment, self).save(**kwargs)
    