# -*- coding: utf-8 -*-
"""
    This module handles the connection to the twitter API.
"""
from __future__ import unicode_literals

from django.core.exceptions import ImproperlyConfigured

from twitterapi import api_keys


class TwitterAPIConnector(object):

    def _check_api_keys(self):
        if (not api_keys.CONSUMER_KEY or not api_keys.CONSUMER_SECRET or not
                api_keys.OAUTH_TOKEN or not api_keys.OAUTH_TOKEN_SECRET):
            raise ImproperlyConfigured("Twitter API Keys are missing")
        return True
