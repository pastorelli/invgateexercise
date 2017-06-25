# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase
from mock import patch
from requests_oauthlib import OAuth1Session

from ..twitter_connector import TwitterAPIConnector


class TwitterAPIConnectorTest(TestCase):

    @patch("twitterapi.twitter_connector.CONSUMER_KEY", None)
    def test_consumer_key_missing_return_improperly_configured(self):
        connector = TwitterAPIConnector()
        with self.assertRaises(ImproperlyConfigured):
            connector._check_api_keys()

    @patch("twitterapi.twitter_connector.CONSUMER_SECRET", None)
    def test_consumer_secret_missing_return_improperly_configured(self):
        connector = TwitterAPIConnector()
        with self.assertRaises(ImproperlyConfigured):
            connector._check_api_keys()

    @patch("twitterapi.twitter_connector.OAUTH_TOKEN", None)
    def test_oauth_token_missing_return_improperly_configured(self):
        connector = TwitterAPIConnector()
        with self.assertRaises(ImproperlyConfigured):
            connector._check_api_keys()

    @patch("twitterapi.twitter_connector.OAUTH_TOKEN_SECRET", None)
    def test_oauth_token_secret_missing_return_improperly_configured(self):
        connector = TwitterAPIConnector()
        with self.assertRaises(ImproperlyConfigured):
            connector._check_api_keys()

    @patch("twitterapi.twitter_connector.CONSUMER_KEY", "valid")
    @patch("twitterapi.twitter_connector.CONSUMER_SECRET", "valid")
    @patch("twitterapi.twitter_connector.OAUTH_TOKEN", "valid")
    @patch("twitterapi.twitter_connector.OAUTH_TOKEN_SECRET", "valid")
    def test_api_keys_existing(self):
        connector = TwitterAPIConnector()
        self.assertTrue(connector._check_api_keys())

    @patch("twitterapi.twitter_connector.CONSUMER_KEY", "valid")
    @patch("twitterapi.twitter_connector.CONSUMER_SECRET", "valid")
    @patch("twitterapi.twitter_connector.OAUTH_TOKEN", "valid")
    @patch("twitterapi.twitter_connector.OAUTH_TOKEN_SECRET", "valid")
    def test_get_oauth(self):
        connector = TwitterAPIConnector()
        self.assertIsInstance(connector._get_oaut(), OAuth1Session)
