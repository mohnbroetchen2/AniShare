"""
Filters: using django-filters to filter querysets
"""
import django_filters
from django_filters import FilterSet
from .models import Animal, Organ, Change
from django.db.models import F
import django.forms
from datetime import timedelta, tzinfo
import time
from django.db.models.functions import ExtractDay, ExtractMonth, ExtractYear
from django.utils import timezone


class AnimalFilter(FilterSet):
    mutations = django_filters.CharFilter(lookup_expr='icontains')
    line = django_filters.CharFilter(lookup_expr='icontains')
    age = django_filters.NumberFilter(method='filter_age')
    class Meta:
        model = Animal
        fields = ['animal_type', 'age', 'sex', 'line', 'location','licence_number',
                  'responsible_person']
    def filter_age(self, queryset, name, value):
        if value:
            day1 = timezone.now().day
            month1 = timezone.now().month
            year1 = timezone.now().year
            secs1 = time.mktime((year1, month1, day1, 0, 0, 0, 0, 0, 0))
            """
            day2 = int(ExtractDay(F('day_of_birth')))
            month2 = int(ExtractMonth(F('day_of_birth')))
            year2 = int(ExtractYear(F('day_of_birth')))
            
            secs2 = time.mktime((year2, month2, day2, 0, 0, 0, 0, 0, 0))
            diff = secs2 - secs1
            weeks = diff / 604800
            """
            queryset = queryset.annotate(thisage=( F('amount')+ time.mktime((2018, 8, 12, 0, 0, 0, 0, 0, 0)) - time.mktime((year1, month1, day1, 0, 0, 0, 0, 0, 0)) )/604800).filter(thisage=value)   
            """
            queryset = queryset.annotate(thisage=( time.mktime((2018, 8, 12, 0, 0, 0, 0, 0, 0)) - time.mktime((year1, month1, day1, 0, 0, 0, 0, 0, 0)) )/604800).filter(thisage=timedelta(seconds=value))
            queryset = queryset.annotate(thisage=(F('available_to') - F('day_of_birth'))/7).filter(thisage=timedelta(seconds=value))
            queryset = queryset.annotate(thisage= diff / 604800).filter(thisage=value)
            queryset = queryset.annotate(thisage=(ExtractDay(F('available_to')) - ExtractDay(F('day_of_birth'))  )).filter(thisage=value)   
            """
        return queryset

class OrganFilter(FilterSet):
    mutations = django_filters.CharFilter(lookup_expr='icontains')
    line = django_filters.CharFilter(lookup_expr='icontains')
    killing_person = django_filters.CharFilter(lookup_expr='icontains')
    method_of_killing = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Organ
        fields = ['animal_type', 'sex', 'day_of_death', 'killing_person',
                  'method_of_killing', 'line', 'mutations','responsible_person',
                  'location', 'licence_number',]

class ChangeFilter(FilterSet):
    class Meta:
        model = Change
        fields = ['change_type','version',]
