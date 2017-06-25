# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase
from mock import patch
from requests_oauthlib import OAuth1

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
        self.assertIsInstance(connector._get_oaut(), OAuth1)

    class MockedRequestResponse(object):
        def __init__(self, status_code, profile={}):
            self.status_code = status_code
            self.profile = profile

        def json(self):
            return self.profile

    @patch("twitterapi.twitter_connector.CONSUMER_KEY", "invalid")
    @patch("twitterapi.twitter_connector.CONSUMER_SECRET", "invalid")
    @patch("twitterapi.twitter_connector.OAUTH_TOKEN", "invalid")
    @patch("twitterapi.twitter_connector.OAUTH_TOKEN_SECRET", "invalid")
    @patch('requests.get')
    def test_get_twitter_profile_invalid_token(self, mock_requests_get):
        mock_requests_get.return_value = self.MockedRequestResponse(401)
        connector = TwitterAPIConnector()
        response = connector.get_twitter_profile("dummy_username")
        self.assertEqual(response['status'], 401)

    @patch("twitterapi.twitter_connector.CONSUMER_KEY", "valid")
    @patch("twitterapi.twitter_connector.CONSUMER_SECRET", "valid")
    @patch("twitterapi.twitter_connector.OAUTH_TOKEN", "valid")
    @patch("twitterapi.twitter_connector.OAUTH_TOKEN_SECRET", "valid")
    @patch('requests.get')
    def test_get_twitter_profile_username_not_found(self, mock_requests_get):
        mock_requests_get.return_value = self.MockedRequestResponse(404)
        connector = TwitterAPIConnector()
        response = connector.get_twitter_profile("dummy_username_not_exist")
        self.assertEqual(response['status'], 404)

    @patch("twitterapi.twitter_connector.CONSUMER_KEY", "valid")
    @patch("twitterapi.twitter_connector.CONSUMER_SECRET", "valid")
    @patch("twitterapi.twitter_connector.OAUTH_TOKEN", "valid")
    @patch("twitterapi.twitter_connector.OAUTH_TOKEN_SECRET", "valid")
    @patch('requests.get')
    def test_get_twitter_profile_username_found(self, mock_requests_get):
        mock_response = self.MockedRequestResponse(
            200,
            profile={'twitter_profile': {'twitter_response'}})
        mock_requests_get.return_value = mock_response
        connector = TwitterAPIConnector()
        response = connector.get_twitter_profile("dummy_username_not_exist")
        self.assertEqual(response['status'], 200)
        self.assertEqual(response['twitter_content'],
                         {'twitter_profile': {'twitter_response'}})
