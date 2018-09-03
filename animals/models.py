"""
This file describes all the models in the database.
"""
from datetime import datetime
from django.urls import reverse
from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import post_save

class Lab(models.Model):
    """
    Labs are only defined by a name and are referenced by
    Person(s) which are responsible (contact) person for this lab
    """
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name + ' Lab'
    def responsible_person(self):
        """
        Retrieve only the person(s) which are responsible for this lab.
        """
        persons = Person.objects.filter(responsible_for_lab=self)
        return ', '.join(i.name for i in persons)

class Person(models.Model):
    """
    The responsible (contact) person for each lab.
    This person gets an email when an animal is being claimed.
    """
    name = models.CharField(max_length=200)
    email = models.EmailField()
    responsible_for_lab = models.ForeignKey(Lab, on_delete=models.CASCADE, default=0)
    def __str__(self):
        return self.name + ' (' + str(self.responsible_for_lab) + ')'

class Location(models.Model):
    """
    Location of animals. Eg. animal house, fish facilities etc.
    """
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Change(models.Model):
    """
    Model for documentation all changes to anishare
    """
    change_type = models.CharField(max_length=100, choices=(
        ('new', 'new'),
        ('adaption', 'adaption'),
        ('bugfix', 'bugfix'),
        ('deletion', 'deletion'),
    ), default="adaption")
    version = models.CharField(max_length=200,)
    entry_date = models.DateField(null=False, auto_now_add=True)
    short_text = models.CharField(max_length=400,)
    description = models.TextField(blank=True, null=True,)
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    
    """def __str__(self):
        return "{} {} {}, {} id:{} [{}]".format
        (self.version, self.change_type, self.short_text, self.description, self.pk, self.entry_date)
"""

    def get_absolute_url(self):
        """
        Get absolute url for this model. Important to link from the admin.
        """
        return "/changehistory/?id=%i" % self.pk


class Animal(models.Model):
    """
    Main model containing the animals.
    """
    amount = models.PositiveIntegerField(default=1, 
                                         help_text="How many fishs? (eg. fish in tank). If animal = mouse only one is possible")
    animal_type = models.CharField(max_length=100, choices=(
        ('fish', 'fish'),
        ('mouse', 'mouse'),
    ),
                                   default='mouse')
    database_id = models.CharField(max_length=200, help_text="ID of animal in eg. PYRAT")
    lab_id = models.CharField(max_length=200, null=True, blank=True, help_text="ID of lab in eg. PYRAT")
    creation_date = models.DateTimeField(null=False, auto_now_add=True)
    modification_date = models.DateTimeField(null=False, auto_now=True)
    entry_date = models.DateField(null=False, auto_now_add=True)
    day_of_birth = models.DateField()
    genetic_background = models.CharField(max_length=200,blank=True, null=True)
    line = models.CharField(max_length=200, help_text="genetic trait of animal")
    sex = models.CharField(max_length=2, choices=(('m', 'male'), ('f', 'female'), ('u', 'unknown')),
                           help_text='Select "unknown" if multiple animals.')
    location = models.ForeignKey(Location, on_delete=models.CASCADE,
                                 help_text='Where is the animal housed?')
    mutations = models.TextField(blank=True, null=True,
                                 help_text="Describe the mutations with the grade of this line in as much detail as possible")
    grade = models.CharField(max_length=200, null=True, blank=True, help_text="")
    """grade1 = models.CharField(max_length=10, null=True, choices=(
        ('+/+', '+/+'),
        ('+/0', '+/0'),
        ('-/+', '-/+'),
        ('-/-', '-/-'),
        ('-/0', '-/0'),
        ('0/fl', '0/fl'),
        ('fl/+', 'fl/+'),
        ('fl/-', 'fl/-'),
        ('fl/fl', 'fl/fl'),
        ('fl/tg', 'fl/tg'),
        ('ki/+', 'ki/+'),
        ('ki/fl', 'ki/fl'),
        ('ki/ki', 'ki/ki'),
        ('ko/+', 'ko/+'),
        ('ko/0', 'ko/0'),
        ('ko/ko', 'ko/ko'),
        ('tg/+', 'tg/+'),
        ('tg/?', 'tg/?'),
        ('tg/tg', 'tg/tg'),
        ('tki/+', 'tki/+'),
        ('tki/tki', 'tki/tki'),
        ('W41/+', 'W41/+'),
        ('W41/W41', 'W41/W41'),
        ('Wv/+', 'Wv/+'),
        ('Wv/Wv', 'Wv/Wv'),
        ('y/-', 'y/-'),
        ),help_text='Grade 1',)"""
    grade1 = models.CharField(max_length=10, null=True,help_text='Grade 1')
    grade2 = models.CharField(max_length=10, null=True,help_text='Grade 2')
    grade3 = models.CharField(max_length=10, null=True ,help_text='Grade 3')
    grade4 = models.CharField(max_length=10, null=True ,help_text='Grade 4')
    licence_number = models.CharField(max_length=200, verbose_name='License number')
    responsible_person = models.ForeignKey(Person, related_name='rperson', on_delete=models.CASCADE, help_text='Person who is responsible in the lab for dealing with the animals')
    responsible_person2 = models.ForeignKey(Person, related_name='rperson2', null=True, blank=True, on_delete=models.CASCADE, 
                                            help_text='Second person who is responsible in the lab for dealing with the animals', verbose_name = "Second responsible person")
    #responsible_person = models.ManyToManyField(Person, related_name='Responsible_person', help_text='Person who is responsible in the lab for dealing with the animals')
    available_from = models.DateField()
    available_to = models.DateField() # default=datetime.today() + timedelta(days=15))
    comment = models.TextField(blank=True, null=True,
                               help_text='Comments, such as individual organs to be offered')
    new_owner = models.CharField(max_length=200, blank=True,
                                 help_text='Person claiming this animal for themselves') # turn into foreignkey to auth_users?
    added_by = models.ForeignKey(User, unique=False, on_delete=models.CASCADE, default=1)

    def validate_amount(value):
        if (self.animal_type != 'fish' and value != 1):
            raise ValidationError('Only one mouse is possible')

    def clean(self):
        animal_type = self.animal_type
        amount = self.amount
        if (animal_type != 'fish' and amount != 1):
            raise ValidationError('Only one mouse is possible')

    def background(self):
        if self.genetic_background is None:
            return ("")
        else:
            return(self.genetic_background)

    def responsible_persons(self):
        if str(self.responsible_person2) != "None":
            return (str(self.responsible_person) + str(" ") +str(self.responsible_person2))
        return (self.responsible_person)


    def age(self):
        """
        Return the age of the animal, calculated by the difference to either
        the current date or the available_to date
        """
