"""
Django Views contains all the functions for rendering objects (HTML display).
It also contains an RSS Feed generator class to create an RSS feed from newly created animals

**Important**:
    When adding new functions, use the login_required decorator
    When adding new classes, use the LoginRequiredMixin
"""
import operator
import logging
import sys
import time
from functools import reduce
from django.conf import settings
from datetime import datetime, timedelta
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
from django.views.decorators.cache import cache_page
#from django.urls import reverse
from django.views import generic

from .filters import AnimalFilter, OrganFilter, ChangeFilter, PersonFilter, FishFilter, MouseFilter, PupFilter
from .models import Animal, Organ, Change, FishPeople, Fish, Location, Person, Lab, FishPeople, FishTeam, FishMutation
from .models import Mouse, MouseMutation, PyratUser, PyratUserPermission, Pup 
from .models import SacrificeIncidentToken, WIncident_write, WIncident, WIncidentanimals_write, WIncidentpups_write, WIncidentcomment
from .importscript import runimport
from django.core.mail import EmailMultiAlternatives, send_mail
from django.utils.html import strip_tags

logger = logging.getLogger('mylogger')


class LatestAnimalsFeed(Feed):
    """
    RSS Feed for new animals/organs.
    """
    title = 'Anishare animal/organ feed'
    link = '/animals/feed'
    description = 'Updates on animals/organs to share.'

    def __call__(self, request, *args, **kwargs):
        #if not request.user.is_authenticated:
        #    return HttpResponse(status=401)
        return super().__call__(request, *args, **kwargs)

    def items(self):
        """
        Get latest animals as items.
        """
        from itertools import chain
        animals = Animal.objects.order_by('-pk')[:10]
        organs = Organ.objects.order_by('-pk')[:10]
        return chain(animals, organs)

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

#class AnimalIndexView(LoginRequiredMixin, generic.ListView):
#    """
#    Index / List view for all available animals.
#    Generic ListView using the LoginRequiredMixin
#
#    :param q: query / search term to filter the results
#    :param show: limit the results to 'current', 'archive', or all animals
#    """
#    model = Animal
#    template_name = 'animals/index.html'
#    context_object_name = 'all_animals'
#    paginate_by = 100
#    def get_queryset(self):
#        """Return the latest additions to the Animals table"""
#        result = super(AnimalIndexView, self).get_queryset()
#        query = self.request.GET.get('q')
#        if query:
#            query_list = query.split()
#            result = result.filter(
#                reduce(operator.and_, (Q(comment__icontains=q) for q in query_list)) |
#                reduce(operator.and_, (Q(mutations__icontains=q) for q in query_list)) |
#                reduce(operator.and_, (Q(database_id__icontains=q) for q in query_list)) |
#                reduce(operator.and_, (Q(line__icontains=q) for q in query_list)) |
#                reduce(operator.and_, (Q(lab_id__icontains=q) for q in query_list)) |
#                reduce(operator.and_, (Q(location__name__icontains=q) for q in query_list)) |
#                reduce(operator.and_, (Q(new_owner__icontains=q) for q in query_list)) |
#                reduce(operator.and_, (Q(responsible_person__name__icontains=q) for q in query_list)) |
#                reduce(operator.and_, (Q(licence_number__icontains=q) for q in query_list))
#            )
#            return result
#        try:
#            show = self.kwargs['show']
#        except KeyError:
#            show = 'current'
#        if show == 'archive':
#            return Animal.objects.filter(available_to__lte=datetime.now().date()).order_by('-entry_date')
#        elif show == 'current':
#            return Animal.objects.filter(available_to__gte=datetime.now().date()).order_by('-entry_date')
#        return Animal.objects.order_by('-entry_date')
#
#class OrganIndexView(LoginRequiredMixin, generic.ListView):
#    """
#    Index / List view for all available Organs.
#    Generic ListView using the LoginRequiredMixin
#
#    :param q: query / search term to filter the results
#    :param show: limit the results to 'current', 'archive', or all Organs
#    """
#    model = Organ
#    template_name = 'animals/organs.html'
#    context_object_name = 'all_organs'
#    paginate_by = 100
#    def get_queryset(self):
#        """Return the latest additions to the Organs table"""
#        result = super(OrganIndexView, self).get_queryset()
#        query = self.request.GET.get('q')
#        if query:
#            query_list = query.split()
#            result = result.filter(
#                reduce(operator.and_, (Q(comment__icontains=q) for q in query_list)) |
#                reduce(operator.and_, (Q(mutations__icontains=q) for q in query_list)) |
#                reduce(operator.and_, (Q(database_id__icontains=q) for q in query_list)) |
#                reduce(operator.and_, (Q(line__icontains=q) for q in query_list)) |
#                reduce(operator.and_, (Q(lab_id__icontains=q) for q in query_list)) |
#                reduce(operator.and_, (Q(location__name__icontains=q) for q in query_list)) |
#                reduce(operator.and_, (Q(killing_person__icontains=q) for q in query_list)) |
#                reduce(operator.and_, (Q(animal_type__icontains=q) for q in query_list)) |
#                reduce(operator.and_, (Q(method_of_killing__icontains=q) for q in query_list)) |
#                reduce(operator.and_, (Q(licence_number__icontains=q) for q in query_list))
#            )
#            return result
#        return Organ.objects.order_by('-entry_date')

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
    logger.info('{} The entry {} has been claimed by {}.'.format(datetime.now(),animal.pk, animal.new_owner))
    subject = "User {} claimed animal {} in AniShare".format(email, primary_key)
    message = render_to_string('email.html', {'email': email, 'object': animal, 'now': datetime.now()})
    if animal.responsible_person2 is None:
        send_mail(subject, message, email, [animal.responsible_person.email, email],html_message=message)
    else:
        send_mail(subject, message, email, [animal.responsible_person.email, animal.responsible_person2.email, email],html_message=message)
    #msg = EmailMultiAlternatives(subject, message, email, [animal.responsible_person.email, email],html_message=message)
    #msg.attach_alternative(message, "text/html")
    #msg.content_subtype = "html"
    #msg.mixed_subtype = 'related'
    #msg.send()
    if amount_difference > 0:  # If there were multiple animals, save the remainder of animals as a new object
        animal.pk = None
        animal.amount = amount_difference
        animal.new_owner = ''
        animal.save()
        messages.add_message(request, messages.SUCCESS, 'The amount of available animals in this entry has been reduced to {}.'.format(animal.amount))
    if animal.responsible_person2 is not None:
        messages.add_message(request, messages.SUCCESS, 'An Email has been sent to <{}> and <{}>.'.format(animal.responsible_person.email, animal.responsible_person2.email))
    else:
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
    primary_key = request.POST['pk']
    
    email = request.POST['email']
    primary_key = request.POST['pk']
    organs_wanted = request.POST['organs_wanted']

    organ= Organ.objects.get(pk=primary_key)
    if not organ.comment:
        organ.comment = request.POST['organs_wanted'] + " already claimed"
    elif organ.comment:
        organ.comment = organ.comment + "\n" + request.POST['organs_wanted'] + " already claimed"
        pass 
    organ.save() 

    organ = Organ.objects.get(pk=primary_key)
    subject = "AniShare User {} claimed organ(s) {}".format(email, organs_wanted)
    message = render_to_string('email.html', {'email': email, 'organs_wanted':organs_wanted, 'object': organ, 'now': datetime.now()})
    if organ.responsible_person2 is None:
        msg = EmailMessage(subject, message, email, [organ.responsible_person.email, email])
    else:
        msg = EmailMessage(subject, message, email, [organ.responsible_person.email,organ.responsible_person2.email, email])
    msg.content_subtype = "html"
    msg.send()
    if organ.responsible_person2 is None:
        messages.add_message(request, messages.SUCCESS, 'An Email has been sent to <{}>.'.format(organ.responsible_person.email))
    else:
        messages.add_message(request, messages.SUCCESS, 'An Email has been sent to <{}> and <{}>.'.format(organ.responsible_person.email,organ.responsible_person2.email))
    logger.info('{} AniShare User {} claimed organ(s) {} from entry {}'.format(datetime.now(), email, organs_wanted,primary_key))
    return HttpResponseRedirect('/organs/')



