"""
Django Views contains all the functions for rendering objects (HTML display).
It also contains an RSS Feed generator class to create an RSS feed from newly created animals

**Important**:
    When adding new functions, use the login_required decorator
    When adding new classes, use the LoginRequiredMixin
"""
import operator
from functools import reduce
from datetime import datetime
from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.syndication.views import Feed
from django.db.models import Q
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
#from django.urls import reverse
from django.views import generic

from .models import Animal, Organ

@login_required
def claim(request, primary_key):
    """
    View to claim an animal.

    :param primary_key: the id/pk of the animal to retrieve

    :returns: rendered page with the claim form
              or 404 if animal not found
    """
    animal = get_object_or_404(Animal, pk=primary_key)
    return render(request, 'animals/animal-claim.html', {'object': animal})

@login_required
def claim_organ(request, primary_key):
    """
    View to claim an organ.

    :param primary_key: the id/pk of the organ to retrieve

    :returns: rendered page with the claim form
              or 404 if organ not found
    """
    organ = get_object_or_404(Organ, pk=primary_key)
    return render(request, 'animals/organ-claim.html', {'object': organ})

class AnimalDetailView(LoginRequiredMixin, generic.DetailView):
    """
    Detail view for an animal.
    This is rarely used, rather use the claim page.
    """
    model = Animal
    template_name = 'animals/animal-detail.html'

class AnimalIndexView(LoginRequiredMixin, generic.ListView):
    """
    Index / List view for all available animals.
    Generic ListView using the LoginRequiredMixin

    :param q: query / search term to filter the results
    :param show: limit the results to 'current', 'archive', or all animals
    """
    model = Animal
    template_name = 'animals/index.html'
    context_object_name = 'all_animals'
    paginate_by = 100
    def get_queryset(self):
        """Return the latest additions to the Animals table"""
        result = super(AnimalIndexView, self).get_queryset()
        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_, (Q(comment__icontains=q) for q in query_list)) |
                reduce(operator.and_, (Q(mutations__icontains=q) for q in query_list)) |
                reduce(operator.and_, (Q(database_id__icontains=q) for q in query_list)) |
                reduce(operator.and_, (Q(line__icontains=q) for q in query_list)) |
                reduce(operator.and_, (Q(lab_id__icontains=q) for q in query_list)) |
                reduce(operator.and_, (Q(location__name__icontains=q) for q in query_list)) |
                reduce(operator.and_, (Q(new_owner__icontains=q) for q in query_list)) |
                reduce(operator.and_, (Q(responsible_person__name__icontains=q) for q in query_list)) |
                reduce(operator.and_, (Q(licence_number__icontains=q) for q in query_list))
            )
            return result
        try:
            show = self.kwargs['show']
        except KeyError:
            show = 'current'
        if show == 'archive':
            return Animal.objects.filter(available_to__lte=datetime.now().date()).order_by('-entry_date')
        elif show == 'current':
            return Animal.objects.filter(available_to__gte=datetime.now().date()).order_by('-entry_date')
        return Animal.objects.order_by('-entry_date')

class OrganIndexView(LoginRequiredMixin, generic.ListView):
    """
    Index / List view for all available Organs.
    Generic ListView using the LoginRequiredMixin

    :param q: query / search term to filter the results
    :param show: limit the results to 'current', 'archive', or all Organs
    """
    model = Organ
    template_name = 'animals/organs.html'
    context_object_name = 'all_organs'
    paginate_by = 100
    def get_queryset(self):
        """Return the latest additions to the Organs table"""
        result = super(OrganIndexView, self).get_queryset()
        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_, (Q(comment__icontains=q) for q in query_list)) |
                reduce(operator.and_, (Q(mutations__icontains=q) for q in query_list)) |
                reduce(operator.and_, (Q(database_id__icontains=q) for q in query_list)) |
                reduce(operator.and_, (Q(line__icontains=q) for q in query_list)) |
                reduce(operator.and_, (Q(lab_id__icontains=q) for q in query_list)) |
                reduce(operator.and_, (Q(location__name__icontains=q) for q in query_list)) |
                reduce(operator.and_, (Q(responsible_person__name__icontains=q) for q in query_list)) |
                reduce(operator.and_, (Q(licence_number__icontains=q) for q in query_list))
            )
            return result
        return Organ.objects.order_by('-entry_date')

def send_email_animal(request):
    """
    Function to send an email about an animal being claimed.

    Needs these variables in the POST request: email, pk, count

    :param email: email address of the request user / new owner
    :param pk: primary_key of the animal(s) to be claimed
    :param count: how many animals are being claimed
    """
    email = request.POST['email']
    primary_key = request.POST['pk']
    count = request.POST['count']

    animal = Animal.objects.get(pk=primary_key)
    animal.new_owner = email
    amount_difference = int(animal.amount)-int(count)
    if amount_difference < 0:  # Save remainder of animals as new object
        messages.add_message(request, messages.ERROR, 'You cannot claim more animals then are available!')
        raise forms.ValidationError("You cannot claim more animals then are available!")
    animal.amount = count
    animal.save()  # Save the animal with the new owner
    messages.add_message(request, messages.SUCCESS,
                         'The entry {} has been claimed by {}.'.format(animal.pk, animal.new_owner))
    subject = "User {} claimed animal {} in AniShare".format(email, primary_key)
    message = render_to_string('email.html', {'email': email, 'object': animal, 'now': datetime.now()})

    msg = EmailMessage(subject, message, email, [animal.responsible_person.email, email])
    msg.content_subtype = "html"
    msg.send()
    if amount_difference > 0:  # If there were multiple animals, save the remainder of animals as a new object
        animal.pk = None
        animal.amount = amount_difference
        animal.new_owner = ''
        animal.save()
        messages.add_message(request, messages.SUCCESS, 'The amount of available animals in this entry has been reduced to {}.'.format(animal.amount))
    messages.add_message(request, messages.SUCCESS, 'An Email has been sent to <{}>.'.format(animal.responsible_person.email))

    return HttpResponseRedirect('/')

def send_email_organ(request):
    """
    Function to send an email about an animal being claimed.

    Needs these variables in the POST request: email, pk, count

    :param email: email address of the request user / new owner
    :param pk: primary_key of the animal(s) to be claimed
    :param organs_wanted: organs wanted from the given animal
    """
    email = request.POST['email']
    primary_key = request.POST['pk']
    organs_wanted = request.POST['organs_wanted']

    organ = Organ.objects.get(pk=primary_key)
    subject = "AniShare User {} claimed organ(s) {}".format(email, organs_wanted)
    message = render_to_string('email.html', {'email': email, 'organs_wanted':organs_wanted, 'object': organ, 'now': datetime.now()})

    msg = EmailMessage(subject, message, email, [organ.responsible_person.email, email])
    msg.content_subtype = "html"
    print(msg.message())
#    msg.send()
    messages.add_message(request, messages.SUCCESS, 'An Email has been sent to <{}>.'.format(organ.responsible_person.email))

    return HttpResponseRedirect('/organs/')


class LatestAnimalsFeed(Feed):
    """
    RSS Feed for new animals.
    """
    title = 'Anishare animal feed'
    link = '/animals/feed'
    description = 'Updates on animals to share.'

    def __call__(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse(status=401)
        return super().__call__(request, *args, **kwargs)

    def items(self):
        """
        Get latest animals as items.
        """
        return Animal.objects.order_by('-entry_date')[:10]

    def item_title(self, item):
        """
        What to print as item title (use default __str__ of model).
        """
        return item

    def item_description(self, item):
        """
        What to print as item description (use default description from model).
        """
        return item.description()
