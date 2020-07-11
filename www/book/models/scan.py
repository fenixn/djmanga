import datetime
import os
import logging
import re
import json

from natsort import natsorted

from django.contrib.staticfiles.templatetags.staticfiles import static
from django.contrib.staticfiles.utils import get_files
from django.contrib.staticfiles.storage import StaticFilesStorage

from django.db import models

from django.utils import timezone
from django.utils.timezone import now

from .book import Book
from .chapter import Chapter
from .page import Page
from tags.models import Tag
from person.models import Person

class Scan(models.Model):
    def __init__(self):
        self.book_dir_url = os.path.abspath(__file__ + "/../../../media/manga")
        self.book_media_url = 'media/manga'

    def get_scan_book_list(self):
        """
        Returns a list of directories in the media/book folder.
        It is assumed that each directory contains a unique book.
        """
        scan_book_list = []
        book_dirs = os.scandir(self.book_dir_url)
        for book_dir in book_dirs:
            scan_book_list.append(book_dir.name)
        return scan_book_list

    def get_scan_chapter_list(self, Book):
        """
        Returns a list of subdirectories in the book's base folder.
        It is assumed that each subdirectory is a chapter.
        If there are no subdirectory, return False
        """
        scan_chapter_list = []
        book_dir_files = os.scandir(Book.dir_abs_path)
        for entry in book_dir_files:
            if entry.is_dir():
                scan_chapter_list.append(entry.name)
        if len(scan_chapter_list) > 0:
            scan_chapter_list = natsorted(scan_chapter_list)
            return scan_chapter_list
        else:
            return False

    def update_chapter_pages(self, Chapter):
        """
        Compile a list of page files in the chapter's folder and update the
        database.
        """
        scan_page_list = []
        chapter_dir_files = os.scandir(Chapter.dir_abs_path)
        for entry in chapter_dir_files:
            if entry.is_file() and entry.name != 'info.json':
                scan_page_list.append(entry.name)
        if len(scan_page_list) > 0:
            scan_page_list = natsorted(scan_page_list)
            page_count = 1
            for page in scan_page_list:
                page_filter = Page.objects.filter(
                    chapter = Chapter,
                    page = page_count
                )
                find_page = page_filter.exists()
                if find_page:
                    # Matching page found, update page file
                    page_to_update = page_filter.get()
                    page_to_update.file_name = page
                    page_to_update.file_abs_path = Chapter.dir_abs_path + '/' + page
                    page_to_update.file_media_path = Chapter.dir_media_path + '/' + page
                    page_to_update.save()
                else:
                    # No matching page, create it
                    new_page = Page.objects.create(
                        chapter = Chapter,
                        page = page_count,
                        file_name = page,
                        file_abs_path = Chapter.dir_abs_path + '/' + page,
                        file_media_path = Chapter.dir_media_path + '/' + page
                    )
                page_count += 1

    def scan_book(self):
        """
        Scan book directory and modify database accordingly.
        """
        scan_book_list = self.get_scan_book_list()

        # Create new Book entry for each directory that does not have an entry.
        for book in scan_book_list:
            book_filter = Book.objects.filter(dir_name = book)
            find_book = book_filter.exists()
            if find_book:
                # An existing entry is found, scan for new chapters
                existing_book = book_filter.get()
                scan_chapter_list = self.get_scan_chapter_list(existing_book)
                if scan_chapter_list == False:
                    # No chapter subdir, update pages
                    chapter = Chapter.objects.filter(
                        book = existing_book
                    ).get()
                    self.update_chapter_pages(chapter)
                else:
                    # Go each chapter and find match, create new entry if no
                    # match is found
                    chapter_count = 1
                    for chapter in scan_chapter_list:
                        chapter_filter = Chapter.objects.filter(
                            book = existing_book,
                            dir_name = chapter
                        )
                        find_chapter = chapter_filter.exists()
                        if find_chapter:
                            # Existing chapter, update pages
                            self.update_chapter_pages(chapter_filter.get())
                        else:
                            # No entry is found, create one
                            new_chapter = Chapter.objects.create(
                                book = existing_book,
                                chapter = chapter_count,
                                dir_name = chapter,
                                dir_abs_path = existing_book.dir_abs_path + '/' + chapter,
                                dir_media_path = existing_book.dir_media_path + '/' + chapter
                            )
                            # Check folder for info.json to update values for chapter
                            info_abs_path = new_chapter.dir_media_path + '/info.json'
                            self.update_model_from_info(new_chapter, info_abs_path)
                            self.update_chapter_pages(new_chapter)                     
                        chapter_count += 1
                    existing_book.chapters = chapter_count - 1
                    existing_book.save()
                info_abs_path = self.book_dir_url + '/' + book + '/info.json'
                self.update_model_from_info(existing_book, info_abs_path)
                self.update_book_cover_path(existing_book)
            else:
                # No entry is found, create one.
                # url_key regex replaces all but alphanumeric with a space
                new_book = Book.objects.create(
                    name = book,
                    url_key = re.sub(r'\W+', ' ', book).strip().replace(' ', '-').lower(),
                    dir_name = book,
                    dir_abs_path = self.book_dir_url + '/' + book,
                    dir_media_path = self.book_media_url + '/' + book
                )
                # Check folder for info.json to update values for book
                info_abs_path = self.book_dir_url + '/' + book + '/info.json'
                self.update_model_from_info(new_book, info_abs_path)
                scan_chapter_list = self.get_scan_chapter_list(new_book)
                if scan_chapter_list == False:
                    # No Chapter subdir found, create one chapter and set
                    # directory location to match book
                    new_chapter = Chapter.objects.create(
                        book = new_book,
                        chapter = 1,
                        dir_name = new_book.dir_name,
                        dir_abs_path = new_book.dir_abs_path,
                        dir_media_path = new_book.dir_media_path
                    )
                    # Check folder for info.json to update values for chapter
                    info_abs_path = new_chapter.dir_media_path + '/info.json'
                    self.update_model_from_info(new_chapter, info_abs_path)
                    self.update_chapter_pages(new_chapter)
                else:
                    # Chapter subdirs found, create a chapter for each
                    chapter_count = 1
                    for chapter in scan_chapter_list:
                        new_chapter = Chapter.objects.create(
                            book = new_book,
                            chapter = chapter_count,
                            dir_name = chapter,
                            dir_abs_path = new_book.dir_abs_path + '/' + chapter,
                            dir_media_path = new_book.dir_media_path + '/' + chapter
                        )
                        # Check folder for info.json to update values for chapter
                        info_abs_path = new_chapter.dir_media_path + '/info.json'
                        self.update_model_from_info(new_chapter, info_abs_path)
                        self.update_chapter_pages(new_chapter)
                        chapter_count += 1
                # Update Cover For New Book
                self.update_book_cover_path(new_book)
        return scan_book_list

    def update_model_from_info(self, model, info_abs_path):
        """
        Update a model from the info.json file inside it's directory.
        """
        if os.path.isfile(info_abs_path):
            info_file = open(info_abs_path, 'r')
            info_json = json.load(info_file)
            for attribute in info_json:
                if attribute == "tags":
                    self.update_book_tags(model, info_json[attribute])
                elif (attribute == "author" or attribute == "illustrator"):
                    self.update_book_person(model, info_json[attribute], attribute)
                else:
                    setattr(model, attribute, info_json[attribute])
            model.save()
        return

    def update_book_cover_path(self, book):
        """
        Update the cover path for the input book.
        """
        cover_chapter = Chapter.objects.filter(
            book = book,
            chapter = book.cover_chapter
        )
        if cover_chapter.exists():
            cover_page = Page.objects.filter(
                chapter = cover_chapter.get(),
                page = book.cover_page
            )
            if cover_page.exists():
                book.cover_path = cover_page.get().file_media_path
                book.save()
        return

    def update_book_tags(self, book, tags):
        """
        Update the tags for the book
        """
        tags = tags.split(',')
        for tag in tags:
            tag = re.sub(r'\W+', ' ', tag).strip().replace(' ', '-').lower()
            find_tag = Tag.objects.filter(name=tag)
            if find_tag.exists():
                book.tags.add(find_tag.get())
            else:
                new_tag = Tag.objects.create(
                    name = tag
                )
                book.tags.add(new_tag)
        book.save()
        return

    def update_book_person(self, book, people, role):
        """
        Update a person's role with a book
        """
        people = people.split(',')
        for person in people:
            person = person.strip()
            find_person = Person.objects.filter(name=person)
            if find_person.exists():
                if role == "author":
                    book.author.add(find_person.get())
                elif role == "illustrator":
                    book.illustrator.add(find_person.get())
            else:
                new_person = Person.objects.create(
                    name = person,
                    slug = re.sub(r'\W+', ' ', person).strip().replace(' ', '-').lower()
                )
                if role == "author":
                    book.author.add(new_person)
                elif role == "illustrator":
                    book.illustrator.add(new_person)
        book.save()