@login_required
#@cache_page(60*60)
def animal_list(request):
    #runimport()
    animallist = Animal.objects.filter(new_owner ='').filter(available_from__lte = datetime.now().date()).filter(available_to__gte = datetime.now().date()).order_by('available_to')
    #animallist = Animal.objects.filter(new_owner__exact='').filter(day_of_death >= datetime.now().date())
    #f = AnimalFilter(request.GET, queryset=Animal.objects.order_by('-entry_date'))
    #f = AnimalFilter(request.GET, queryset=Animal.objects.all().order_by('-entry_date'))

    f = AnimalFilter(request.GET, queryset=animallist)
    return render(request, 'animals/animal-index.html', {'filter': f})

@login_required
#@cache_page(60*60)
def organ_list(request):
    organlist = Organ.objects.filter(day_of_death__gte = datetime.now().date()).order_by('day_of_death')
    f = OrganFilter(request.GET, queryset=organlist)
    #f = OrganFilter(request.GET, queryset=Organ.objects.order_by('-entry_date'))
    return render(request, 'animals/organ-index.html', {'filter': f})
#today = datetime.now().date()
#        return self.day_of_death >= today

@login_required
#@cache_page(60*60)
def tickatlabpersonlist(request):
    personlist = FishPeople.objects.using('fishdb').all().order_by('lastname')
    f = PersonFilter(request.GET, queryset=personlist)
    return render(request, 'animals/fishpeople.html', {'filter': f})


@login_required
def pyratpuplist(request):
    pyratuser = PyratUser.objects.using('mousedb').get(username=request.user.username)
    if (pyratuser.locallevel == 11):
        #messages.add_message(request, messages.INFO,'You do not have the right to connect to the PyRAT Database')
        fullname = pyratuser.firstname + ' '  + pyratuser.lastname
        puplist = Pup.objects.using('mousedb').all().filter(responsible=fullname).order_by('eartag') 
        f = PupFilter(request.GET, queryset=puplist)
        return render(request, 'animals/pupfrompyrat.html', {'showgroups': True, 'filter': f})
    if (pyratuser.locallevel == 3 or pyratuser.locallevel == 4):
        try:
            owner = request.GET['owner']
            responsible1 = request.GET['responsible']
        except:
            owner=''
            responsible1=''
        if (owner =='' and responsible1==''):
            puplist = Pup.objects.using('mousedb').all().filter(owner_id__in=[]).order_by('eartag') 
            messages.add_message(request, messages.INFO,'Please search for an owner or a responsible person of the pup you like to share')
        else:
            puplist = Pup.objects.using('mousedb').all().order_by('eartag') 
        f = PupFilter(request.GET, queryset=puplist)
        return render(request, 'animals/pupfrompyrat.html', {'showgroups': True, 'filter': f})
    pupownerid = []
    pupelist = None
    i = 0
    if (pyratuser.usernum is not None and pyratuser.usernum != ''):
        pupownerid.insert(i,pyratuser.id)
    permission= PyratUserPermission.objects.using('mousedb').all().filter(userid=pyratuser.id)
    if (permission is not None and permission !=''):       
        for p in permission:
            pupownerid.insert(i,p.uid)
    puplist = Pup.objects.using('mousedb').all().filter(owner_id__in=pupownerid).order_by('eartag')    
    f = PupFilter(request.GET, queryset=puplist)
    return render(request, 'animals/pupfrompyrat.html', {'filter': f})


