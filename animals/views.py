from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Animal, Person


class AnimalIndexView(generic.ListView):
    template_name = 'animals/index.html'
    context_object_name = 'all_animals'
    def get_queryset(self):
        """Return the latest additions to the Animals table"""
        return Animal.objects.order_by('-entry_date')[:100]
