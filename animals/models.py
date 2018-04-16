from django.db import models
from datetime import datetime, timedelta

class Lab(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name + ' Lab'

class Person(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    responsible_for_lab = models.ForeignKey(Lab, on_delete=models.CASCADE, default=0)
    def __str__(self):
        return self.name + ' (' + str(self.responsible_for_lab) + ')'

class Animal(models.Model):
    amount = models.IntegerField(default=1, help_text="How many animals? (eg. fish in tank)")
    pyrat_id = models.CharField(max_length=200)
#    nr = models.IntegerField(null=False)
    entry_date = models.DateField(null=False, auto_now_add=True)
    pyrat_lab_id = models.CharField(max_length=200)
    day_of_birth = models.DateField()
    line = models.CharField(max_length=200)
    sex = models.CharField(max_length=2, choices = (('m','male'),('f','female'), ('u','unknown')))
    location = models.CharField(max_length=200)
    mutations = models.TextField(blank=True,null=True)
    licence_number = models.CharField(max_length=200)
    responsible_person = models.ForeignKey(Person, on_delete=models.CASCADE, default=0)
    available_from = models.DateField(default=datetime.now)
    available_to = models.DateField(default=datetime.today() + timedelta(days=14))
    new_owner = models.CharField(max_length=200, blank=True) # turn into foreignkey to auth_users?

    def age(self):
        return int((self.entry_date - self.day_of_birth).days / 7)

    def __str__(self):
        return self.licence_number

 # Nr.	Entry date	ID	Lab ID	DOB	Age (w)	Line / Strain	Mutation 1	Grade 1	Mutation 2	Grade 2	Mutation 3	Grade 3	Mutation 4	Grade 4	Sex	Building	Licence number	Responsible person	Available from	Available until	New Owner