@login_required
def pyratmouselist(request):
    pyratuser = PyratUser.objects.using('mousedb').get(username=request.user.username)
    if (pyratuser.locallevel == 11):
        #messages.add_message(request, messages.INFO,'You do not have the right to connect to the PyRAT Database')
        fullname = pyratuser.firstname + ' '  + pyratuser.lastname
        mouselist = Mouse.objects.using('mousedb').all().filter(responsible=fullname).order_by('eartag') 
        f = MouseFilter(request.GET, queryset=mouselist)
        return render(request, 'animals/micefrompyrat.html', {'showgroups': True, 'filter': f,})
    if (pyratuser.locallevel == 3 or pyratuser.locallevel == 4):
        try:
            owner = request.GET['owner']
            responsible1 = request.GET['responsible']
        except:
            owner=''
            responsible1=''
        if (owner =='' and responsible1==''):
            mouselist = Mouse.objects.using('mousedb').all().filter(owner_id__in=[]).order_by('eartag') 
            messages.add_message(request, messages.INFO,'Please search for an owner or a responsible person of the mice you like to share')
        else:
            mouselist = Mouse.objects.using('mousedb').all().order_by('eartag') 
        f = MouseFilter(request.GET, queryset=mouselist)
        return render(request, 'animals/micefrompyrat.html', {'showgroups': True, 'filter': f,})
    mouseownerid = []
    mouselist = None
    i = 0
    if (pyratuser.usernum is not None and pyratuser.usernum != ''):
        mouseownerid.insert(i,pyratuser.id)
    permission= PyratUserPermission.objects.using('mousedb').all().filter(userid=pyratuser.id)
    if (permission is not None and permission !=''):       
        for p in permission:
            mouseownerid.insert(i,p.uid)
    mouselist = Mouse.objects.using('mousedb').all().filter(owner_id__in=mouseownerid).order_by('eartag') 
    mutationlist = MouseMutation.objects.using('mousedb').all()  
    # .filter(animalid__in = mouselist.id) 
    f = MouseFilter(request.GET, queryset=mouselist)
    return render(request, 'animals/micefrompyrat.html', {'filter': f, 'mutation': mutationlist})

@login_required
def pyratmouselistuser(request, username):
    pyratuser = PyratUser.objects.using('mousedb').get(username=username)
    if (pyratuser.locallevel == 3 or pyratuser.locallevel == 4):
        try:
            owner = request.GET['owner']
            responsible1 = request.GET['responsible']
        except:
            owner=''
            responsible1=''
        if (owner =='' and responsible1==''):
            mouselist = Mouse.objects.using('mousedb').all().filter(owner_id__in=[]).order_by('eartag') 
            messages.add_message(request, messages.INFO,'Please search for an owner or a responsible person of the mice you like to share')
        else:
            mouselist = Mouse.objects.using('mousedb').all().order_by('eartag') 
        f = MouseFilter(request.GET, queryset=mouselist)
        return render(request, 'animals/micefrompyrat.html', {'showgroups': True, 'filter': f})
    mouseownerid = []
    mouselist = None
    if (pyratuser.usernum is not None and pyratuser.usernum != ''):
        mouseownerid.insert(i,pyratuser.id)
    permission= PyratUserPermission.objects.using('mousedb').all().filter(userid=pyratuser.id)
    if (permission is not None and permission !=''):       
        i = 0
        for p in permission:
            mouseownerid.insert(i,p.uid)
    mouselist = Mouse.objects.using('mousedb').all().filter(owner_id__in=mouseownerid).order_by('eartag')    
    f = MouseFilter(request.GET, queryset=mouselist)
    return render(request, 'animals/micefrompyrat.html', {'filter': f})

@login_required
def importmice_view(request):
    if request.method == "POST":
        importlist = request.POST.getlist("selected",None)
        mouselist = Mouse.objects.using('mousedb').filter(id__in = importlist).order_by('id')
        f = MouseFilter(request.GET, queryset=mouselist)
        persons = Person.objects.all().order_by('name')
        return render(request, 'animals/import-mice.html', {'filter': f, 'persons':persons})

@login_required
def importpup_view(request):
    if request.method == "POST":
        importlist = request.POST.getlist("selected",None)
        puplist = Pup.objects.using('mousedb').filter(id__in = importlist).order_by('id')
        f = PupFilter(request.GET, queryset=puplist)
        persons = Person.objects.all().order_by('name')
        return render(request, 'animals/import-pup.html', {'filter': f, 'persons':persons})

