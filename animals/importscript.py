def runimport():
        from django.core import management
        from .models import WIncident, WIncidentAnimals, Animal, Mouse, MouseMutation, Location, Person, Lab, WIncidentcomment
        from django.contrib.auth.models import User
        from django.core.mail import EmailMultiAlternatives, send_mail
        from datetime import datetime, timedelta
        from django.conf import settings
        
        today = datetime.now().date()
        incidentlist = WIncident.objects.using('mousedb_test').all().filter(status=5)
        for incident in incidentlist:
            skip = 0
            error = 0
            i = 0
            animallist = WIncidentAnimals.objects.using('mousedb_test').filter(incidentid = incident.incidentid)
            count_animals = animallist.count()
            for pyratmouse in animallist:
                i = i + 1
                try:
                    animouse = Animal.objects.get(mouse_id=pyratmouse.animalid)
                    if (animouse.available_to >= today):
                        skip = 1
                        break
                except Exception: 
                        error = 1
                        skip = 1
                        ADMIN_EMAIL = getattr(settings, "ADMIN_EMAIL", None)
                        send_mail("AniShare Check Status Error", 'Fehler {} bei der Statusüberprüfung des Auftrags {}'.format( Exception, incident.incidentid), ADMIN_EMAIL, [ADMIN_EMAIL])
                if (skip == 0 and i == count_animals):
                    incident.status = 1
                    incident.save()
                    new_comment = WIncidentcomment()
                    new_comment.incidentid = incident
                    new_comment.comment = 'AniShare: Request status changed to closed'
                    new_comment.save() 

        """incidentlist = WIncident.objects.using('mousedb_test').all().filter(status=2)
        for incident in incidentlist:
            error = 0
            animallist = WIncidentAnimals.objects.using('mousedb_test').filter(incidentid = incident.incidentid)
            for pyratmouse in animallist:
                try:
                    if Animal.objects.filter(mouse_id=pyratmouse.animalid).exists():
                        continue
                    new_mouse = Animal()
                    new_mouse.animal_type    = "mouse"
                    dataset = Mouse.objects.using('mousedb_test').get(id=pyratmouse.animalid)
                    new_mouse.mouse_id       = dataset.id
                    new_mouse.database_id    = dataset.eartag
                    new_mouse.lab_id         = dataset.labid
                    new_mouse.amount         = 1
                    new_mouse.genetic_background  = dataset.genetic_bg
                    new_mouse.available_from = datetime.today().date()
                    new_mouse.available_to   = datetime.today().date() + timedelta(days=14)
                    new_mouse.licence_number = dataset.licence
                    new_mouse.day_of_birth   = dataset.dob
                    mousemutations           = MouseMutation.objects.using('mousedb_test').filter(animalid = dataset.id)
                    new_mouse.mutations = ''
                    for m in mousemutations:
                        new_mouse.mutations  = new_mouse.mutations + m.mutation_name + ' ' + m.grade_name + '; '
                    try:
                        new_mouse.location       = Location.objects.get(name=dataset.location)
                    except:
                        new_location = Location()
                        new_location.name = dataset.location
                        new_location.save()
                        new_mouse.location       = Location.objects.get(name=dataset.location)
                    new_mouse.line           = dataset.strain  
                    try:        
                        new_mouse.responsible_person = Person.objects.get(name=dataset.responsible)
                    except:
                        new_person = Person()
                        new_person.name = dataset.responsible
                        new_person.email = dataset.responsible_email
                        new_person.responsible_for_lab = Lab.objects.get(name="False")
                        new_person.save()
                        new_mouse.responsible_person = Person.objects.get(name=dataset.responsible)
                        ADMIN_EMAIL = getattr(settings, "ADMIN_EMAIL", None)
                        send_mail("AniShare neue Person", 'Neue Person in AniShare {}'.format(new_person.name), ADMIN_EMAIL, [ADMIN_EMAIL])
                    new_mouse.added_by       = User.objects.get(username='fmonheim')
                    new_mouse.sex = dataset.sex
                    try:
                        new_mouse.save()
                    except Exception: 
                        error = 1
                        send_mail("AniShare Importscriptfehler", 'Fehler beim Mouseimport von Maus {} mit Fehler {} '.format(dataset.eartag, Exception), ADMIN_EMAIL, [ADMIN_EMAIL])
                except Exception: 
                    error = 1
                    send_mail("AniShare Importscriptfehler", 'Fehler beim Mouseimport von Maus {} mit Fehler {} '.format(dataset.eartag, Exception), ADMIN_EMAIL, [ADMIN_EMAIL])   
            if error == 0:
                incident.status = 1
                incident.save()
        management.call_command("clearsessions")"""
        