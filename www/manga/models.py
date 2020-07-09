import datetime
import os
import logging

from django.contrib.staticfiles.templatetags.staticfiles import static
from django.contrib.staticfiles.utils import get_files
from django.contrib.staticfiles.storage import StaticFilesStorage

from django.db import models

from django.utils import timezone
from django.utils.timezone import now

class Manga(models.Model): # A manga series
    name = models.CharField(max_length=1000)
    author = models.CharField(max_length=200)
    chapters = models.IntegerField(default=1)
    folder_name = models.CharField(max_length=1000)
    folder_path = models.CharField(max_length=1200)
    pub_date = models.DateTimeField(verbose_name='date published', blank=True, null=True)
    created_date = models.DateTimeField(verbose_name='entry creation date', default=now)
    update_date = models.DateTimeField(verbose_name='date last updated', auto_now=True)

    def __str__(self):
        return self.name

class Chapter(models.Model): # A single chapter of a manga
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    chapter = models.IntegerField(default=1)
    folder_name = models.CharField(max_length=1000)
    pub_date = models.DateTimeField(verbose_name='date published', blank=True, null=True)
    created_date = models.DateTimeField(verbose_name='entry creation date', default=now)
    update_date = models.DateTimeField(verbose_name='date last updated', auto_now=True)

    def __str__(self):
        return self.name

    #def getpath():
        """
        Get the folder static path by adding the parent manga folder path to the
        chapter folder path
        """

class Scan(models.Model):
    def __init__(self):
        self.manga_dir_url = os.path.abspath(__file__ + "/../../media/manga/")

    def get_manga_list(self):
        """
        Returns a list of directories in the media/manga folder.
        It is assumed that each directory contains a unique manga.
        """
        manga_list = []
        manga_dirs = os.scandir(self.manga_dir_url)
        for manga_dir in manga_dirs:
            manga_list.append(manga_dir.name)
        return manga_list

    #def get_chapter_list
        """
        Returns a list of subdirectories in the manga's base folder.
        It is assumed that each subdirectory is a chapter.
        """

    def scan_manga(self):
        """
        Scan manga directory and modify database with new entries.
        """
        manga_list = self.get_manga_list()

        # Create new Manga entry for each directory that does not have an entry.
        for manga in manga_list:
            match = Manga.objects.filter(
                folder_name=manga
            )
            if len(match) == 0:
                # No entry is found, create one
                Manga.objects.create(
                    name=manga, 
                    folder_name=manga,
                    folder_path='media/manga/' + manga
                )
            # Get number of chapters by scanning manga directory.
            # If no subdirs found, assume only 1 chapter
            # and all pages stored in manga root dir.
            # For each chapter, create entry

        return manga_list