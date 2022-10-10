from django import forms
from .models import Animal, Organ, Organtype, Person
from datetime import datetime, timedelta

class addAnimalForm(forms.ModelForm): 
    date_from = datetime.today()
    date_to = datetime.today() + timedelta(days=14)
    available_from   = forms.DateTimeField(input_formats=['%d/%m/%Y'], initial=date_from.strftime("%d/%m/%Y")) #https://simpleisbetterthancomplex.com/tutorial/2019/01/03/how-to-use-date-picker-with-django.html
    available_to     = forms.DateTimeField(input_formats=['%d/%m/%Y'], initial=date_to.strftime("%d/%m/%Y"))
    day_of_birth     = forms.DateTimeField(input_formats=['%d/%m/%Y'])

    class Meta:
        model = Animal
        exclude = ('database_id','fish_id','mouse_id','pup_id','fish_specie','new_owner','added_by','pyrat_incidentid','lab_id')

class addOrganForm(forms.ModelForm):
    date_from = datetime.today()
    date_to = datetime.today() + timedelta(days=14)
    day_of_birth        = forms.DateTimeField(input_formats=['%d/%m/%Y'])
    day_of_death        = forms.DateTimeField(input_formats=['%d/%m/%Y'])
    organ_type          = forms.ModelMultipleChoiceField(queryset=Organtype.objects.all().order_by('name'), help_text='Select used organs')
    responsible_person  = forms.ModelChoiceField(queryset=Person.objects.order_by('name'), help_text='This person will be informed if someone is claiming an organ')
    line                = forms.CharField(label="Strain")
    animal_type         = forms.ChoiceField(choices=(
        ('fish', 'fish'),
        ('mouse', 'mouse'),
        ('unknown', 'unknown'),
        ), label='Specie')
    field_order = ['animal_type', 'sex', 'day_of_birth', 'day_of_death','organ_type','line','responsible_person','genetic_background','mutations']
    class Meta:
        model = Organ
        exclude = ('database_id','lab_id','entry_date','institution','creation_date','modification_date','added_by','responsible_person2','killing_person')