"""
This file describes all the models in the database.
"""
from datetime import datetime
from django.urls import reverse
from django.db import models
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
    
    def __str__(self):
        return "{} {} {}, {} id:{} [{}]".format
        (self.version, self.change_type, self.short_text, self.description, self.pk, self.entry_date)


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
    database_id = models.CharField(max_length=200, help_text="ID of animal in eg. PYRAT", default="0")
    lab_id = models.CharField(max_length=200, null=True, blank=True, help_text="ID of lab in eg. PYRAT")
    creation_date = models.DateTimeField(null=False, auto_now_add=True)
    modification_date = models.DateTimeField(null=False, auto_now=True)
    entry_date = models.DateField(null=False, auto_now_add=True)
    day_of_birth = models.DateField()
    line = models.CharField(max_length=200, help_text="genetic trait of animal")
    sex = models.CharField(max_length=2, choices=(('m', 'male'), ('f', 'female'), ('u', 'unknown')),
                           help_text='Select "unknown" if multiple animals.')
    location = models.ForeignKey(Location, on_delete=models.CASCADE,
                                 help_text='Where is the animal housed?')
    mutations = models.TextField(blank=True, null=True,
                                 help_text="Describe the mutations of this line in as much detail as possible")
    licence_number = models.CharField(max_length=200)
    responsible_person = models.ForeignKey(Person, on_delete=models.CASCADE, help_text='Person who is responsible in the lab for dealing with the animals')
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
    location = models.ForeignKey(Location, on_delete=models.CASCADE, help_text='Where is the animal housed?')
    licence_number = models.CharField(max_length=200, blank=True)
    responsible_person = models.ForeignKey(Person, on_delete=models.CASCADE, default=0,
                                           help_text='Person who is responsible in the lab for dealing with the animals')
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
