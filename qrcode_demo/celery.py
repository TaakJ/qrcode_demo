from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qrcode_demo.settings')

app = Celery('qrcode_demo')
app.conf.enable_utc = False

app.conf.update(timezone='Asia/Bangkok')

app.config_from_object(settings, namespace='CELERY')

# Celery Beat Settings
app.conf.beat_schedule = {
    'push-message-every-day': {
        'task': "apps.home.tasks.push_message_job", 
        'schedule': crontab(hour=0, minute=0, day_of_month='*', month_of_year='*'),
    },
}

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')