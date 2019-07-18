from django_extensions.management.jobs import DailyJob


class Job(DailyJob):
    help = ""

    def execute(self):
        from django.core import management
        from ...models import WIncident, WIncident_write, WIncidentAnimals, Animal, Mouse, Pup, MouseMutation, Location, Person, Lab, WIncidentcomment, WIncidentPups
        from django.contrib.auth.models import User
        from django.core.mail import EmailMultiAlternatives, send_mail
        from datetime import datetime, timedelta
        from django.conf import settings
        import logging
        import sys

        mousedb = 'mousedb_test'
        mousedb_write = 'mousedb_test_write'
        logger = logging.getLogger('myscriptlogger')

        try:
            incidentlist = WIncident.objects.using(mousedb).all().filter(status=2)
            for incident in incidentlist:
                error = 0
                # Import mice #
                animallist = WIncidentAnimals.objects.using(mousedb).filter(incidentid = incident.incidentid)
                for pyratmouse in animallist:
                    try:
                        if Animal.objects.filter(mouse_id=pyratmouse.animalid).exists():
                            # Benachrichtigung, dass Maus bereits angeboten wird?
                            continue
                        new_mouse = Animal()
                        new_mouse.animal_type    = "mouse"
                        dataset = Mouse.objects.using(mousedb).get(id=pyratmouse.animalid)
                        try:
                            new_mouse.mouse_id       = dataset.id
                        except: # mouse has no licence
                            initiator_mail = ""
                            initiator_mail = incident.initiator.email
                            if len(initiator_mail) > 0:
                                send_mail("AniShare: Mouse without license", 'You created a work request with the ID {} to add a mouse to AniShare. It is not possible to import a mouse without a license. '.format(new_person.name), ADMIN_EMAIL, [ADMIN_EMAIL])
                            break
                        new_mouse.database_id    = dataset.eartag
                        new_mouse.lab_id         = dataset.labid
                        new_mouse.amount         = 1
                        new_mouse.genetic_background  = dataset.genetic_bg
                        new_mouse.available_from = datetime.today().date()
                        new_mouse.available_to   = datetime.today().date() + timedelta(days=14)
                        new_mouse.licence_number = dataset.licence
                        new_mouse.day_of_birth   = dataset.dob
                        mousemutations           = MouseMutation.objects.using(mousedb).filter(animalid = dataset.id)
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
                            logger.debug('{}: Mouse with id {} has been imported by Script.'.format(datetime.now(), new_mouse.database_id))
                        except BaseException as e: 
                            error = 1
                            ADMIN_EMAIL = getattr(settings, "ADMIN_EMAIL", None)
                            send_mail("AniShare Importscriptfehler", 'Fehler beim Mouseimport von Maus {} mit Fehler {} in Zeile {}'.format(dataset.eartag, e,sys.exc_info()[2].tb_lineno ), ADMIN_EMAIL, [ADMIN_EMAIL])
                            #send_mail("AniShare Importscriptfehler", 'Fehler beim Mouseimport von Maus {} mit Fehler {} '.format(dataset.eartag, Exception), ADMIN_EMAIL, [ADMIN_EMAIL])
                    except BaseException as e: 
                        error = 1
                        ADMIN_EMAIL = getattr(settings, "ADMIN_EMAIL", None)
                        send_mail("AniShare Importscriptfehler", 'Fehler beim Mouseimport von Maus {} mit Fehler {} in Zeile {}'.format(dataset.eartag, e,sys.exc_info()[2].tb_lineno ), ADMIN_EMAIL, [ADMIN_EMAIL])
                        #send_mail("AniShare Importscriptfehler", 'Fehler beim Mouseimport von Maus {} mit Fehler {} '.format(dataset.eartag, Exception), ADMIN_EMAIL, [ADMIN_EMAIL])   
                
                # Import pups #
                puplist = WIncidentPups.objects.using(mousedb).filter(incidentid = incident.incidentid)
                for pyratpup in puplist:
                    try:
                        if Animal.objects.filter(pup_id=pyratpup.pupid).exists():
                            # Benachrichtigung, dass Maus bereits angeboten wird?
                            continue
                        new_pup = Animal()
                        new_pup.animal_type    = "pup"
                        dataset = Pup.objects.using(mousedb).get(id=pyratpup.pupid)
                        new_pup.pup_id       = dataset.id
                        new_pup.database_id    = dataset.eartag
                        new_pup.lab_id         = dataset.labid
                        new_pup.amount         = 1
                        new_pup.genetic_background  = dataset.genetic_bg
                        new_pup.available_from = datetime.today().date()
                        new_pup.available_to   = datetime.today().date() + timedelta(days=7)
                        new_pup.licence_number = dataset.licence
                        new_pup.day_of_birth   = dataset.dob
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
                        new_pup.added_by       = User.objects.get(username='fmonheim')
                        new_pup.sex = dataset.sex
                        try:
                            new_pup.save()
                            logger.debug('{}: Pup with id {} has been imported by Script.'.format(datetime.now(), new_pup.database_id))
                        except BaseException as e:  
                            error = 1
                            ADMIN_EMAIL = getattr(settings, "ADMIN_EMAIL", None)
                            send_mail("AniShare Importscriptfehler", '{}: Fehler beim Pupimport von Pup {} mit Fehler {} in Zeile {}'.format(mousedb, dataset.eartag, e,sys.exc_info()[2].tb_lineno ), ADMIN_EMAIL, [ADMIN_EMAIL])
                            #send_mail("AniShare Importscriptfehler", '{}: Fehler beim Pupimport von Pup {} mit Fehler {} '.format(mousedb, dataset.eartag, Exception), ADMIN_EMAIL, [ADMIN_EMAIL])
                    except BaseException as e:  
                        error = 1
                        ADMIN_EMAIL = getattr(settings, "ADMIN_EMAIL", None)
                        send_mail("AniShare Importscriptfehler", '{}: Fehler beim Pupimport von Pup {} mit Fehler {} in Zeile {}'.format(mousedb, dataset.eartag, e,sys.exc_info()[2].tb_lineno ), ADMIN_EMAIL, [ADMIN_EMAIL])
                        #send_mail("AniShare Importscriptfehler", '{}: Fehler beim Pupimport von Pup {} mit Fehler {} '.format(mousedb, dataset.eartag, Exception), ADMIN_EMAIL, [ADMIN_EMAIL])   
                            
                if error == 0:
                    incident_write = WIncident_write.objects.using(mousedb_write).get(incidentid=incident.incidentid)
                    incident_write.status = 5
                    incident_write.save(using=mousedb_write)
                    logger.debug('{}: Incident status {} has been changed to 5.'.format(datetime.now(), incident.incidentid))
                    new_comment = WIncidentcomment()
                    new_comment.incidentid = incident
                    new_comment.comment = 'AniShare: Request status changed to Added to Anishare'
                    new_comment.save(using=mousedb_write)
        except BaseException as e: 
            management.call_command("clearsessions")
            ADMIN_EMAIL = getattr(settings, "ADMIN_EMAIL", None)
            send_mail("AniShare Importscriptfehler hourly_insert_from_pyrat.py", '{}: Fehler {} in Zeile {}'.format(mousedb, e,sys.exc_info()[2].tb_lineno), ADMIN_EMAIL, [ADMIN_EMAIL])
        management.call_command("clearsessions")