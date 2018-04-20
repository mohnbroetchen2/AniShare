from django.contrib import admin
from .models import Animal, Person, Lab

admin.site.site_header = 'Animals2Share admin interface'
admin.site.site_title = 'Animals2Share'
admin.site.index_title = 'Welcome to Animals2Share'

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'email','responsible_for_lab')
    search_fields=('name','email','responsible_for_lab__name')

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ( 'amount', 'entry_date', 'day_of_birth', 'age', 'available_from', 'available_to', 'line', 'sex', 'location', 'new_owner')
    list_display_links = ( 'amount', 'entry_date', 'day_of_birth', 'age', 'available_from', 'available_to', 'line', 'sex', 'location', 'new_owner')
    search_fields = ( 'amount', 'entry_date', 'external_id', 'external_lab_id', 'day_of_birth', 'line', 'sex', 'location', 'responsible_person__name', 'new_owner', 'mutations', 'available_from', 'available_to')
    autocomplete_fields = ['responsible_person']
    list_filter = ('sex', 'responsible_person__responsible_for_lab', 'location')
    radio_fields = {'sex':admin.HORIZONTAL}
    readonly_fields = ('creation_date','modification_date')

@admin.register(Lab)
class LabAdmin(admin.ModelAdmin):
    list_display = ('name','responsible_person')
    search_fields=('name',)


