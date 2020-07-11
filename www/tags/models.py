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

class Tag(models.Model):
    """
    A tag can be set to other models. Tags are useful for filtering
    """
    name = models.CharField(max_length=100) # The tag's name
    display = models.CharField(max_length=100, blank=True, null=True) # The tag's display name
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, blank=True, null=True) # A tag can be child to another Tag

    def __str__(self):
        if self.display:
            return self.display
        else:
            return self.name

    def get_by_name(name):
        """
        Returns the Tag object from a name input.
        Returns False if no match is found
        """
        tag_filter = Tag.objects.filter(
            name = name
        )
        if tag_filter.exists():
            return tag_filter.get()
        else:
            return False

    def get_book(self):
        """
        Returns all related Book
        """
        return self.book_set.all().order_by('name')
