import datetime

from django.conf import settings
from rest_framework import serializers

from .models import Appointment


DATE_ERROR_MESSAGE = "Date is past today"
TIME_ERROR_MESSAGE = "Doctor gets visitors only in working hours"


class AppointmentSerializer(serializers.HyperlinkedModelSerializer):
    time_start = serializers.TimeField(format="%H:%M")

    class Meta:
        model = Appointment
        fields = ('non_recurring', 'date', 'time_start', 'reason')

    def validate_date(self, data):
        if not data >= datetime.date.today():
            raise serializers.ValidationError(DATE_ERROR_MESSAGE)
        return data

    def validate_time_start(self, data):
        start, end = settings.WORKING_HOURS
        worktime = start <= data <= end
        if not worktime:
            raise serializers.ValidationError(TIME_ERROR_MESSAGE)
        return data


class FrameSerializer(serializers.HyperlinkedModelSerializer):
    hour_start = serializers.SerializerMethodField()
    min_start = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = ('date', 'hour_start', 'min_start')

    def get_hour_start(self, obj):
        return obj.time_start.hour

    def get_min_start(self, obj):
        return "%02d" % obj.time_start.minute
