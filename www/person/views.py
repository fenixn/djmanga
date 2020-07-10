from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import TemplateView

from .models import Person

class IndexView(ListView):
    template_name = 'person/index.html'
    context_object_name = 'tags_list'
    def get_queryset(self):
        """
        Return people list
        """
        return Person.objects.order_by('name')

def person_view(request, slug):
    template_name = 'person/person-view.html'
    find_person = Person.get_by_slug(slug)
    if find_person == False:
        return render(request, template_name, {
            'error_message': 'The person cannot be found.'
        })
    else:
        return render(request, template_name, {
            'person': find_person
        })