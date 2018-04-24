from django.views import generic
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.core.mail import send_mail
from datetime import datetime
#from django.core.urlresolvers import reverse_lazy

from .models import Animal

def claim(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    return render(request, 'animals/animal-claim.html', {'object': animal})

class AnimalDetailView(LoginRequiredMixin,generic.DetailView):
    model = Animal
    template_name = 'animals/animal-detail.html'

# class AnimalCreateView(LoginRequiredMixin,generic.CreateView):
    # model = Animal
    # fields = ( 'amount', 'available_from', 'available_to', 'day_of_birth', 'entry_date', 'external_id', 'external_lab_id', 'line', 'location', 'mutations', 'new_owner', 'responsible_person', 'sex',)

# class AnimalDeleteView(LoginRequiredMixin,generic.DeleteView):
#     model = Animal
# #    success_url = reverse_lazy('animals-list')

# class AnimalUpdateView(LoginRequiredMixin,generic.UpdateView):
#     model = Animal
#     fields = ( 'amount', 'available_from', 'available_to', 'day_of_birth', 'entry_date', 'external_id', 'external_lab_id', 'line', 'location', 'mutations', 'new_owner', 'responsible_person', 'sex',)

class AnimalIndexView(LoginRequiredMixin,generic.ListView):
    model = Animal
    template_name = 'animals/index.html'
    context_object_name = 'all_animals'
    paginate_by = 100
    def get_queryset(self):
        """Return the latest additions to the Animals table"""
        return Animal.objects.order_by('-entry_date')#[:100]


def send_email(request):
    email = request.POST['email']
    pk = request.POST['pk']
    animal = Animal.objects.get(pk=pk)
    animal.new_owner = email
    animal.save()
    subject = "User {} claimed animal {} in AniShare".format(email, pk)
    message = "Dear " + animal.responsible_person.name +\
    ",\nOn " + str(datetime.now()) +\
    " " + email + " " + \
    "claimed " + str(animal.amount) + " " + animal.animal_type + " with id " + str(animal.pk) + ".\n" +\
    "Further information:\n" + "\n" +\
    "external_id: " + animal.external_id  + "\n" +\
    "external_lab_id: " + animal.external_lab_id  + "\n" +\
    "day_of_birth: " + str(animal.day_of_birth)  + "\n" +\
    "line: " + animal.line  + "\n" +\
    "sex: " + animal.sex  + "\n" +\
    "location: " + animal.location  + "\n" +\
    "mutations: " + str(animal.mutations)  + "\n" +\
    "licence_number: " + str(animal.licence_number)  + "\n" +\
    "comment: " + str(animal.comment)

    send_mail(
        subject,
        message,
        email,
        [animal.responsible_person.email,],
        fail_silently=False,
        )
    return HttpResponseRedirect('/')
