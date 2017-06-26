# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

from braces.views import JSONResponseMixin
from django.http import (HttpResponseBadRequest, HttpResponse,
                         HttpResponseNotFound)
from django.views.generic import View
from django.core.exceptions import ImproperlyConfigured

from .models import TwitterProfile, TwitterTaskStatus
from .tasks import request_twitter_profile_task
from .twitter_connector import check_api_keys


class RetrieveTwitterProfileView(JSONResponseMixin, View):
    """
        Returns the twitter profile requested,
        if the twitter profile doesn't exists in
        the database it makes the request to the job handler.
    """
    http_method_names = [u'get']

    def get(self, request):
        username = self.request.GET.get('username', None)
        if not username:
            return HttpResponseBadRequest(
                "Twitter username expected as a GET param")

        if not check_api_keys():
            return HttpResponse("Twitter API keys not configured",
                                status=503)

        # Check if the profile already exists
        twitter_profile = self._get_twitter_profile(username)
        if twitter_profile:
            return self.render_json_response(
                {
                    'data': self._twitter_profile_to_dict(twitter_profile)
                })

        # Check if there is already a job for this profile
        twitter_task_profile = self._get_twitter_task_status(username)
        if twitter_task_profile:
            if twitter_task_profile.status == 404:
                twitter_task_profile.delete()
                return HttpResponseNotFound(
                    "Twitter username doesnt exist")
            if twitter_task_profile.status == 401:
                twitter_task_profile.delete()
                return HttpResponse("Twitter API token invalid", status=401)
            if twitter_task_profile.status == 202:
                return HttpResponse("processing request", status=202)
            if twitter_task_profile.status == 200:
                twitter_profile = self._parse_twitter_profile(
                    username,
                    twitter_task_profile.twitter_response)
                twitter_task_profile.delete()
                return self.render_json_response(
                    {
                        'data': self._twitter_profile_to_dict(twitter_profile)
                    })
            return HttpResponse(twitter_task_profile.twitter_response,
                                status=twitter_task_profile.status)

        # If there are no jobs create one
        job_id = request_twitter_profile_task.delay(username)
        twitter_task_status = TwitterTaskStatus(
            username=username, job=str(job_id))
        twitter_task_status.save()
        return HttpResponse("processing request", status=202)

    def _parse_twitter_profile(self, username, twitter_profile_data):
        twitter_profile_data = json.loads(twitter_profile_data)
        twitter_profile = TwitterProfile(
            username=username,
            name=twitter_profile_data.get('name', ''),
            short_description=twitter_profile_data.get('description', ''),
            profile_pic_uri=twitter_profile_data.get('profile_image_url', ''),
            popularity_index=twitter_profile_data.get('followers_count', 0),
        )
        twitter_profile.save()
        return twitter_profile

    def _twitter_profile_to_dict(self, twitter_profile):
        return {
            'name': twitter_profile.name,
            'description': twitter_profile.short_description,
            'profile_pic_uri': twitter_profile.profile_pic_uri,
            'popularity_index': twitter_profile.popularity_index,
        }

    def _get_twitter_profile(self, username):
        try:
            return TwitterProfile.objects.get(username=username)
        except TwitterProfile.DoesNotExist:
            return None

    def _get_twitter_task_status(self, username):
        try:
            return TwitterTaskStatus.objects.get(username=username)
        except TwitterTaskStatus.DoesNotExist:
            return None