@login_required
def importpuptoanishare(request):

    if request.method == "POST":
        pupidlist = request.POST.getlist("id",None)
        availablefromlist = request.POST.getlist("availablefrom",None)
        availabletolist = request.POST.getlist("availableto",None)
        responsible_person2 = request.POST.getlist("responsible_person2",None)
        puplist = Pup.objects.using('mousedb').filter(id__in = pupidlist)
        i=0
        for dataset in puplist:
            try:
                mouse_already_imported = Animal.objects.get(pup_id=dataset.id)
                messages.add_message(request, messages.ERROR,'The pup with the ID {} is already imported. A new import is not possible'.format(dataset.eartag))
                continue
            except Animal.DoesNotExist:
                i=i
            new_pup = Animal()
            new_pup.animal_type    = "pup"
            new_pup.pup_id       = dataset.id
            if dataset.eartag:
                new_pup.database_id    = dataset.eartag
            else:
                new_pup.database_id   = dataset.id
            new_pup.lab_id         = dataset.labid
            new_pup.amount         = 1
            new_pup.genetic_background  = dataset.genetic_bg
            new_pup.available_from = availablefromlist[i]
            new_pup.available_to   = availabletolist[i]
            if dataset.licence:
                new_pup.licence_number = dataset.licence
            else:
                new_pup.licence_number =''
            #new_pup.licence_number = dataset.licence
            new_pup.day_of_birth   = dataset.dob
            if responsible_person2[i]!="":
                new_pup.responsible_person2 = Person.objects.get(name=responsible_person2[i])
            mousemutations           = MouseMutation.objects.using('mousedb').filter(pupid = dataset.id)
            new_pup.mutations = ''
            for m in mousemutations:
                if m.grade_name:
                    new_pup.mutations  = new_pup.mutations + m.mutation_name + ' ' + m.grade_name + '; '
                else:
                    new_pup.mutations  = new_pup.mutations + m.mutation_name + ' ' + 'N.V.; '
            try:
                new_pup.location       = Location.objects.get(name=dataset.location)
            except:
                new_location = Location()
                new_location.name = dataset.location
                new_location.save()
                new_pup.location       = Location.objects.get(name=dataset.location)
            new_pup.line           = dataset.strain  
            try:        
                new_pup.responsible_person = Person.objects.get(name=dataset.responsible)
            except:
                new_person = Person()
                new_person.name = dataset.responsible
                new_person.email = dataset.responsible_email
                new_person.responsible_for_lab = Lab.objects.get(name="False")
                new_person.save()
                new_pup.responsible_person = Person.objects.get(name=dataset.responsible)
                ADMIN_EMAIL = getattr(settings, "ADMIN_EMAIL", None)
                send_mail("AniShare neue Person", 'Neue Person in AniShare {}'.format(new_person.name), ADMIN_EMAIL, [ADMIN_EMAIL])
            new_pup.added_by       = request.user
            if dataset.sex == '?':
                new_pup.sex = 'u'
            else:
                new_pup.sex = dataset.sex
            try:
                new_pup.save()
                if dataset.eartag:
                    messages.add_message(request, messages.SUCCESS,'The pup {} has been imported.'.format(dataset.eartag))
                else:
                    messages.add_message(request, messages.SUCCESS,'The pup {} has been imported.'.format(dataset.id))
            except BaseException as e:
                messages.add_message(request, messages.ERROR,'Becaus of an error the pup {} has NOT been imported. The AniShare admin is informed about the error'.format(dataset.eartag))
                ADMIN_EMAIL = getattr(settings, "ADMIN_EMAIL", None)
                send_mail("AniShare Importfehler", 'Fehler beim Pupimport von Pup {} mit Fehler {} in Zeile {}'.format(dataset.eartag, e,sys.exc_info()[2].tb_lineno ), request.user.email, [ADMIN_EMAIL])
            i = i + 1
    return HttpResponseRedirect('/admin/animals/animal/')

