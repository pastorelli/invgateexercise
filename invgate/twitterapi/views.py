# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from braces.views import JSONResponseMixin
from django.http import HttpResponseBadRequest
from django.views.generic import View

from .models import TwitterProfile
from .twitter_connector import TwitterAPIConnector


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
                })
        response = self._request_profile_twitter_api(username)
        if response['status'] == 404:
            return HttpResponseBadRequest(
                "Twitter username doesnt exist")
        if response['status'] == 401:
            return HttpResponseBadRequest(
                "Twitter API token invalid")
        if response['status'] == 200:
            twitter_profile = self._parse_twitter_profile(
                username,
                response['twitter_content'])
        return self.render_json_response(
            {
                'data': self._twitter_profile_to_dict(twitter_profile)
            })
        # return HttpResponseBadRequest(response['twitter_content'])

    def _request_profile_twitter_api(self, username):
        connector = TwitterAPIConnector()
        return connector.get_twitter_profile(username)

    def _parse_twitter_profile(self, username, twitter_profile_data):
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
