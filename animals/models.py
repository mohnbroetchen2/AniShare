"""
This file describes all the models in the database.
"""
from datetime import datetime
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User

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
    This person gets emailled when an animal is being claimed.
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

class Animal(models.Model):
    """
    Main model containing the animals.
    """
    amount = models.PositiveIntegerField(default=1,
                                         help_text="How many animals? (eg. fish in tank)")
    animal_type = models.CharField(max_length=100, choices=(
        ('fish', 'fish'),
        ('mouse', 'mouse'),
                                  ),
                                   default='mouse')
#    organ_type = models.CharField(max_length=100, choices=(
#        ('bladder', 'bladder'),
#        ('bone marrow', 'bone marrow'),
#        ('brain', 'brain'),
#        ('genitals', 'genitals'),
#        ('heart', 'heart'),
#        ('intestine', 'intestine'),
#        ('kidney', 'kidney'),
#        ('liver', 'liver'),
#        ('lungs', 'lungs'),
#        ('spleen', 'spleen'),
#        ('stomach', 'stomach'),
#        ('other', 'other'),
#        ('whole animal', 'whole animal'),
#        ),
#                                  default='whole animal')
    database_id = models.CharField(max_length=200, help_text="ID of animal in eg. PYRAT")
    lab_id = models.CharField(max_length=200, help_text="ID of lab in eg. PYRAT")
    creation_date = models.DateTimeField(null=False, auto_now_add=True)
    modification_date = models.DateTimeField(null=False, auto_now=True)
    entry_date = models.DateField(null=False, auto_now_add=True)
    day_of_birth = models.DateField()
    line = models.CharField(max_length=200, help_text="genetic trait of animal")
    sex = models.CharField(max_length=2, choices=(('m', 'male'), ('f', 'female'), ('u', 'unknown')),
                           help_text='Select "unknown" if multiple animals.')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, help_text='Where is the animal housed?')
    mutations = models.TextField(blank=True, null=True, help_text="Describe the mutations of this line in as much detail as possible")
    licence_number = models.CharField(max_length=200)
    responsible_person = models.ForeignKey(Person, on_delete=models.CASCADE, default=0,
                                           help_text='Person who is responsible in the lab for dealing with the animals')
    available_from = models.DateField()
    available_to = models.DateField() # default=datetime.today() + timedelta(days=15))
    comment = models.TextField(blank=True, null=True,
                               help_text='Comments, such as individual organs to be offered')
    new_owner = models.CharField(max_length=200, blank=True,
                                 help_text='Person claiming this animal for themselves') # turn into foreignkey to auth_users?
    added_by = models.ForeignKey(User, unique=False, on_delete=models.CASCADE, default=1)

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



# class Organ(models.Model):
#     """
#     Model containing the organs
#     """
#     amount = models.PositiveIntegerField(default=1,
#                                          help_text="How many of this organ?")
#     animal_type = models.CharField(max_length=100, choices=(
#         ('fish', 'fish'),
#         ('fly', 'fly'),
#         ('mouse', 'mouse'),
#         ('unknown', 'unknown'),
#         ('worm', 'worm')),
#                                    default='mouse')
#     organ_type = models.CharField(max_length=100, choices=(
#         ('bladder', 'bladder'),
#         ('bone marrow', 'bone marrow'),
#         ('brain', 'brain'),
#         ('genitals', 'genitals'),
#         ('heart', 'heart'),
#         ('intestine', 'intestine'),
#         ('kidney', 'kidney'),
#         ('liver', 'liver'),
#         ('lungs', 'lungs'),
#         ('spleen', 'spleen'),
#         ('stomach', 'stomach'),
#         ('other', 'other'),
#         ),
#                                   )
#     external_id = models.CharField(max_length=200, help_text="ID of animal in eg. PYRAT")
#     external_lab_id = models.CharField(max_length=200, help_text="ID of lab in eg. PYRAT")
#     creation_date = models.DateTimeField(null=False, auto_now_add=True)
#     modification_date = models.DateTimeField(null=False, auto_now=True)
#     entry_date = models.DateField(null=False, auto_now_add=True)
#     day_of_birth = models.DateField()
#     day_of_death = models.DateField()
#     method_of_killing = models.CharField(max_length=100, choices=(
#         ('CO2', 'CO2'),
#         ('mazeration', 'mazeration'),
#         ('other', 'other'),
#         ),)
#     killing_person = models.CharField(max_length=200, help_text='Person who is responsible for killing the animal')
#     line = models.CharField(max_length=200, help_text="genetic trait of animal")
#     sex = models.CharField(max_length=2, choices=(('m', 'male'), ('f', 'female'), ('u', 'unknown')),
#                            help_text='Select "unknown" if multiple animals.')
#     location = models.ForeignKey(Location, on_delete=models.CASCADE, help_text='Where is the animal housed?')
#     mutations = models.TextField(blank=True, null=True, help_text="Describe the mutations of this line in as much detail as possible")
#     licence_number = models.CharField(max_length=200)
#     responsible_person = models.ForeignKey(Person, on_delete=models.CASCADE, default=0,
#                                            help_text='Person who is responsible in the lab for dealing with the animals')
#     available_from = models.DateField()
#     available_to = models.DateField() # default=datetime.today() + timedelta(days=15))
#     comment = models.TextField(blank=True, null=True,
#                                help_text='Comments, such as individual organs to be offered')
#     new_owner = models.CharField(max_length=200, blank=True,
#                                  help_text='Person claiming this animal for themselves') # turn into foreignkey to auth_users?
#     added_by = models.ForeignKey(User, unique=False, on_delete=models.CASCADE, default=1)
#
#     def age_at_death(self):
#         """
#         Return the age of the animal, at the time of death
#         """
#         return int((self.day_of_death - self.day_of_birth).days / 7)
#
#     def available(self):
#         """
#         Returns True if the animal is still available
#         """
#         today = datetime.now().date()
#         return (self.available_from <= today) and (today <= self.available_to)
#
#     def get_absolute_url(self):
#         """
#         Get absolute url for this model. Important to link from the admin.
#         """
#         return reverse('animals:claim', kwargs={'primary_key': self.pk})
#
#     def __str__(self):
#         return "{} {} {}, {} id:{} [{}]".format(
#             self.amount, self.get_sex_display(), self.animal_type, self.line, self.pk, self.day_of_birth)
#
#     def description(self):
#         """
#         Return description of this model
#         """
#         return "id:{}, lab_id:{}, available:{}-{}, location:{}, mutations:{}".format(
#             self.external_id, self.external_lab_id, self.available_from,
#             self.available_to, self.location, "".join(self.mutations))
#
