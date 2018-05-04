from django.contrib import admin
from django import forms
from .models import Animal, Person, Lab
from datetime import datetime, timedelta

from django.conf import settings

admin.site.site_header = 'AniShare admin interface'
admin.site.site_title = 'AniShare'
admin.site.index_title = 'Welcome to AniShare'

class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = ( 'amount', 'animal_type', 'entry_date', 'day_of_birth', 'available_from', 'available_to', 'sex', 'external_id', 'external_lab_id', 'line', 'location', 'mutations', 'responsible_person','new_owner', )

    def clean(self):
        available_from = self.cleaned_data.get('available_from')
        available_to = self.cleaned_data.get('available_to')
        day_of_birth = self.cleaned_data.get('day_of_birth')
        if available_from > available_to:
            raise forms.ValidationError("Dates are incorrect")
        if day_of_birth and ((datetime.now().date() -  day_of_birth) <= timedelta(days=settings.MIN_SHARE_DURATION_PUPS)):
            if available_to - available_from <= timedelta(days=settings.MIN_SHARE_DURATION_PUPS):
                raise forms.ValidationError("Minimum share duration for pups must be {} days!".format(settings.MIN_SHARE_DURATION_PUPS ))
        elif available_to - available_from <= timedelta(days=settings.MIN_SHARE_DURATION):
            raise forms.ValidationError("Minimum share duration must be {} days!".format(settings.MIN_SHARE_DURATION ))
        return self.cleaned_data

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'email','responsible_for_lab')
    search_fields=('name','email','responsible_for_lab__name')

def clear_claim(modeladmin, request, queryset):
    queryset.update(new_owner = '')
    clear_claim.short_description = "Clear 'new_owner' from selected animals"


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ( 'amount', 'entry_date', 'day_of_birth', 'age', 'available_from', 'available_to', 'line', 'sex', 'location', 'new_owner')
    list_display_links = ( 'amount', 'entry_date', 'day_of_birth', 'age', 'available_from', 'available_to', 'line', 'sex', 'location', 'new_owner')
    search_fields = ( 'amount', 'entry_date', 'external_id', 'external_lab_id', 'day_of_birth', 'line', 'sex', 'location', 'responsible_person__name', 'new_owner', 'mutations', 'available_from', 'available_to')
    autocomplete_fields = ['responsible_person']
    list_filter = ('sex', 'responsible_person__responsible_for_lab', 'location')
    radio_fields = {'sex':admin.HORIZONTAL}
    readonly_fields = ('creation_date','modification_date')
    form = AnimalForm
    actions = [clear_claim,]

@admin.register(Lab)
class LabAdmin(admin.ModelAdmin):
    list_display = ('name','responsible_person')
    search_fields=('name',)
