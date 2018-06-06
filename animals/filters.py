"""
Filters: using django-filters to filter querysets
"""
import django_filters
from django_filters import FilterSet
from .models import Animal

class AnimalFilter(FilterSet):
    mutations = django_filters.CharFilter(lookup_expr='icontains')
    line = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Animal
        fields = ['animal_type', 'sex', 'day_of_birth', 'line', 'mutations', 'location',
                  'responsible_person', 'added_by' ]
