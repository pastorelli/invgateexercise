"""
    Here goes the API keys needed to login to the twitter API.abs

    The keys can be obtained using the twiiter dev page:
        -. First create an app and then create the keys for that app
            https://apps.twitter.com/

    INFO:
    If the urls doesn't exist the application will throw an
    ImproperlyConfigured error.
"""
from django.conf import settings

CONSUMER_KEY = settings.CONSUMER_KEY
CONSUMER_SECRET =  settings.CONSUMER_SECRET

OAUTH_TOKEN = settings.OAUTH_TOKEN
OAUTH_TOKEN_SECRET = settings.OAUTH_TOKEN_SECRET