@login_required
def importmicetoanishare(request):
    try:
        if request.method == "POST":
            miceidlist = request.POST.getlist("id",None)
            availablefromlist = request.POST.getlist("availablefrom",None)
            availabletolist = request.POST.getlist("availableto",None)
            responsible_person2 = request.POST.getlist("responsible_person2",None)
            micelist = Mouse.objects.using('mousedb').filter(id__in = miceidlist)
            i=0
            for dataset in micelist:
                try:
                    mouse_already_imported = Animal.objects.get(mouse_id=dataset.id)
                    messages.add_message(request, messages.ERROR,'The mouse with the ID {} is already imported. A new import is not possible'.format(dataset.eartag))
                    continue
                except Animal.DoesNotExist:
                    i=i
                logger.debug('{}: Import Mouse with id {}'.format(datetime.now(), dataset.eartag))
                new_mouse = Animal()
                new_mouse.animal_type    = "mouse"
                new_mouse.mouse_id       = dataset.id
                new_mouse.database_id    = dataset.eartag
                new_mouse.lab_id         = dataset.labid
                new_mouse.amount         = 1
                new_mouse.genetic_background  = dataset.genetic_bg
                new_mouse.available_from = availablefromlist[i]
                new_mouse.available_to   = availabletolist[i]
                new_mouse.licence_number = dataset.licence
                new_mouse.day_of_birth   = dataset.dob
                if responsible_person2[i]!="":
                    new_mouse.responsible_person2 = Person.objects.get(name=responsible_person2[i])
                mousemutations           = MouseMutation.objects.using('mousedb').filter(animalid = dataset.id)
                new_mouse.mutations = ''
                all_grades_exist = 1
                for m in mousemutations:
                    if m.grade_name: 
                        new_mouse.mutations  = new_mouse.mutations + m.mutation_name + ' ' + m.grade_name + '; '
                    else:
                        all_grades_exist = 0
                        messages.add_message(request, messages.ERROR,'The mouse {} was not imported because of a missing grade.'.format(dataset.eartag))   
                if all_grades_exist == 0:
                    continue
                try:
                    new_mouse.location       = Location.objects.get(name=dataset.location)
                except:
                    logger.debug('{}:Neue Location {}'.format(datetime.now(), dataset.location))
                    new_location = Location()
                    new_location.name = dataset.location
                    new_location.save()
                    new_mouse.location       = Location.objects.get(name=dataset.location)
                new_mouse.line           = dataset.strain  
                try:        
                    new_mouse.responsible_person = Person.objects.get(name=dataset.responsible)
                except:
                    logger.debug('{}:Neue verwantwortliche Person {}'.format(datetime.now(), dataset.responsible))
                    new_person = Person()
                    new_person.name = dataset.responsible
                    new_person.email = dataset.responsible_email
                    new_person.responsible_for_lab = Lab.objects.get(name="False")
                    new_person.save()
                    new_mouse.responsible_person = Person.objects.get(name=dataset.responsible)
                    ADMIN_EMAIL = getattr(settings, "ADMIN_EMAIL", None)
                    send_mail("AniShare neue Person", 'Neue Person in AniShare {}'.format(new_person.name), ADMIN_EMAIL, [ADMIN_EMAIL])
                new_mouse.added_by       = request.user
                new_mouse.sex = dataset.sex
                try:
                    new_mouse.save()
                    messages.add_message(request, messages.SUCCESS,'The mouse {} has been imported.'.format(dataset.eartag))
                except BaseException as e: 
                    messages.add_message(request, messages.ERROR,'Becaus of an error the mouse {} has NOT been imported. The AniShare admin is informed about the error'.format(dataset.eartag))
                    send_mail("AniShare Importfehler", 'Fehler beim Mouseimport von Maus {} mit Fehler {} in Zeile {}'.format(dataset.eartag, e,sys.exc_info()[2].tb_lineno ), request.user.email, [ADMIN_EMAIL])
                i = i + 1
    except BaseException as e: 
        messages.add_message(request, messages.ERROR,'There was an error. The AniShare admin is informed about the error')
        ADMIN_EMAIL = getattr(settings, "ADMIN_EMAIL", None)
        send_mail("AniShare Importfehler", 'Fehler beim Mouseimport von Maus {} mit Fehler {} in Zeile {}'.format(dataset.eartag, e,sys.exc_info()[2].tb_lineno ), request.user.email, [ADMIN_EMAIL])
    return HttpResponseRedirect('/admin/animals/animal/')

@login_required
def tickatlabfishlist(request):
    
    try:
        fishuser = FishPeople.objects.using('fishdb').get(login=request.user.username)
        fishteams = FishTeam.objects.using('fishdb').all().filter(userid=fishuser.id)
        #logger.debug('{}:fishteams {}'.format(datetime.now(), fishteams))
        fishteamsid = []
        i=0
        fishteamsid.insert(i,fishuser.mainteamid)
        i=1
        for t in fishteams:
            fishteamsid.insert(i,t.teamid)
            #logger.debug('{}:fishteamsid {}'.format(datetime.now(), t.teamid))
            i=i+1
        #logger.debug('{}:fishteamsid {}'.format(datetime.now(), fishteamsid))
        fishlist = Fish.objects.using('fishdb').all().filter(teamid__in=fishteamsid).order_by('id')
        f = FishFilter(request.GET, queryset=fishlist)
        return render(request, 'animals/fishfromtickatlab.html', {'filter': f})
    except BaseException as e:                            
        logger.debug('{}:tickatlabfishlist except Fehler {} in Zeile {}'.format(datetime.now(),e,sys.exc_info()[2].tb_lineno))
        return render(request, 'animals/fishfromtickatlab.html')

@login_required
def importfish_view(request):
    if request.method == "POST":
        importlist = request.POST.getlist("selected",None)
        fishlist = Fish.objects.using('fishdb').filter(id__in = importlist).order_by('id')
        f = FishFilter(request.GET, queryset=fishlist)
        persons = Person.objects.all().order_by('name')
        return render(request, 'animals/import-fish.html', {'filter': f, 'persons':persons})

