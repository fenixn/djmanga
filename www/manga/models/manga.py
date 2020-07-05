import datetime
import os
import logging

from django.contrib.staticfiles.templatetags.staticfiles import static
from django.contrib.staticfiles.utils import get_files
from django.contrib.staticfiles.storage import StaticFilesStorage

from django.db import models
from django.apps import apps

from django.utils import timezone
from django.utils.timezone import now

class Manga(models.Model): # A manga series
    name = models.CharField(max_length=1000)
    url_key = models.CharField(max_length=1000)
    author = models.CharField(max_length=200, blank=True)
    illustrator = models.CharField(max_length=200, blank=True)
    chapters = models.IntegerField(default=1)
    dir_name = models.CharField(max_length=1000)
    dir_abs_path = models.CharField(max_length=1200)
    dir_media_path = models.CharField(max_length=1000)
    cover_path = models.CharField(max_length=2400)
    pub_date = models.DateTimeField(verbose_name='date published', blank=True, null=True)
    created_date = models.DateTimeField(verbose_name='entry creation date', default=now)
    update_date = models.DateTimeField(verbose_name='date last updated', auto_now=True)

    def __str__(self):
        return self.name

    def get_chapters(self):
        """
        Returns all related Chapters
        """
        return self.chapter_set.all().order_by('-update_date')