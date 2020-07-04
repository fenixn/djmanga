import datetime
import os
import logging

from django.contrib.staticfiles.templatetags.staticfiles import static
from django.contrib.staticfiles.utils import get_files
from django.contrib.staticfiles.storage import StaticFilesStorage

from django.db import models

from django.utils import timezone
from django.utils.timezone import now

from .chapter import Chapter

class Page(models.Model): # A single page of a chapter
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    page = models.IntegerField(default=1)
    file_name = models.CharField(max_length=200)
    file_abs_path = models.CharField(max_length=2400)
    file_media_path = models.CharField(max_length=2000)

    def __str__(self):
        return self.file_media_path