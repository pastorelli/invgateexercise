# -*- coding: utf-8 -*-
"""
    This module handles the connection to the twitter API.
"""
from __future__ import unicode_literals

from django.core.exceptions import ImproperlyConfigured
from requests_oauthlib import OAuth1Session

from api_keys import (
    CONSUMER_KEY, CONSUMER_SECRET,
    OAUTH_TOKEN, OAUTH_TOKEN_SECRET
)


class TwitterAPIConnector(object):

    def _get_oaut(self):
        if self._check_api_keys():
            return OAuth1Session(CONSUMER_KEY,
                                 client_secret=CONSUMER_SECRET,
                                 resource_owner_key=OAUTH_TOKEN,
                                 resource_owner_secret=OAUTH_TOKEN_SECRET)

    def _check_api_keys(self):
        if (not CONSUMER_KEY or not CONSUMER_SECRET or not
                OAUTH_TOKEN or not OAUTH_TOKEN_SECRET):
            raise ImproperlyConfigured("Twitter API Keys are missing")
        return True
