"""
    Twitter API app urls
"""
from django.conf.urls import url

from .views import RetrieveTwitterProfileView


urlpatterns = [
    url(r'^$', RetrieveTwitterProfileView.as_view(),
        name='retrieve'),
    url(r'^(?P<username>\w+)/$', RetrieveTwitterProfileView.as_view(),
        name='retrieve')
]