@login_required
def importfishtoanishare(request):
    if request.method == "POST":
        fishidlist = request.POST.getlist("id",None)
        availablefromlist = request.POST.getlist("availablefrom",None)
        availabletolist = request.POST.getlist("availableto",None)
        responsible_person2 = request.POST.getlist("responsible_person2",None)
        fishlist = Fish.objects.using('fishdb').filter(id__in = fishidlist)
        i=0
        for dataset in fishlist:
            try:
                fish_already_imported = Animal.objects.get(fish_id=dataset.id)
                messages.add_message(request, messages.ERROR,'The fish with the ID {} is already imported. A new import is not possible'.format(dataset.animalnumber))
                continue
            except Animal.DoesNotExist:
                i=i
            new_fish = Animal()
            new_fish.animal_type    = "fish"
            new_fish.fish_id        = dataset.id
            if (dataset.identifier1 != ""):
                new_fish.database_id = dataset.animalnumber+"//"+dataset.identifier1
            else:
                new_fish.database_id    = dataset.animalnumber
            new_fish.lab_id         = new_fish.database_id
            new_fish.amount         = dataset.quantity
            new_fish.available_from = availablefromlist[i]
            new_fish.available_to   = availabletolist[i]
            new_fish.licence_number = dataset.license
            new_fish.day_of_birth   = dataset.dob
            new_fish.comment        = dataset.tag
            if dataset.specie == 40291147:   # It is a Notobranchius
                new_fish.fish_specie = 'n'
            elif dataset.specie == 40291120:
                new_fish.fish_specie = 'z' # It is a Zebra fish
            if responsible_person2[i]!="":
                new_fish.responsible_person2 = Person.objects.get(name=responsible_person2[i])
            
            fishmutations           = FishMutation.objects.using('fishdb').filter(referenceid = dataset.id)
            new_fish.mutations = ''
            for m in fishmutations:
                new_fish.mutations  = new_fish.mutations + m.description + ' ' + m.genotype + '; '
            try:
                new_fish.location       = Location.objects.get(name=dataset.location)
            except:
                new_location = Location()
                new_location.name = dataset.location
                new_location.save()
                new_fish.location       = Location.objects.get(name=dataset.location)
            #new_fish.mutations      = dataset.strain
            new_fish.line           = dataset.strain  
            try:        
                new_fish.responsible_person = Person.objects.get(name=dataset.responsible)
            except:
                new_person = Person()
                new_person.name = dataset.responsible
                new_person.email = dataset.responsible_email
                new_person.responsible_for_lab = Lab.objects.get(name="False")
                new_person.save()
                new_fish.responsible_person = Person.objects.get(name=dataset.responsible)
                ADMIN_EMAIL = getattr(settings, "ADMIN_EMAIL", None)
                send_mail("AniShare neue Person", 'Neue Person in AniShare {}'.format(new_person.name), ADMIN_EMAIL, [ADMIN_EMAIL])
            new_fish.added_by       = request.user
            if (dataset.sex == 1):
                new_fish.sex = 'm'
            elif (dataset.sex == 2):
                new_fish.sex = 'f'
            elif (dataset.sex == 0):
                new_fish.sex = 'u'
            try:
                new_fish.save()
                messages.add_message(request, messages.SUCCESS,'The fish {} has been imported.'.format(dataset.animalnumber))
            except Exception:
                messages.add_message(request, messages.ERROR,'Becaus of an error the fish {} has NOT been imported. The AniShare admin is informed about the error'.format(dataset.animalnumber))
                send_mail("AniShare Importfehler", 'Fehler beim Fishimport von Fish  {} mit Fehler {} '.format(dataset.animalnumber, Exception), request.user.email, [ADMIN_EMAIL])
            i = i + 1
    return HttpResponseRedirect('/admin/animals/animal/')


