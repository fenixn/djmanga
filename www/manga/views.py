from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import TemplateView

from .models import Manga
from .models import Chapter
from .models import Scan

class IndexView(ListView):
    template_name = 'manga/index.html'
    context_object_name = 'manga_list'
    def get_queryset(self):
        """
        Return manga list
        """
        return Manga.objects.order_by('-update_date')

def manga_view(request, url_key):
    template_name = 'manga/manga-view.html'
    manga = Manga.get_by_slug(url_key)
    if manga == False:
        return render(request, template_name, {
            'error_message': 'The Manga cannot be found.'
        })
    else:
        return render(request, template_name, {
            'manga': manga
        })
    
def chapter_view(request, url_key, chapter):
    template_name = 'manga/chapter-view.html'
    manga = Chapter.get_manga_by_slug(url_key)
    if manga == False:
        return render(request, template_name, {
            'error_message': 'The Manga cannot be found.'
        })
    else:
        current_chapter = Chapter.objects.filter(
            manga = manga,
            chapter = chapter
        ).get()
        return render(request, template_name, {
            'manga': manga,
            'chapter': current_chapter
        })

class ScanView(TemplateView):
    template_name = "manga/scan.html"
    model = Scan()

    def get_context_data(self, **kwargs):
        context = super(ScanView, self).get_context_data(**kwargs)
        context.update({'manga_list': self.model.scan_manga()})
        return context
