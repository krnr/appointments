import datetime
import json

from django.core.urlresolvers import resolve
from django.test import TestCase
from rest_framework.serializers import ValidationError
from rest_framework.test import APITestCase

from .models import Appointment
from .serializers import DATE_ERROR_MESSAGE, TIME_ERROR_MESSAGE
from .views import main_view


class AppointmentModelTestCase(TestCase):
    """docstring"""
    appt_dict = {
        'date': datetime.date.today().isoformat(),
        'time_start': "13:30",
        'non_recurring': "Anon",
        'reason': "I broke a leg"
    }

    def test_appointment_saved_with_time_end(self):
        existing = Appointment.objects.create(**self.appt_dict)
        self.assertEqual(existing.time_end, datetime.time(13, 59))


class MainViewTestCase(TestCase):
    """Smoke tests"""
    def test_index_resolve_correct_view(self):
        view = resolve('/')
        self.assertEqual(view.func, main_view)

    def test_index_renders_correct_html(self):
        resp = self.client.get('/')
        self.assertIn(b'Dr. Dre\'s', resp.content)


class AppointmentAPITestCase(APITestCase):
    """docstring for AppointmentAPITestCase"""
    endpoint = '/api/v1/appointment/'
    appt_dict = {
        'date': datetime.date.today().isoformat(),
        'time_start': "13:30",
        'non_recurring': "Anon",
        'reason': "I broke a leg"
    }

    def test_anonymous_user_can_create_appointment(self):
        resp = self.client.post(self.endpoint, self.appt_dict)
        self.assertEqual(resp.status_code, 201)
        appt = Appointment.objects.first()
        self.assertEqual(appt.reason, self.appt_dict['reason'])
        self.assertEqual(appt.non_recurring, self.appt_dict['non_recurring'])
        self.assertIsNone(appt.visitor)

    def test_appointments_cant_be_in_past(self):
        appt_dict = dict(self.appt_dict)
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        appt_dict['date'] = yesterday.isoformat()
        resp = self.client.post(self.endpoint, appt_dict)
        self.assertJSONEqual(resp.content.decode('utf-8'),
                             {"date":[DATE_ERROR_MESSAGE]})
        self.assertFalse(Appointment.objects.exists())

    def test_appointments_cant_be_in_wrong_hours(self):
        appt_dict = dict(self.appt_dict)
        appt_dict['time_start'] = "07:00"
        resp = self.client.post(self.endpoint, appt_dict)
        self.assertJSONEqual(resp.content.decode('utf-8'),
                             {"time_start":[TIME_ERROR_MESSAGE]})
        self.assertFalse(Appointment.objects.exists())

    def test_appointments_cant_be_closer_than_30_mins(self):
        Appointment.objects.create(**self.appt_dict)
        before = dict(self.appt_dict)
        before['time_start'] = "13:01"
        after = dict(self.appt_dict)
        after['time_start'] = "13:59"
        self.client.post(self.endpoint, before)
        self.client.post(self.endpoint, after)
        self.assertEqual(Appointment.objects.count(), 1)
    
    def test_user_cant_edit_appointment(self):
        existing = Appointment.objects.create(**self.appt_dict)
        edit = {'reason': "Malicious edit"}
        resp = self.client.patch(self.endpoint + str(existing.id), edit)
        self.assertEqual(resp.status_code, 405)
        self.assertEqual(Appointment.objects.first().reason,
                         existing.reason)

    def test_user_cant_delete_appointment(self):
        existing = Appointment.objects.create(**self.appt_dict)
        before = Appointment.objects.count()
        resp = self.client.delete(self.endpoint + str(existing.id))
        self.assertEqual(resp.status_code, 405)
        after = Appointment.objects.count()
        self.assertTrue(Appointment.objects.exists())
        self.assertEqual(before, after)
