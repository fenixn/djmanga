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

from tags.models import Tag
from person.models import Person

class Book(models.Model): # A book series
    name = models.CharField(max_length=1000)
    url_key = models.CharField(max_length=1000)
    book_type = models.CharField(max_length=50, default='manga')
    author = models.ManyToManyField(Person, related_name = 'author') # A Book can have many authors
    illustrator = models.ManyToManyField(Person, related_name= 'illustrator') # Book can have many illustrators
    tags = models.ManyToManyField(Tag) # Book can have many tags for filtering
    chapters = models.IntegerField(default=1)
    dir_name = models.CharField(max_length=1000)
    dir_update_timestamp = models.IntegerField(verbose_name='directory update date', blank=True, null=True)
    dir_abs_path = models.CharField(max_length=1200)
    dir_media_path = models.CharField(max_length=1000)
    cover_chapter = models.IntegerField(default=1)
    cover_page = models.IntegerField(default=1)
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
        return self.chapter_set.all().order_by('-chapter')

    def get_by_slug(slug):
        """
        Returns the Book object from a slug input.
        Returns False if no match is found
        """
        book_filter = Book.objects.filter(
            url_key = slug
        )
        if book_filter.exists():
            return book_filter.get()
        else:
            return False

    def is_single_chapter(self):
        """
        Returns True if this Book only has one chapter, and False otherwise.
        """
        if self.get_chapters().count() == 1:
            return True
        else:
            return False

    def get_tag_tree(self):
        tag_tree = {}
        tag_branches = {}
        tags = self.tags.all()
        logger = logging.getLogger('djmanga')
        # build branches
        for tag in tags:
            if tag.parent is None:
                tag_tree.update({tag: {}})
            else:
                tag_branches.update({tag: {}})
        # connect branches
        unconnected_branches = tag_branches.copy()
        for tag in unconnected_branches:
            if tag.parent and tag.parent in tag_branches:
                branch_tag = tag_branches[tag]
                tag_branches[tag.parent].update({tag:branch_tag})
                tag_branches.pop(tag)
        unconnected_branches = tag_branches.copy()
        for tag in unconnected_branches:
            branch_tag = tag_branches[tag]
            tag_tree[tag.parent].update({tag:branch_tag})
            tag_branches.pop(tag)

        logger.info('tag_tree')
        logger.info(tag_tree)
        logger.info('tag_branches')
        logger.info(tag_branches)
        return tag_tree