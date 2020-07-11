from django.contrib import admin

from .models import Book, Chapter, Page

class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'url_key', 'dir_name', 'update_date')
    search_fields = ('name', 'author', 'illustrator')
    filter_horizontal = ('tags',)

class ChapterAdmin(admin.ModelAdmin):
    list_display = ('book', 'chapter', 'name', 'dir_name', 'read_left')
    list_editable = ('read_left',)
    search_fields = ('book', 'name')

class PageAdmin(admin.ModelAdmin):
    list_display = ('chapter', 'page', 'file_abs_path')

admin.site.register(Book, BookAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Page, PageAdmin)