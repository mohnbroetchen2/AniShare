from django import forms
from .models import Animal
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
