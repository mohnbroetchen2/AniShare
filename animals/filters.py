"""
Filters: using django-filters to filter querysets
"""
from django_filters import FilterSet
from .models import Animal

class AnimalFilter(FilterSet):
    class Meta:
        model = Animal
        fields = ['sex', 'animal_type', 'day_of_birth', 'line', 'location', 'responsible_person',
                  'added_by' ]
