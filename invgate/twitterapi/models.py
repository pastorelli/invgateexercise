# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class TwitterProfile(models.Model):
    """
        Defines the twitter profile information used in the crawler
    """
    def __str__(self):
        return self.name

    name = models.CharField(max_length=100)
    short_description = models.CharField(max_length=200, blank=True, null=True)
    profile_pic_uri = models.CharField(max_length=200, blank=True, null=True)
    popularity_index = models.IntegerField(default=0)
