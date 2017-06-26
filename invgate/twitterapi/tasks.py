# -*- coding: utf-8 -*-
"""
    Celery task that excecute the twitter request asyncronous.
"""
from __future__ import absolute_import, unicode_literals

from celery import shared_task
from django.core.exceptions import ImproperlyConfigured

from .models import TwitterTaskStatus
from .twitter_connector import TwitterAPIConnector


@shared_task
def request_twitter_profile_task(username):
    connector = TwitterAPIConnector()
    response = connector.get_twitter_profile(username)

    twitter_task_status = TwitterTaskStatus.objects.get(
        username=username
    )
    twitter_task_status.status = response['status']
    twitter_task_status.twitter_response = response['twitter_content']
    twitter_task_status.save()
    return twitter_task_status
