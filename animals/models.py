from django.urls import reverse
from django.db import models
from datetime import datetime, timedelta

class Lab(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name + ' Lab'
    def responsible_person(self):
        persons = Person.objects.filter(responsible_for_lab=self)
        return ', '.join(i.name for i in persons)

class Person(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    responsible_for_lab = models.ForeignKey(Lab, on_delete=models.CASCADE, default=0)
    def __str__(self):
        return self.name + ' (' + str(self.responsible_for_lab) + ')'

class Animal(models.Model):
    amount = models.PositiveIntegerField(default=1, help_text="How many animals? (eg. fish in tank)")
    animal_type = models.CharField(max_length=100, choices = (
        ('mouse', 'mus musculus'),
        ('fish','fish'),
        ('u','unknown')),
        default='mouse')
    external_id = models.CharField(max_length=200)
    external_lab_id = models.CharField(max_length=200)
    creation_date = models.DateTimeField(null=False, auto_now_add=True)
    modification_date = models.DateTimeField(null=False, auto_now=True)
    entry_date = models.DateField(null=False, default=datetime.now)
    day_of_birth = models.DateField()
    line = models.CharField(max_length=200)
    sex = models.CharField(max_length=2, choices = (('m','male'),('f','female'), ('u','unknown')))
    location = models.CharField(max_length=200)
    mutations = models.TextField(blank=True,null=True)
    licence_number = models.CharField(max_length=200)
    responsible_person = models.ForeignKey(Person, on_delete=models.CASCADE, default=0)
    available_from = models.DateField(default=datetime.now)
    available_to = models.DateField(default=datetime.today() + timedelta(days=15))
    comment = models.TextField(blank=True, null=True)
    new_owner = models.CharField(max_length=200, blank=True) # turn into foreignkey to auth_users?

    def age(self):
        return int((self.entry_date - self.day_of_birth).days / 7)

    def available(self):
        today = datetime.now().date()
        return (self.available_from <= today) and (today <= self.available_to)

    def get_absolute_url(self):
        return reverse('animals:animal-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return "{} {} {}, {} id:{} [{}]".format(
            self.amount, self.get_sex_display(), self.animal_type, self.line, self.pk, self.day_of_birth)

    def description(self):
        return "id:{}, lab_id:{}, available:{}-{}, location:{}, mutations:{}".format(
            self.external_id, self.external_lab_id, self.available_from, self.available_to, self.location, "".join(self.mutations))
