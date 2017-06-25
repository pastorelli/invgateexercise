# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase

from twitterapi import api_keys
from ..twitter_connector import TwitterAPIConnector


class TwitterAPIConnectorTest(TestCase):

    def test_consumer_key_missing_return_improperly_configured(self):
        api_keys.CONSUMER_KEY = None
        connector = TwitterAPIConnector()
        with self.assertRaises(ImproperlyConfigured):
            connector._check_api_keys()

    def test_consumer_secret_missing_return_improperly_configured(self):
        api_keys.CONSUMER_SECRET = None
        connector = TwitterAPIConnector()
        with self.assertRaises(ImproperlyConfigured):
            connector._check_api_keys()

    def test_oauth_token_missing_return_improperly_configured(self):
        api_keys.OAUTH_TOKEN = None
        connector = TwitterAPIConnector()
        with self.assertRaises(ImproperlyConfigured):
            connector._check_api_keys()

    def test_oauth_token_secret_missing_return_improperly_configured(self):
        api_keys.OAUTH_TOKEN_SECRET = None
        connector = TwitterAPIConnector()
        with self.assertRaises(ImproperlyConfigured):
            connector._check_api_keys()

    def test_api_keys_existing(self):
        api_keys.CONSUMER_KEY = "CONSUMER_KEY"
        api_keys.CONSUMER_SECRET = "CONSUMER_SECRET"
        api_keys.OAUTH_TOKEN = "OAUTH_TOKEN"
        api_keys.OAUTH_TOKEN_SECRET = "OAUTH_TOKEN_SECRET"
        connector = TwitterAPIConnector()
        self.assertTrue(connector._check_api_keys())
