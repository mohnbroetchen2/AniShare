"""
Admin module
"""
import copy
from import_export.admin import ImportExportModelAdmin
from datetime import datetime, timedelta
from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget
from django.contrib import admin
from django import forms
from django.conf import settings
from rangefilter.filter import DateRangeFilter # , DateTimeRangeFilter
from .models import Animal, Person, Lab, Location, Organ


admin.site.site_header = 'AniShare admin interface'
admin.site.site_title = 'AniShare'
admin.site.index_title = 'Welcome to AniShare'

class AnimalResource(resources.ModelResource): # für den Import. Hier werden die Felder festgelegt, die importiert werden können
    location = fields.Field(
        column_name='location',
        attribute='location',
        widget=ForeignKeyWidget(Location, 'name'))
    responsible_person = fields.Field(
        column_name='responsible_person',
        attribute='responsible_person',
        widget=ForeignKeyWidget(Person, 'email'))
    class Meta:
        model = Animal
        fields = ('lab_id','animal_type', 'amount', 'database_id','day_of_birth', 'lab_id',
        'line','sex','location','mutations','licence_number',
        'responsible_person','available_from','available_to','comment',)
    def get_instance(self, instance_loader, row):
        try:
            params = {}
            for key in instance_loader.resource.get_import_id_fields():
                field = instance_loader.resource.fields[key]
                params[field.attribute] = field.clean(row)
            return self.get_queryset().get(**params)
        except Exception:
            return None


class AnimalForm(forms.ModelForm):
    """
    Form for animal editing in admin
    """
    class Meta:
        model = Animal
        fields = ('amount', 'animal_type', 'day_of_birth',
                  'available_from', 'available_to', 'sex', 'database_id',
                  'lab_id', 'line', 'location', 'responsible_person',
                  'licence_number', 'mutations', 'comment', 'new_owner', )

    def clean(self):
        available_from = self.cleaned_data.get('available_from')
        available_to = self.cleaned_data.get('available_to')
        day_of_birth = self.cleaned_data.get('day_of_birth')
#        self.author =  request.user
        if available_from > available_to:
            raise forms.ValidationError("Dates are incorrect")
        if day_of_birth and (
                (datetime.now().date() -  day_of_birth) <=
                timedelta(days=settings.MIN_SHARE_DURATION_PUPS)):
            if available_to - available_from <= timedelta(days=settings.MIN_SHARE_DURATION_PUPS):
                raise forms.ValidationError(
                    "Minimum share duration for pups must be {} days!".format(
                        settings.MIN_SHARE_DURATION_PUPS))
        elif available_to - available_from <= timedelta(days=settings.MIN_SHARE_DURATION):
            raise forms.ValidationError(
                "Minimum share duration must be {} days!".format(settings.MIN_SHARE_DURATION))
        return self.cleaned_data

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    """
    ModelAdmin for Person model
    """
    list_display = ('name', 'email', 'responsible_for_lab')
    search_fields = ('name', 'email', 'responsible_for_lab__name')
    ordering = ('name', )

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """
    ModelAdmin for Location model
    """
    list_display = ('name',)
    search_fields = ('name',)

def clear_claim(modeladmin, request, queryset):
    """
    Convenience Function to delete a claim from several selected animals
    """
    queryset.update(new_owner='')
    clear_claim.short_description = "Clear 'new_owner' from selected animals"

def copy_animal(modeladmin, request, queryset):
    """
    Copy an instance of an animal so similar entries can be easily created.
    """
    for animal in queryset:
        animal_copy = copy.copy(animal) # (2) django copy object
        animal_copy.id = None   # (3) set 'id' to None to create new object
        animal_copy.save()    # initial save

    copy_animal.short_description = "Make a Copy of an entry"



@admin.register(Animal)
#class AnimalAdmin(admin.ModelAdmin):

class AnimalAdmin(ImportExportModelAdmin):
    """
    ModelAdmin for Animal model
    """
    resource_class = AnimalResource
    list_display = ('amount', 'entry_date', 'day_of_birth', 'age', 'available_from',
                    'available_to', 'line', 'sex', 'location', 'licence_number', 'lab_id',
                    'responsible_person', 'added_by', 'new_owner')
    list_display_links = ('amount', 'entry_date', 'day_of_birth', 'age',
                          'available_from', 'available_to', 'line', 'sex',
                          'location', 'licence_number', 'lab_id','responsible_person',
                          'added_by', 'new_owner')
    search_fields = ('amount', 'database_id', 'lab_id', 'day_of_birth',
                     'line', 'sex', 'location__name', 'new_owner', 'licence_number',
                     'mutations', 'available_from', 'available_to', 'responsible_person__name',
                     'responsible_person__email', 'added_by__email')
    autocomplete_fields = ['responsible_person']
    list_filter = ('amount', 'sex', 'responsible_person__responsible_for_lab',
                   ('day_of_birth', DateRangeFilter),
                   'location', 'licence_number', 'new_owner', 'added_by')
    radio_fields = {'sex':admin.HORIZONTAL}
    readonly_fields = ('creation_date', 'modification_date')
    form = AnimalForm
    save_as = True
    save_on_top = True
    actions = [clear_claim, copy_animal]
    def age(self, obj):
        """Show the age in the admin as 'Age (w)' instead of 'age'"""
        return obj.age()
    age.short_description = 'Age (w)'
#    def formfield_for_foreignkey(self, db_field, request, **kwargs):
#        if db_field.name == 'author':
#            kwargs['queryset'] = get_user_model().objects.filter(username=request.user.username)
#        return super(AnimalAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            # Only set added_by during the first save.
            obj.added_by = request.user
        super().save_model(request, obj, form, change)



@admin.register(Organ)
class OrganAdmin(admin.ModelAdmin):
    """
    ModelAdmin for Organ model
    """
    list_display = ('amount', 'animal_type', 'organ_type', 'entry_date', 'day_of_birth',
                    'day_of_death', 'age', 'method_of_killing', 'killing_person', 'line',
                    'sex', 'location','lab_id', 'licence_number', 'responsible_person', 'added_by')
    list_display_links = ('amount', 'animal_type', 'organ_type', 'entry_date', 'day_of_birth',
                          'day_of_death', 'age', 'method_of_killing', 'killing_person', 'line',
                          'sex', 'location','lab_id', 'licence_number', 'responsible_person', 'added_by')
    search_fields = ('amount', 'animal_type', 'organ_type', 'entry_date', 'day_of_birth',
                     'day_of_death', 'age', 'method_of_killing', 'killing_person', 'line',
                     'sex', 'location', 'licence_number', 'responsible_person', 'added_by')
    autocomplete_fields = ['responsible_person']
    list_filter = ('amount', 'sex',
                   ('day_of_birth', DateRangeFilter), ('day_of_death', DateRangeFilter),
                   'responsible_person__responsible_for_lab',
                   'location', 'licence_number', 'added_by',)
    radio_fields = {'sex':admin.HORIZONTAL}
    readonly_fields = ('added_by', 'creation_date', 'modification_date')
    save_as = True
    save_on_top = True
#    form = OrganForm
    actions = [clear_claim, copy_animal]

    def age(self, obj):
        """Show the age in the admin as 'Age (w)' instead of 'age'"""
        return obj.age()
    age.short_description = 'Age (w)'

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            # Only set added_by during the first save.
            obj.added_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Lab)
class LabAdmin(admin.ModelAdmin):
    """
    ModelAdmin for Lab model
    """
    list_display = ('name', 'responsible_person')
    search_fields = ('name',)