@login_required
def ConfirmRequest(request, token):### Change Status from a sacrifice work request to the status open
    message = "URL is wrong. Please check your URL or get in contact with the administrator" 
    confirmed = 0
    user_confirmed = 0
    ADMIN_EMAIL = getattr(settings, "ADMIN_EMAIL", None)
    TIMEDIFF = getattr(settings, "TIMEDIFF", 2)
    LINES_PROHIBIT_SACRIFICE = getattr(settings, "LINES_PROHIBIT_SACRIFICE", None)
    try:
        sIncidentToken = SacrificeIncidentToken.objects.get(urltoken = token)
        try:
            #sIncidentToken = SacrificeIncidentToken.objects.get(urltoken = token)
            if sIncidentToken:
                for u in range(len(settings.USER_MAPPING)): # used if the username differs from anishare and pyrat
                    if request.user.username == settings.USER_MAPPING[u][0]:
                        if settings.USER_MAPPING[u][1] == sIncidentToken.initiator:
                            user_confirmed = 1 
                if ((request.user.username == sIncidentToken.initiator) or (user_confirmed == 1)):
                    if sIncidentToken.confirmed:
                        message = "Request is already created. A second time is not possible"
                    elif (sIncidentToken.created + timedelta(days=15) < datetime.now(sIncidentToken.created.tzinfo)): # Request expired
                        message = "The Link is expired because the AddToAniShare request has expired more than 14 days ago. You can create a sacrifice request directly inside PyRAT."
                    else:
                        MOUSEDB= getattr(settings, "MOUSEDB", None)
                        previous_incident = WIncident.objects.using(MOUSEDB).get(incidentid = sIncidentToken.incidentid) 
                        animallist = Animal.objects.filter(pyrat_incidentid = previous_incident.incidentid)
                        
                        # Check if a mouse is claimed
                        i = 0
                        for animal in animallist:
                            if animal.new_owner:
                                animallist=animallist.exclude(pk=animal.pk)
                            if animal.line in LINES_PROHIBIT_SACRIFICE:
                                animallist = animallist.exclude(pk=animal.pk)
                            i = i + 1
                        if len(animallist) == 0:
                            message = "All mice are claimed"
                            return render(request, 'animals/confirmrequest.html', {'message': message,'confirmed':confirmed})

                        # Check if all mice are still alive
                        i = 0
                        for animal in animallist:
                            if (animal.animal_type == 'mouse'):
                                try:
                                    if not Mouse.objects.using(MOUSEDB).filter(id = animal.mouse_id).exists():
                                        animallist=animallist.exclude(pk=animal.pk)
                                except BaseException as e:     
                                    send_mail("AniShare ConfirmRequest", 'Fehler {} in Zeile {}'.format(e,sys.exc_info()[2].tb_lineno), ADMIN_EMAIL, [ADMIN_EMAIL])
                                    animallist=animallist.exclude(pk=animal.pk)
                            if (animal.animal_type == 'pup'):
                                try:
                                    if not Pup.objects.using(MOUSEDB).filter(id = animal.pup_id).exists():
                                        send_mail("AniShare ConfirmRequest", 'Pup {} nicht vorhanden. Siehe AddToAniShare Auftrag {}'.format(animal.pup_id,previous_incident.incidentid), ADMIN_EMAIL, [ADMIN_EMAIL])
                                        # Pup könnte bereits zu einem erwachsenen Tier übergangen sein, Änderung muss kontrolliert werden
                                        if Mouse.objects.using(MOUSEDB).filter(id = animal.animalid).exists():
                                            v_mouse = Mouse.objects.using(mousedb).get(id = animal.animalid)
                                        else:
                                            animallist=animallist.exclude(pk=animal.pk)
                                            continue
                                        if Animal.objects.filter(database_id=v_mouse.eartag).exists():
                                            animal = Animal.objects.get(database_id=v_mouse.eartag)
                                            animal.mouse_id = v_mouse.id
                                            animal.save() # Save new animal_id (id changed because pup is now an adult)
                                        else:
                                            animallist=animallist.exclude(pk=animal.pk)
                                            continue 
                                        #animallist=animallist.exclude(pk=animal.pk)
                                except:
                                    animallist=animallist.exclude(pk=animal.pk)
                        if len(animallist) > 0:
                            confirmed = 1
                        else:
                            message = "There is no living mouse or pup to create a sacrifice request"
                            return render(request, 'animals/confirmrequest.html', {'message': message,'confirmed':confirmed})

                        new_sacrifice_incident                  = WIncident_write()
                        new_sacrifice_incident.incidentclass    = 1                         # Sacrifices
                        new_sacrifice_incident.initiator        = previous_incident.initiator.id  # Person who create the Add to AniShare request
                        new_sacrifice_incident.owner            = previous_incident.owner.id      # copied from the Add to AniShare request
                        new_sacrifice_incident.responsible      = previous_incident.responsible.id # copied from the Add to AniShare request
                        new_sacrifice_incident.sacrifice_reason = previous_incident.sacrifice_reason # copied from the Add to AniShare request
                        new_sacrifice_incident.sacrifice_method = previous_incident.sacrifice_method # copied from the Add to AniShare request
                        new_sacrifice_incident.behavior         = 4 # Sacrifice
                        new_sacrifice_incident.priority         = 3 # medium
                        new_sacrifice_incident.status           = 2 # open
                        new_sacrifice_incident.duedate          = datetime.now() + timedelta(hours=TIMEDIFF) + timedelta(days=3)
                        new_sacrifice_incident.approved         = 1
                        MOUSEDB_WRITE = getattr(settings, "MOUSEDB_WRITE", None)
                        new_sacrifice_incident.save(using=MOUSEDB_WRITE)
                        time.sleep(1)

                        new_sacrifice_incident_tmp = WIncident.objects.using(MOUSEDB).get(incidentid=new_sacrifice_incident.incidentid) 
                        new_comment = WIncidentcomment()
                        new_comment.incidentid = new_sacrifice_incident_tmp
                        new_comment.comment = 'AniShare: Request created. Previous AddToAniShare request is: {}'.format(previous_incident.incidentid)
                        new_comment.save(using=MOUSEDB_WRITE) 
                        new_comment.commentdate = new_comment.commentdate + timedelta(hours=TIMEDIFF)
                        new_comment.save(using=MOUSEDB_WRITE)

                        new_comment = WIncidentcomment()
                        new_comment.incidentid = previous_incident
                        new_comment.comment = 'AniShare: Sacrifice request with id {} created'.format(new_sacrifice_incident.incidentid)
                        new_comment.save(using=MOUSEDB_WRITE) 
                        new_comment.commentdate = new_comment.commentdate + timedelta(hours=TIMEDIFF)
                        new_comment.save(using=MOUSEDB_WRITE)

                        for animal in animallist:
                            if (animal.animal_type == 'mouse'):
                                try:
                                    incident_mouse = WIncidentanimals_write()
                                    incident_mouse.incidentid = new_sacrifice_incident
                                    incident_mouse.animalid = animal.mouse_id
                                    incident_mouse.save(using=MOUSEDB_WRITE)
                                except BaseException as e:
                                    send_mail("AniShare ConfirmRequest", 'Fehler {} in Zeile {}'.format(e,sys.exc_info()[2].tb_lineno), ADMIN_EMAIL, [ADMIN_EMAIL])
                            if (animal.animal_type == 'pup'):
                                try:
                                    incident_pup = WIncidentpups_write()
                                    incident_pup.incidentid = new_sacrifice_incident
                                    incident_pup.pupid = animal.pup_id
                                    incident_pup.save(using=MOUSEDB_WRITE)
                                except BaseException as e:
                                    send_mail("AniShare ConfirmRequest", 'Fehler {} in Zeile {}'.format(e,sys.exc_info()[2].tb_lineno), ADMIN_EMAIL, [ADMIN_EMAIL])
                        sIncidentToken.confirmed = datetime.now()
                        sIncidentToken.save()   
                        message ="Sacrifice request created with id: {}".format(new_sacrifice_incident.incidentid)
                        confirmed = 1
                else:
                    message ="Sorry, you can not create this request because you are not the initiator of the previous AddToAniShare request."
            else:
                #not possible
                message =""
        except BaseException as e: 
            send_mail("AniShare ConfirmRequest", 'Fehler {} in Zeile {}'.format(e,sys.exc_info()[2].tb_lineno), ADMIN_EMAIL, [ADMIN_EMAIL])
            return render(request, 'animals/confirmrequest.html', {'message': message,'confirmed':confirmed})
    except BaseException as e: 
        # Wrong URL or token exists multiple times
        return render(request, 'animals/confirmrequest.html', {'message': message,'confirmed':confirmed})
    return render(request, 'animals/confirmrequest.html', {'message': message,'confirmed':confirmed})

