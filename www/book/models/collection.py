import datetime
import os
import logging
import pickle

from django.db import models
from django.apps import apps

from django.utils import timezone
from django.utils.timezone import now

class Collection(models.Model):
    """
    A collection is designed to hold a collection of books for better organization. 
    For example: manga, comics, books and magazines are all very different from 
    each other. There are advantages to separating these into their own collections.
    """
    name = models.CharField(max_length=1000)
    url_key = models.CharField(max_length=1000)
    skip_scan = models.BooleanField(default=False)

    def __str__(self):
        return self.name
