# coding: utf-8
# __author__: u"John"
from __future__ import unicode_literals, print_function, absolute_import
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

celery_app = Celery("mysite")
celery_app.config_from_object("django.conf:settings", namespace="CELERY")
celery_app.autodiscover_tasks()
