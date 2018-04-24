from django.views import generic
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseNotFound
from django.core.mail import send_mail
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
