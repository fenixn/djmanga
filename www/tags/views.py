from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import TemplateView

from .models import Tag

class IndexView(ListView):
    template_name = 'tags/index.html'
    context_object_name = 'tags_list'
    def get_queryset(self):
        """
        Return tags list
        """
        return Tag.objects.order_by('name')

def tag_view(request, tag):
    template_name = 'tags/tag-view.html'
    find_tag = Tag.get_by_name(tag)
    if find_tag == False:
        return render(request, template_name, {
            'error_message': 'The tag cannot be found.'
        })
    else:
        return render(request, template_name, {
            'tag': find_tag
        })