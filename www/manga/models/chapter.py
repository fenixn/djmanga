import datetime
import os
import logging

from django.contrib.staticfiles.templatetags.staticfiles import static
from django.contrib.staticfiles.utils import get_files
from django.contrib.staticfiles.storage import StaticFilesStorage

from django.db import models

from django.utils import timezone
from django.utils.timezone import now

from .manga import Manga

class Chapter(models.Model): # A single chapter of a manga
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    chapter = models.IntegerField(default=1)
    dir_name = models.CharField(max_length=1000)
    dir_abs_path = models.CharField(max_length=2200)
    dir_media_path = models.CharField(max_length=2000)
    pub_date = models.DateTimeField(verbose_name='date published', blank=True, null=True)
    created_date = models.DateTimeField(verbose_name='entry creation date', default=now)
    update_date = models.DateTimeField(verbose_name='date last updated', auto_now=True)

    def __str__(self):
        return self.name

    def get_chapter_cover(self):
        """
        Returns the media path of the first page of the chapter.
        """
        return self.page_set.filter(chapter=self, page=1).get().file_media_path