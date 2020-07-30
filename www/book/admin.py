from django.contrib import admin

from .models import Collection, Book, Chapter, Page

class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'url_key', 'skip_scan')
    list_editable = ('skip_scan',)
    search_fields = ('name',)

class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'url_key', 'dir_name', 'update_date', 'force_scan')
    list_editable = ('force_scan',)
    search_fields = ('name', 'author__name', 'illustrator__name')
    filter_horizontal = ('tags',)

class ChapterAdmin(admin.ModelAdmin):
    list_display = ('book', 'chapter', 'name', 'dir_name', 'read_left')
    list_editable = ('read_left',)
    search_fields = ('name',)

class PageAdmin(admin.ModelAdmin):
    list_display = ('page', 'file_abs_path')

admin.site.register(Collection, CollectionAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Page, PageAdmin)