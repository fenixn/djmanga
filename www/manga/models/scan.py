import datetime
import os
import logging
import re
import json

from django.contrib.staticfiles.templatetags.staticfiles import static
from django.contrib.staticfiles.utils import get_files
from django.contrib.staticfiles.storage import StaticFilesStorage

from django.db import models

from django.utils import timezone
from django.utils.timezone import now

from .manga import Manga
from .chapter import Chapter
from .page import Page

class Scan(models.Model):
    def __init__(self):
        self.manga_dir_url = os.path.abspath(__file__ + "/../../../media/manga")
        self.manga_media_url = 'media/manga'

    def get_scan_manga_list(self):
        """
        Returns a list of directories in the media/manga folder.
        It is assumed that each directory contains a unique manga.
        """
        scan_manga_list = []
        manga_dirs = os.scandir(self.manga_dir_url)
        for manga_dir in manga_dirs:
            scan_manga_list.append(manga_dir.name)
        return scan_manga_list

    def get_scan_chapter_list(self, Manga):
        """
        Returns a list of subdirectories in the manga's base folder.
        It is assumed that each subdirectory is a chapter.
        If there are no subdirectory, return False
        """
        scan_chapter_list = []
        manga_dir_files = os.scandir(Manga.dir_abs_path)
        for entry in manga_dir_files:
            if entry.is_dir():
                scan_chapter_list.append(entry.name)
        if len(scan_chapter_list) > 0:
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
            if entry.is_file():
                scan_page_list.append(entry.name)
        if len(scan_page_list) > 0:
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
        # Update Cover
        manga = Chapter.manga
        first_page_filter = Page.objects.filter(
            chapter = Chapter,
            page = 1
        )
        manga.cover_path = first_page_filter.get().file_media_path
        manga.save()

    def scan_manga(self):
        """
        Scan manga directory and modify database accordingly.
        """
        scan_manga_list = self.get_scan_manga_list()

        # Create new Manga entry for each directory that does not have an entry.
        for manga in scan_manga_list:
            manga_filter = Manga.objects.filter(dir_name = manga)
            find_manga = manga_filter.exists()
            if find_manga:
                # An existing entry is found, scan for new chapters
                existing_manga = manga_filter.get()
                scan_chapter_list = self.get_scan_chapter_list(existing_manga)
                if scan_chapter_list == False:
                    # No chapter subdir, update pages
                    chapter = Chapter.objects.filter(
                        manga = existing_manga
                    ).get()
                    self.update_chapter_pages(chapter)
                else:
                    # Go each chapter and find match, create new entry if no
                    # match is found
                    chapter_count = 1
                    for chapter in scan_chapter_list:
                        chapter_filter = Chapter.objects.filter(
                            manga = existing_manga,
                            dir_name = chapter
                        )
                        find_chapter = chapter_filter.exists()
                        if find_chapter:
                            # Existing chapter, update pages
                            self.update_chapter_pages(chapter_filter.get())
                        else:
                            # No entry is found, create one
                            new_chapter = Chapter.objects.create(
                                manga = existing_manga,
                                chapter = chapter_count,
                                dir_name = chapter,
                                dir_abs_path = existing_manga.dir_abs_path + '/' + chapter,
                                dir_media_path = existing_manga.dir_media_path + '/' + chapter
                            )
                            self.update_chapter_pages(new_chapter)                     
                        chapter_count += 1
                    existing_manga.chapters = chapter_count - 1
                    existing_manga.save()
            else:
                # No entry is found, create one.
                # url_key regex replaces all but alphanumeric with a space
                new_manga = Manga.objects.create(
                    name = manga,
                    url_key = re.sub(r'\W+', ' ', manga).strip().replace(' ', '-').lower(),
                    dir_name = manga,
                    dir_abs_path = self.manga_dir_url + '/' + manga,
                    dir_media_path = self.manga_media_url + '/' + manga
                )
                # Check folder for info.json to update values for entry
                info_abs_path = self.manga_dir_url + '/' + manga + '/info.json'
                if os.path.isfile(info_abs_path):
                    info_file = open(info_abs_path, 'r')
                    info_json = json.load(info_file)
                    for attribute in info_json:
                        setattr(new_manga, attribute, info_json[attribute])
                    new_manga.save()
                
                scan_chapter_list = self.get_scan_chapter_list(new_manga)
                if scan_chapter_list == False:
                    # No Chapter subdir found, create one chapter and set
                    # directory location to match manga
                    new_chapter = Chapter.objects.create(
                        manga = new_manga,
                        chapter = 1,
                        dir_name = new_manga.dir_name,
                        dir_abs_path = new_manga.dir_abs_path,
                        dir_media_path = new_manga.dir_media_path
                    )
                    self.update_chapter_pages(new_chapter)
                else:
                    # Chapter subdirs found, create a chapter for each
                    chapter_count = 1
                    for chapter in scan_chapter_list:
                        new_chapter = Chapter.objects.create(
                            manga = new_manga,
                            chapter = chapter_count,
                            dir_name = chapter,
                            dir_abs_path = new_manga.dir_abs_path + '/' + chapter,
                            dir_media_path = new_manga.dir_media_path + '/' + chapter
                        )
                        self.update_chapter_pages(new_chapter)
                        chapter_count += 1
        return scan_manga_list