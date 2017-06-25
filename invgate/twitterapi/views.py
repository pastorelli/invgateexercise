# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from braces.views import JSONResponseMixin
from django.http import HttpResponseBadRequest, HttpResponse
from django.views.generic import View

from .models import TwitterProfile


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

        twitter_profile = self._get_twitter_profile(username)
        if twitter_profile:
            return self.render_json_response(
                {
                    'data': self._twitter_profile_to_dict(twitter_profile)
                }
            )
        return HttpResponse("processing request", status=202)

    def _twitter_profile_to_dict(self, twitter_profile):
        return {
            'name': twitter_profile.name,
            'description': twitter_profile.short_description,
            'profile_pic_uri': twitter_profile.profile_pic_uri,
            'popularity_index': twitter_profile.popularity_index,
        }

    def _get_twitter_profile(self, username):
        try:
            return TwitterProfile.objects.get(name=username)
        except TwitterProfile.DoesNotExist:
            return None
