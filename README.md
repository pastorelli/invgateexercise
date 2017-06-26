
Twitter web crawler using a message broker
=====

Twitter API exercise
=====

This app is used to retrieve the twitter profile information using
celery and rabbitMQ as a message broker

Requirements
-----------

This app needs celery and rabbitMQ in order to process the twitter profile requests.

To install rabbitMQ on ubuntu/debian
```
$ sudo apt-get install rabbitmq-server
```
For other enviroments check the installation page on the rabbitmq website:
`https://www.rabbitmq.com/download.html`


Quick start
-----------

1. Add "twitterapi" to your INSTALLED_APPS setting like this::
```python
    INSTALLED_APPS = [
        ...
        'twitterapi',
    ]
```
2. Include the twitterapi URLconf in your project urls.py like this::

```python
    url(r'^twitterapi/', include('twitterapi.urls')),
```
3. Run `python manage.py migrate` to create the twitterapi models.

4. Configure Celery.
    In the directory where your `settings.py` is located creates a `celery.py` file.
    Changing 'projectname' with your project name
```python
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectname.settings')

app = Celery('projectname')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
```
5. In the same directory inside your `__init__.py` file add

```python
from __future__ import absolute_import, unicode_literals

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app

__all__ = ['celery_app']
```

6. You can now run celery on your console

	`$ celery -A projectname worker -l info`
	where projectname is the project name

7. In your `settings.py` add the information about your twitter api keys:
    > The keys can be obtained using the twiiter dev page:
    > First create an app and then create the keys for that app
         `https://apps.twitter.com/`
```python
CONSUMER_KEY = "KEY"
CONSUMER_SECRET = "KEY"

OAUTH_TOKEN = "KEY"
OAUTH_TOKEN_SECRET = "KEY"
```
8. Visit `http://127.0.0.1:8000/twitterapi/?username=twitterusername` to get the twitter profile
