# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ImproperlyConfigured
from django.views.generic import View

from twitterapi import api_keys


class RetrieveTwitterProfileView(View):
    """
        Returns the twitter profile requested,
        if the twitter profile doesn't exists in
        the database it makes the request to the job handler.
    """

    def _check_api_keys(self):
        if (not api_keys.CONSUMER_KEY or not api_keys.CONSUMER_SECRET or not
                api_keys.OAUTH_TOKEN or not api_keys.OAUTH_TOKEN_SECRET):
            raise ImproperlyConfigured("Twitter API Keys are missing")
        return True
