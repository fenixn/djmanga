import datetime
import os
import logging
import pickle

from django.core import serializers
from django.db import models

from django.utils import timezone
from django.utils.timezone import now
from django.urls import resolve

from .book import Book
from tags.models import Tag
from person.models import Person

class Chapter(models.Model): # A single chapter of a book
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    chapter = models.IntegerField(default=1)
    author = models.ManyToManyField(Person, related_name = 'chapterauthor')
    illustrator = models.ManyToManyField(Person, related_name= 'chapterillustrator')
    tags = models.ManyToManyField(Tag)
    tag_tree = models.BinaryField(blank=True)
    read_left = models.BooleanField(verbose_name='read right to left?', default=True)
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

    def get_book_by_slug(slug):
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

    def get_pages(self):
        """
        Return all Page entries related to the chapter.
        """
        return self.page_set.all().order_by('page')

    def get_next(self):
        """
        Returns the path for the next chapter.
        Returns False if there is no next chapter.
        """
        next_chapter = Chapter.objects.filter(
            book = self.book,
            chapter = self.chapter + 1
        )
        if next_chapter.exists():
            return '/book/' + self.book.url_key + '/' + str(self.chapter + 1)
        else:
            return False

    def get_prev(self):
        """
        Returns the path for the previous chapter.
        Returns False if there is no previous chapter.
        """
        prev_chapter = Chapter.objects.filter(
            book = self.book,
            chapter = self.chapter - 1
        )
        if prev_chapter.exists():
            return '/book/' + self.book.url_key + '/' + str(self.chapter - 1)
        else:
            return False

    def create_tag_tree(self):
        """
        Return the model's tags in a tree structure
        """
        tags = self.tags.all()
        tag_tree = Tag.create_tag_tree(Tag,tags)
        tag_tree = pickle.dumps(tag_tree)
        self.tag_tree = tag_tree
        self.save()
        return

    def get_tag_tree(self):
        tag_tree = ''
        try:
            tag_tree = pickle.loads(self.tag_tree)
        except EOFError:
            # This means the tag tree is not created yet.
            # Do nothing so we can prevent an unnecessary error message.
            pass
        finally: 
            return tag_tree
