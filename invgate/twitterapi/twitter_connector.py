# -*- coding: utf-8 -*-
"""
    This module handles the connection to the twitter API.
"""
from __future__ import unicode_literals

import requests
from requests_oauthlib import OAuth1

from django.core.exceptions import ImproperlyConfigured

from .api_keys import (CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN,
                       OAUTH_TOKEN_SECRET)
from .twitter_urls import TWITTER_PROFILE_URL


class TwitterAPIConnector(object):

    def get_twitter_profile(self, twitter_username):
        url = "{}screen_name={}".format(TWITTER_PROFILE_URL, twitter_username)
        oauth = self._get_oaut()
        response = requests.get(url, auth=oauth)
        json_response = response.json()
        if response.status_code == 200:
            return {
                'twitter_profile': json_response,
                'status': 200
            }
        return {
            'twitter_content': json_response,
            'status': response.status_code
        }

    def _get_oaut(self):
        if self._check_api_keys():
            return OAuth1(CONSUMER_KEY,
                          client_secret=CONSUMER_SECRET,
                          resource_owner_key=OAUTH_TOKEN,
                          resource_owner_secret=OAUTH_TOKEN_SECRET)

    def _check_api_keys(self):
        if (not CONSUMER_KEY or not CONSUMER_SECRET or not
                OAUTH_TOKEN or not OAUTH_TOKEN_SECRET):
            raise ImproperlyConfigured("Twitter API Keys are missing")
        return True
