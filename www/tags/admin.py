from django.contrib import admin

from .models import Tag
from book.models import Book

class MembershipInline(admin.TabularInline):
    model = Book.tags.through

class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'display', 'parent')
    search_fields = ('name', 'display', 'parent')
    inlines = [
        MembershipInline,
    ]

admin.site.register(Tag, TagAdmin)