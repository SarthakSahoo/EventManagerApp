from __future__ import absolute_import, unicode_literals

from celery import Celery

import os

import gqldemo.constants as gc

# set the default Django settings module for the 'Celery' program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gqldemo.settings')

# Creating the app with Name of the Project
app=Celery(gc.project_name)

# Make Celery to use django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Also, checks if there is any task entered to queue
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

# Setting the Celery beat schedule
app.conf.beat_schedule = {
    # Naming the beat task name
    'send-email-in-every-one-minute': {
        # Defining the task name defined 
        # and the interval on which the task
        # will be executed which could be changed
        # further depending on the requirement.
        'task': 'all_event_mail',
        'schedule': 60.0
    }
}
