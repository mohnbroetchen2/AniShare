"""
Filters: using django-filters to filter querysets
"""
import django_filters
from django_filters import FilterSet
from .models import Animal, Organ, Change, FishPeople, Fish, Mouse
from django.db.models import F
import django.forms
from datetime import timedelta, tzinfo
import time
from django.db.models.functions import ExtractDay, ExtractMonth, ExtractYear
from django.utils import timezone
from datetime import datetime

def action1(query, value):
    return query.extra(where=['thisage= %s'], params=[value])

class AnimalFilter(FilterSet):
    licence_number = django_filters.CharFilter(lookup_expr='icontains')
    mutations = django_filters.CharFilter(lookup_expr='icontains')
    line = django_filters.CharFilter(lookup_expr='icontains')
    genetic_background  = django_filters.CharFilter(lookup_expr='icontains')
    age = django_filters.NumberFilter(method='filter_age', label='Age')
    class Meta:
        model = Animal
        fields = ['animal_type', 'age', 'sex', 'line', 'location','licence_number', 'genetic_background',
                  'responsible_person','day_of_birth']
    def filter_age(self, queryset, name, value):
        if value:
            maxdelta = int(value)* 7
            mindelta = (int(value) * 7) + 6
            maxdate = datetime.today().date() - timedelta(days = maxdelta)
            mindate = datetime.today().date() - timedelta(days = mindelta)
        return queryset.filter(day_of_birth__range=[mindate,maxdate])
    

class OrganFilter(FilterSet):
    mutations = django_filters.CharFilter(lookup_expr='icontains')
    line = django_filters.CharFilter(lookup_expr='icontains')
    killing_person = django_filters.CharFilter(lookup_expr='icontains')
    method_of_killing = django_filters.CharFilter(lookup_expr='icontains')
    genetic_background  = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Organ
        fields = ['animal_type', 'sex', 'day_of_death', 'killing_person',
                  'method_of_killing', 'line', 'mutations','genetic_background','responsible_person',
                  'location', 'licence_number',]

class ChangeFilter(FilterSet):
    class Meta:
        model = Change
        fields = ['id','change_type','version',]

class PersonFilter(FilterSet):
    class Meta:
        model = FishPeople
        fields = ['id','firstname','lastname','login',]

class FishFilter(FilterSet):
    location = django_filters.CharFilter(lookup_expr='icontains')
    license = django_filters.CharFilter(lookup_expr='icontains')
    responsible = django_filters.CharFilter(lookup_expr='icontains')
    strain = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Fish
        fields = ['sex','strain','responsible','license','location',]

class MouseFilter(FilterSet):
    location = django_filters.CharFilter(lookup_expr='icontains')
    licence = django_filters.CharFilter(lookup_expr='icontains')
    responsible = django_filters.CharFilter(lookup_expr='icontains')
    strain = django_filters.CharFilter(lookup_expr='icontains')
    owner = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Mouse
        fields = ['sex','strain','responsible','licence','location','owner']

class PupFilter(FilterSet):
    strain = django_filters.CharFilter(lookup_expr='icontains')
    location = django_filters.CharFilter(lookup_expr='icontains')
    licence = django_filters.CharFilter(lookup_expr='icontains')
    responsible = django_filters.CharFilter(lookup_expr='icontains')
    owner = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Mouse
        fields = ['sex','strain','responsible','licence','location','owner']
