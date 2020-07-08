from django.contrib import admin

from .models import Tag
from manga.models import Manga

class MembershipInline(admin.TabularInline):
    model = Manga.tags.through

class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'display', 'parent')
    search_fields = ('name', 'display', 'parent')
    inlines = [
        MembershipInline,
    ]

admin.site.register(Tag, TagAdmin)