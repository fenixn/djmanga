from django.contrib import admin

from .models import Person
from book.models import Book

class AuthorInline(admin.TabularInline):
    model = Book.author.through

class IllustratorInline(admin.TabularInline):
    model = Book.illustrator.through

class PeopleAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    inlines = [
        AuthorInline, IllustratorInline
    ]

admin.site.register(Person, PeopleAdmin)