#        return int((self.entry_date - self.day_of_birth).days / 7)
        now = datetime.today().date()
        if now < self.available_to:
            return int((now - self.day_of_birth).days / 7)
        return int((self.available_to - self.day_of_birth).days / 7)

    def available(self):
        """
        Returns True if the animal is still available
        """
        today = datetime.now().date()
        return (self.available_from <= today) and (today <= self.available_to)

    def get_absolute_url(self):
        """
        Get absolute url for this model. Important to link from the admin.
        """
        return reverse('animals:claim', kwargs={'primary_key': self.pk})

    def __str__(self):
        return "{} {} {}, {} id:{} [{}]".format(
            self.amount, self.get_sex_display(), self.animal_type, self.line, self.pk, self.day_of_birth)

    def description(self):
        """
        Return description of this model
        """
        return "id:{}, lab_id:{}, available:{}-{}, location:{}, mutations:{}".format(
            self.database_id, self.lab_id, self.available_from,
            self.available_to, self.location, "".join(self.mutations))

class Organtype(models.Model):
    """
    Model containing the organ types
    """
    """ name = models.CharField(max_length=100, choices=(
        ('bladder', 'bladder'),
        ('bone marrow', 'bone marrow'),
        ('brain', 'brain'),
        ('genitals', 'genitals'),
        ('heart', 'heart'),
        ('intestine', 'intestine'),
        ('kidney', 'kidney'),
        ('liver', 'liver'),
        ('lungs', 'lungs'),
        ('spleen', 'spleen'),
        ('stomach', 'stomach'),
        ('other', 'other'),
        ),help_text='Organ type which is not available',)"""
    name = models.CharField(max_length=100,)
    class Meta:
        verbose_name = "presets for used organs"
        verbose_name_plural = "Organs used"
    def __str__(self):
        return self.name

