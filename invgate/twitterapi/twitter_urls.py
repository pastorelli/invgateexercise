"""
    Here goes the twitter url used to retrieve the profile

    INFO:
    If the urls doesn't exist the application will throw an
    ImproperlyConfigured error.
"""
TWITTER_BASE_URL = "https://api.twitter.com/1.1"
TWITTER_PROFILE_URL = TWITTER_BASE_URL + "/users/show.json?"
