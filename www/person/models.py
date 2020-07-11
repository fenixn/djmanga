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

class Person(models.Model):
    """
    A person model. Used for authors and illustrators.
    """
    name = models.CharField(max_length=100) # The person's name
    slug = models.CharField(max_length=100) # The slug used to access a person's page

    def __str__(self):
            return self.name

    def get_by_slug(slug):
        """
        Returns the Person object from a slug input.
        Returns False if no match is found
        """
        person_filter = Person.objects.filter(
            slug = slug
        )
        if person_filter.exists():
            return person_filter.get()
        else:
            return False

    def get_authored_book(self):
        """
        Returns all  Book authored by this person
        """
        return self.author.all().order_by('name')

    def get_illustrated_book(self):
        """
        Returns all  Book illustrated by this person
        """
        return self.illustrator.all().order_by('name')
