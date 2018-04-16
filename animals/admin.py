from django.contrib import admin

from .models import Animal, Person, Lab

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
    list_display = ('name', 'email','responsible_for_lab')
    search_fields=('name','email','responsible_for_lab__name')

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ( 'amount', 'entry_date', 'age', 'pyrat_id', 'pyrat_lab_id', 'day_of_birth', 'line', 'sex', 'location', 'responsible_person', 'available_from', 'available_to')
    autocomplete_fields = ['responsible_person']
    list_filter = ('sex', 'responsible_person__responsible_for_lab', 'location')
#    readonly_fields = ('age',)

admin.site.register(Lab)
