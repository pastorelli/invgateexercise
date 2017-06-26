# -*- coding: utf-8 -*-
"""
    Tests for the get twitter profile view
"""
from __future__ import unicode_literals
import json

from django.core.urlresolvers import reverse
from django.test import RequestFactory, TestCase
from mock import patch

from ..models import TwitterProfile, TwitterTaskStatus
from ..views import RetrieveTwitterProfileView


class RetrieveTwitterProfileTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def _dummy_twitter_profile(self):
        return TwitterProfile.objects.create(
            username="dummy_name",
            name="dummy_name",
            short_description="dummy_description",
            profile_pic_uri="dummy_pic_uri"
        )

    def _dummy_twitter_task_status(self, status, content=""):
        return TwitterTaskStatus.objects.create(
            username="dummy_name",
            job="job_id",
            status=status,
            twitter_response=content
        )

    def test_get_without_params(self):
        request = self.factory.get(reverse('twitterapi:retrieve'))
        response = RetrieveTwitterProfileView.as_view()(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content,
                         "Twitter username expected as a GET param")

    def test_not_existing_twitter_profile_returns_none(self):
        view = RetrieveTwitterProfileView()
        self.assertIsNone(view._get_twitter_profile("no_existing_name"))

    def test_existing_twitter_profile_returns_profile(self):
        dummy_profile = self._dummy_twitter_profile()
        view = RetrieveTwitterProfileView()
        test_profile = view._get_twitter_profile("dummy_name")
        self.assertEqual(test_profile.pk, dummy_profile.pk)

    def test_twitter_profile_to_dict(self):
        dummy_profile = self._dummy_twitter_profile()
        dummy_profile_dict = {
            'name': "dummy_name",
            'description': "dummy_description",
            'profile_pic_uri': "dummy_pic_uri",
            'popularity_index': 0,
        }
        view = RetrieveTwitterProfileView()
        self.assertEqual(view._twitter_profile_to_dict(dummy_profile),
                         dummy_profile_dict)

    @patch('twitterapi.views.check_api_keys')
    def test_get_existing_twitter_profile_as_json(self, mock_check_api_keys):
        mock_check_api_keys.return_value = True
        dummy_profile = self._dummy_twitter_profile()
        response = self.client.get(
            reverse('twitterapi:retrieve'), {'username': 'dummy_name'})
        json_dummy_profile = {
            'name': 'dummy_name',
            'description': 'dummy_description',
            'profile_pic_uri': 'dummy_pic_uri',
            'popularity_index': 0
        }
        response_dummy = json.dumps(
            {'data': json_dummy_profile}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, response_dummy)

    @patch('twitterapi.views.check_api_keys')
    def test_get_twitter_profile_exist(self, mock_check_api_keys):
        mock_check_api_keys.return_value = True
        dummy_profile = self._dummy_twitter_profile()
        response = self.client.get(
            reverse('twitterapi:retrieve'), {'username': 'dummy_name'})
        twitter_profile = json.loads(response.content)['data']
        response_dummy = {'name': 'dummy_name',
                          'description': 'dummy_description',
                          'profile_pic_uri': 'dummy_pic_uri',
                          'popularity_index': 0}
        self.assertEqual(twitter_profile['name'],
                         response_dummy['name'])
        self.assertEqual(twitter_profile['description'],
                         response_dummy['description'])
        self.assertEqual(twitter_profile['profile_pic_uri'],
                         response_dummy['profile_pic_uri'])
        self.assertEqual(twitter_profile['popularity_index'],
                         response_dummy['popularity_index'])

    @patch('twitterapi.views.check_api_keys')
    def test_get_task_status_username_not_found(self, mock_check_api_keys):
        mock_check_api_keys.return_value = True
        tts = self._dummy_twitter_task_status(404)
        response = self.client.get(
            reverse('twitterapi:retrieve'), {'username': 'dummy_name'})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, 'Twitter username doesnt exist')

    @patch('twitterapi.views.check_api_keys')
    def test_get_task_status_api_key_invalid(self, mock_check_api_keys):
        mock_check_api_keys.return_value = True
        tts = self._dummy_twitter_task_status(401)
        response = self.client.get(
            reverse('twitterapi:retrieve'), {'username': 'dummy_name'})
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, 'Twitter API token invalid')

    @patch('twitterapi.views.check_api_keys')
    def test_get_task_status_processing(self, mock_check_api_keys):
        mock_check_api_keys.return_value = True
        tts = self._dummy_twitter_task_status(202)
        response = self.client.get(
            reverse('twitterapi:retrieve'), {'username': 'dummy_name'})
        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.content, "processing request")

    @patch('twitterapi.views.check_api_keys')
    def test_get_twitter_task_profile_exist(self, mock_check_api_keys):
        mock_check_api_keys.return_value = True
        content = json.dumps({
            "name": "dummy_name",
            "description": "dummy_description",
            "profile_image_url": "dummy_pic_uri",
            "followers_count": 0,
        })
        tts = self._dummy_twitter_task_status(200, content=content)
        response = self.client.get(
            reverse('twitterapi:retrieve'), {'username': 'dummy_name'})
        twitter_profile = json.loads(response.content)['data']
        response_dummy = {'name': 'dummy_name',
                          'description': 'dummy_description',
                          'profile_pic_uri': 'dummy_pic_uri',
                          'popularity_index': 0}
        self.assertEqual(twitter_profile['name'],
                         response_dummy['name'])
        self.assertEqual(twitter_profile['description'],
                         response_dummy['description'])
        self.assertEqual(twitter_profile['profile_pic_uri'],
                         response_dummy['profile_pic_uri'])
        self.assertEqual(twitter_profile['popularity_index'],
                         response_dummy['popularity_index'])

    @patch('twitterapi.views.check_api_keys')
    def test_get_task_status_unknown_response_status(self, mock_check_api_keys):
        mock_check_api_keys.return_value = True
        tts = self._dummy_twitter_task_status(250,
                                              content="unkown message error")
        response = self.client.get(
            reverse('twitterapi:retrieve'), {'username': 'dummy_name'})
        self.assertEqual(response.status_code, 250)
        self.assertEqual(response.content, "unkown message error")