@login_required
def change_history(request):
    changelist = Change.objects.all()
    f = ChangeFilter(request.GET, queryset=changelist)
    return render(request, 'animals/change-index.html', {'filter': f})

@login_required
def macros(request):
    return render(request, 'animals/macro-index.html')

class LatestChangesFeed(Feed):
    """
    RSS Feed for system changes on AniShare.
    """
    title = 'AniShare version feed'
    link = '/versionhistory/feed'
    description = 'Updates on AniShare.'

    def __call__(self, request, *args, **kwargs):
       # if not request.user.is_authenticated:
        #    return HttpResponse(status=401)
        return super().__call__(request, *args, **kwargs)

    def items(self):
        """
        Get latest changes as items.
        """
        changes = Change.objects.order_by('-pk')[:10]
        return changes

    def item_title(self, item):
        """
        What to print as item title (use default __str__ of model).
        """
        return "{}: {} [{}]".format(
            item.version, item.short_text, item.entry_date) 

    def item_description(self, item):
        """
        What to print as item description (use default description from model).
        """
        return item.description

def AnimalClaimView(request):
    if request.method == "POST":
        claimlist = request.POST.getlist("selected",None)
        animallist = Animal.objects.filter(pk__in = claimlist)
        f = AnimalFilter(request.GET, queryset=animallist)
        return render(request, 'animals/animals-claim.html', {'filter': f})


def send_email_animals(request):  # send a mail to the responsible persons of the claimed animals and go back to the overview site
    if request.method == "POST":
        email = request.POST['email']
        claimlist = request.POST.getlist("selectedAnimals",None)
        animallist = Animal.objects.filter(pk__in = claimlist)
        last_responsible = ""
        last_responsible2 = None
        error = 0;

        for sAnimal in animallist: 
            # the loop collects in an improvable way all animals from one responsible person and send it to the person.
            # Then the loop collects all animals from the next responsible person 
            if last_responsible != sAnimal.responsible_person or last_responsible2 != sAnimal.responsible_person2:
                last_responsible = sAnimal.responsible_person
                last_responsible2 = sAnimal.responsible_person2
                templist = Animal.objects.filter(pk__in = claimlist).filter(responsible_person = last_responsible).filter(responsible_person2 = last_responsible2)
                for tempAnimal in templist:
                    if tempAnimal.amount > 1:
                        messages.add_message(request, messages.SUCCESS,'It is not possible to claim animal groups (#>1) with other entries. Please claim the fish group individually')
                        error = 1;
                        break
                if error == 1:
                    break
                subject = "User {} claimed animals in AniShare".format(email)
                if last_responsible2 is None: # render the mail without second responsible person
                    message = render_to_string('email_animals.html',{'email':email, 'animals':templist, 'now': datetime.now(),'responsible_person':sAnimal.responsible_person.name, 'responsible_person2':None})
                else: # render the mail with the second responsible person
                    message = render_to_string('email_animals.html',{'email':email, 'animals':templist, 'now': datetime.now(),'responsible_person':sAnimal.responsible_person.name, 'responsible_person2':sAnimal.responsible_person2.name})
                if last_responsible2 is None: # send mail only to the first responsible person
                    msg = EmailMessage(subject, message, email, [sAnimal.responsible_person.email, email])
                else: # send mail to the first and second responsible person
                    msg = EmailMessage(subject, message, email, [sAnimal.responsible_person.email, sAnimal.responsible_person2.email, email])
                msg.content_subtype = "html"
                msg.send()
                if last_responsible2 is None:
                    messages.add_message(request, messages.SUCCESS, 'An Email has been sent to <{}>.'.format(sAnimal.responsible_person.email))
                else:
                    messages.add_message(request, messages.SUCCESS, 'An Email has been sent to <{}> and <{}>.'.format(sAnimal.responsible_person.email, sAnimal.responsible_person2.email))
                sAnimal.new_owner = email # save the new owner = mail address of the claiming user
                sAnimal.save()
                messages.add_message(request, messages.SUCCESS,'The entry {} has been claimed by {}.'.format(sAnimal.pk, sAnimal.new_owner))
                logger.info('{} The entry {} has been claimed by {}.'.format(datetime.now(), sAnimal.pk, sAnimal.new_owner))
            else:
                sAnimal.new_owner = email
                sAnimal.save()
                messages.add_message(request, messages.SUCCESS,'The entry {} has been claimed by {}.'.format(sAnimal.pk, sAnimal.new_owner))
                logger.info('{} The entry {} has been claimed by {}.'.format(datetime.now(), sAnimal.pk, sAnimal.new_owner))
    return HttpResponseRedirect('/animals')
