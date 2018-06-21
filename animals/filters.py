"""
Filters: using django-filters to filter querysets
"""
import django_filters
from django_filters import FilterSet
from .models import Animal, Organ
import django.forms

class AnimalFilter(FilterSet):
    mutations = django_filters.CharFilter(lookup_expr='icontains')
    line = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Animal
        fields = ['animal_type', 'sex', 'line', 'location','licence_number',
                  'responsible_person']

class OrganFilter(FilterSet):
    mutations = django_filters.CharFilter(lookup_expr='icontains')
    line = django_filters.CharFilter(lookup_expr='icontains')
    killing_person = django_filters.CharFilter(lookup_expr='icontains')
    method_of_killing = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Organ
        fields = ['animal_type', 'organ_type', 'sex', 'day_of_death', 'killing_person',
                  'method_of_killing', 'line', 'mutations','responsible_person',
                  'location', 'licence_number' ]

