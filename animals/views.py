from django.views import generic
#from django.core.urlresolvers import reverse_lazy

from .models import Animal

class AnimalDetailView(generic.ListView):
    model = Animal
    template_name = 'animals/animal-detail.html'
#    def get_context_data(self, **kwargs):
#        context = super(AnimalDetailView, self).get_context_data(**kwargs)
#        return context

class AnimalCreateView(generic.CreateView):
    model = Animal
    fields = ( 'amount', 'available_from', 'available_to', 'day_of_birth', 'entry_date', 'external_id', 'external_lab_id', 'line', 'location', 'mutations', 'new_owner', 'responsible_person', 'sex',)

class AnimalDeleteView(generic.DeleteView):
    model = Animal
#    success_url = reverse_lazy('animals-list')

class AnimalUpdateView(generic.UpdateView):
    model = Animal
    fields = ( 'amount', 'available_from', 'available_to', 'day_of_birth', 'entry_date', 'external_id', 'external_lab_id', 'line', 'location', 'mutations', 'new_owner', 'responsible_person', 'sex',)

class AnimalIndexView(generic.ListView):
    model = Animal
    template_name = 'animals/index.html'
    context_object_name = 'all_animals'
    paginate_by = 100
    def get_queryset(self):
        """Return the latest additions to the Animals table"""
        return Animal.objects.order_by('-entry_date')#[:100]
