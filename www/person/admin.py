from django.contrib import admin

from .models import Person
from manga.models import Manga

class AuthorInline(admin.TabularInline):
    model = Manga.author.through

class IllustratorInline(admin.TabularInline):
    model = Manga.illustrator.through

class PeopleAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    inlines = [
        AuthorInline, IllustratorInline
    ]

admin.site.register(Person, PeopleAdmin)