class FishPeople(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    login = models.CharField(db_column='LOGIN', max_length=255, help_text="ID of animal in eg. PYRAT")
    firstname = models.CharField(db_column='FIRSTNAME', max_length=255, help_text="ID of animal in eg. PYRAT")
    lastname = models.CharField(db_column='LASTNAME', max_length=255, help_text="ID of animal in eg. PYRAT")

    class Meta:
        managed = False
        db_table = 'vPerson'

class Fish(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    animalnumber = models.CharField(db_column='ANIMALNUMBER', max_length=255, help_text="Anima-ID")
    identifier1 = models.CharField(db_column='IDENTIFIER1', max_length=255)
    identifier2 = models.CharField(db_column='IDENTIFIER2', max_length=255)
    identifier3 = models.CharField(db_column='IDENTIFIER3', max_length=255)
    identifier4 = models.CharField(db_column='IDENTIFIER4', max_length=255)
    sex = models.IntegerField(db_column='SEX')
    quantity = models.IntegerField(db_column='QUANTITY')
    dob = models.DateField(db_column='DOB')
    notes = models.CharField(db_column='NOTES', max_length=4000)
    responsible = models.CharField(db_column='RESPONSIBLE', max_length=512)
    responsible_email = models.CharField(db_column='RESPONSIBLE_EMAIL', max_length=512)
    location = models.CharField(db_column='LOCATION', max_length=4000)
    license = models.CharField(db_column='LICENSE', max_length=255)
    strain = models.CharField(db_column='STRAIN', max_length=255)

    def age(self):
        """
        Return the age of the animal, calculated by the difference to either
        the current date or the available_to date
        """
        now = datetime.today().date()
        return int((now - self.dob).days / 7)

    class Meta:
        managed = False
        db_table = 'FISHS_ALIVE'


class Organ(models.Model):
    """
    Model containing the organs
    """
    """amount = models.PositiveIntegerField(default=1,
                                         help_text="How many organs?")"""
    animal_type = models.CharField(max_length=100, choices=(
        ('fish', 'fish'),
        ('mouse', 'mouse'),
        ('unknown', 'unknown'),
        ),
                                   default='mouse')
    sex = models.CharField(max_length=2, choices=(('m', 'male'), ('f', 'female'), ('u', 'unknown')),
                           help_text='Select "unknown" if multiple animals.')
    organ_type = models.ManyToManyField(Organtype, related_name='Organ_used', verbose_name='presets for used organs')
    day_of_birth = models.DateField()
    day_of_death = models.DateField()
    method_of_killing = models.CharField(null=True, blank=True,verbose_name='Sacrifice method', max_length=100, choices=(
        ('CO2', 'CO2'),
        ('cervicale dislocation', 'cervicale dislocation'),
        ('decapitation', 'decapitation'),
        ('blood withdrawl', 'blood withdrawl'),
        ('finale heart punction', 'finale heart punction'),
        ('overdose anaesthetics', 'overdose anaesthetic'),
        ('other', 'other'),
        ),)
    killing_person = models.EmailField(verbose_name='Euthanasia performed by',null=True, blank=True, help_text='Email address of the person who performe euthanasia. Leave it empty if it is the address of the responsible person')
    database_id = models.CharField(max_length=200, help_text="ID of animal in eg. PYRAT")
    lab_id = models.CharField(max_length=200, null=True, blank=True, help_text="ID of lab in eg. PYRAT")
    entry_date = models.DateField(null=False, auto_now_add=True)
    line = models.CharField(max_length=200, help_text="genetic trait of animal")
    genetic_background = models.CharField(max_length=200, blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, help_text='Where is the animal housed?')
    licence_number = models.CharField(max_length=200, blank=True, verbose_name='License number')
    responsible_person = models.ForeignKey(Person, related_name='rperson_organ', on_delete=models.CASCADE, default=0,
                                           help_text='Person who is responsible in the lab for dealing with the animals')
    responsible_person2 = models.ForeignKey(Person,  related_name='rperson2_organ', null=True, blank=True, on_delete=models.CASCADE, 
                                            help_text='Second person who is responsible in the lab for dealing with the animals', verbose_name = "Second responsible person")
    mutations = models.TextField(blank=True, null=True, help_text="Describe the mutations of this line in as much detail as possible")
    comment = models.TextField(blank=True, null=True,
                               help_text='Comments, such as individual organs to be offered')
#    new_owner = models.CharField(max_length=200, blank=True,
#                                 help_text='Person claiming this animal for themselves') # turn into foreignkey to auth_users?
    creation_date = models.DateTimeField(null=False, auto_now_add=True)
    modification_date = models.DateTimeField(null=False, auto_now=True)
    added_by = models.ForeignKey(User, unique=False, on_delete=models.CASCADE, default=1)

    def get_organtypes(self):
        """Get all organ types which are used"""
        return ",\n".join([ot.name for ot in self.organ_type.all()])
    get_organtypes.short_description ='ORGAN TYPE (used)'

    def background(self):
        if self.genetic_background is None:
            return ("")
        else:
            return(self.genetic_background)

    def responsible_persons(self):
        if str(self.responsible_person2) != "None":
            return (str(self.responsible_person) + str(" ") +str(self.responsible_person2))
        return (self.responsible_person)

    def age(self):
        """
        Return the age of the animal, at the time of death
        """
        return int((self.day_of_death - self.day_of_birth).days / 7)

    def available(self):
        """
        Returns True if the animal is still available
        """
        today = datetime.now().date()
        return self.day_of_death >= today

    def get_absolute_url(self):
        """
        Get absolute url for this model. Important to link from the admin.
        """
        return reverse('claim_organ', kwargs={'primary_key': self.pk})

    def __str__(self):
        return " {} {}, {} id:{} [{}]".format(
            self.get_sex_display(), self.animal_type, self.line, self.pk, self.day_of_birth)

    def description(self):
        """
        Return description of this model
        """
        return "id:{}, lab_id:{}, available:{}-{}, location:{}, mutations:{}".format(
            self.database_id, self.lab_id, self.day_of_birth,
            self.day_of_death, self.location, "".join(self.mutations))

@receiver(post_save, sender=Organ) # check if killing_person (mail address) is given. If not save the mail address of the responsible person as killing_person 
def update_killing_person(sender, instance, created, **kwargs):
    if (instance.killing_person == None):
        instance.killing_person = instance.responsible_person.email
        instance.save()

# class ClaimOrgan(forms.Form):
#    organUsed=forms.ModelMultipleChoiceField(queryset=Organtype.objects.all(),widget=forms.CheckboxSelectMultiple())
