
import os
from celery import Celery
from celery.decorators import periodic_task
from celery.task.schedules import crontab
from django.apps import apps, AppConfig
from django.conf import settings


if not settings.configured:
    # set the default Django settings module for the 'celery' program.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')  # pragma: no cover


app = Celery('dr_dre')


class CeleryConfig(AppConfig):
    name = 'dr_dre.taskapp'
    verbose_name = 'Celery Config'

    def ready(self):
        # Using a string here means the worker will not have to
        # pickle the object when using Windows.
        app.config_from_object('django.conf:settings')
        installed_apps = [app_config.name for app_config in apps.get_app_configs()]
        app.autodiscover_tasks(lambda: installed_apps, force=True)

        if hasattr(settings, 'RAVEN_CONFIG'):
            # Celery signal registration
# Since raven is required in production only,
            # imports might (most surely will) be wiped out
            # during PyCharm code clean up started
            # in other environments.
            # @formatter:off
            from raven import Client as RavenClient
            from raven.contrib.celery import register_signal as raven_register_signal
            from raven.contrib.celery import register_logger_signal as raven_register_logger_signal
# @formatter:on

            raven_client = RavenClient(dsn=settings.RAVEN_CONFIG['DSN'])
            raven_register_logger_signal(raven_client)
            raven_register_signal(raven_client)


@periodic_task(run_every=(crontab(minute='0', hour='7')), name="todays_appts", ignore_result=True)
def send_todays_appts(self):
    """
    Every morning before start working doctor gets appointments for today
    """
    from django.core.mail import mail_managers
    from django.utils import timezone
    from ..appointments.models import Appointment

    today = timezone.now().date()
    appts = Appointment.objects.filter(date=today).order_by('time_start')

    if appts:
        message = "Here're your patients for today:\n"
        for appt in appts:
            message += "* {} - {}. Issue: {}".format(
                appt.time_start, 
                appt.non_recurring,
                appt.reason
            )
    else:
        message = "You do not have appointments for today."

    mail_managers("Appointments for {0:%d} {0:%B}".format(today), 
                  message)
