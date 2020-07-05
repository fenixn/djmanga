from django.contrib import admin

from .models import Manga, Chapter, Page

class MangaAdmin(admin.ModelAdmin):
    list_display = ('name', 'url_key', 'author', 'dir_name')
    search_fields = ('name', 'author')

class ChapterAdmin(admin.ModelAdmin):
    list_display = ('manga', 'chapter', 'name', 'dir_name', 'read_left')
    list_editable = ('read_left',)
    search_fields = ('manga', 'name')

class PageAdmin(admin.ModelAdmin):
    list_display = ('chapter', 'page', 'file_abs_path')

admin.site.register(Manga, MangaAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Page, PageAdmin)