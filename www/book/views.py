from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import TemplateView

from .models import Book
from .models import Chapter
from .models import Scan

class IndexView(ListView):
    template_name = 'book/index.html'
    context_object_name = 'book_list'
    def get_queryset(self):
        """
        Return book list
        """
        return Book.objects.order_by('-update_date')

def book_view(request, url_key):
    template_name = 'book/book-view.html'
    book = Book.get_by_slug(url_key)
    if book == False:
        return render(request, template_name, {
            'error_message': 'The Book cannot be found.'
        })
    else:
        return render(request, template_name, {
            'book': book
        })
    
def chapter_view(request, url_key, chapter):
    template_name = 'book/chapter-view.html'
    book = Chapter.get_book_by_slug(url_key)
    if book == False:
        return render(request, template_name, {
            'error_message': 'The Book cannot be found.'
        })
    else:
        current_chapter = Chapter.objects.filter(
            book = book,
            chapter = chapter
        ).get()
        return render(request, template_name, {
            'book': book,
            'chapter': current_chapter
        })

class ScanView(TemplateView):
    template_name = "book/scan.html"
    model = Scan()

    def get_context_data(self, **kwargs):
        context = super(ScanView, self).get_context_data(**kwargs)
        context.update({'book_list': self.model.scan_book()})
        return context
