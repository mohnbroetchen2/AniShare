from datetime import datetime
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.syndication.views import Feed
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import generic

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
        try:
            show = self.kwargs['show']
        except KeyError:
            show = 'current'
        if show == 'archive':
            return Animal.objects.filter(available_to__lte=datetime.now().date()).order_by('-entry_date')
        elif show == 'current':
            return Animal.objects.filter(available_to__gte=datetime.now().date()).order_by('-entry_date')
        else:
            return Animal.objects.order_by('-entry_date')


def send_email(request):
    email = request.POST['email']
    pk = request.POST['pk']
    animal = Animal.objects.get(pk=pk)
    animal.new_owner = email
    animal.save()
    subject = "User {} claimed animal {} in AniShare".format(email, pk)
    message = render_to_string('email.html', {'email': email, 'animal': animal, 'now': datetime.now()})

    msg = EmailMessage(subject, message, email, [animal.responsible_person.email, email])
    msg.content_subtype = "html"
    msg.send()
    messages.add_message(request, messages.SUCCESS, 'An Email has been sent to <{}>.'.format(animal.responsible_person.email))
#    send_mail( subject, message, email, [animal.responsible_person.email, email], fail_silently=False, html_message=message)

    return HttpResponseRedirect('/')


class LatestAnimalsFeed(Feed):
    title = 'Anishare animal feed'
    link = '/animals/feed'
    description = 'Updates on animals to share.'

    def items(self):
        return Animal.objects.order_by('-entry_date')[:10]

    def item_title(self, item):
        return item

    def item_description(self, item):
        return item.description()
