from django.views import generic

from .models import Animal

class AnimalDetailView(generic.ListView):
    model = Animal
    template_name = 'animals/animal-detail.html'
#    def get_context_data(self, **kwargs):
#        context = super(AnimalDetailView, self).get_context_data(**kwargs)
#        return context

class AnimalIndexView(generic.ListView):
    model = Animal
    template_name = 'animals/index.html'
    context_object_name = 'all_animals'
    paginate_by = 100
    def get_queryset(self):
        """Return the latest additions to the Animals table"""
        return Animal.objects.order_by('-entry_date')#[:100]
