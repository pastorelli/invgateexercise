# -*- coding: utf-8 -*-
"""
    This module handles the connection to the twitter API.
"""
from __future__ import unicode_literals

import requests
from requests_oauthlib import OAuth1

from django.conf import settings

from .twitter_urls import TWITTER_PROFILE_URL

CONSUMER_KEY = settings.CONSUMER_KEY
CONSUMER_SECRET = settings.CONSUMER_SECRET

OAUTH_TOKEN = settings.OAUTH_TOKEN
OAUTH_TOKEN_SECRET = settings.OAUTH_TOKEN_SECRET


def check_api_keys():
    if (not CONSUMER_KEY or not CONSUMER_SECRET or not
            OAUTH_TOKEN or not OAUTH_TOKEN_SECRET):
        return False
    return True


class TwitterAPIConnector(object):

    def get_twitter_profile(self, twitter_username):
        url = "{}screen_name={}".format(TWITTER_PROFILE_URL, twitter_username)
        oauth = self._get_oaut()
        response = requests.get(url, auth=oauth)
        return {
            'twitter_content': response.content,
            'status': response.status_code
        }

    def _get_oaut(self):
        if check_api_keys():
            return OAuth1(CONSUMER_KEY,
                          client_secret=CONSUMER_SECRET,
                          resource_owner_key=OAUTH_TOKEN,
                          resource_owner_secret=OAUTH_TOKEN_SECRET)
