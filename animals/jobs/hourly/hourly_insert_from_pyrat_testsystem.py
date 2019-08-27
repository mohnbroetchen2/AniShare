from django_extensions.management.jobs import HourlyJob


class Job(HourlyJob):
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
        ADMIN_EMAIL = getattr(settings, "ADMIN_EMAIL", None)
        TIMEDIFF = getattr(settings, "TIMEDIFF", 2)

        try:
            incidentlist = WIncident.objects.using(mousedb).all().filter(incidentclass=22).filter(status=2)
            for incident in incidentlist:
                if incident.duedate.date() != datetime.today().date():
                    logger.debug('incident.duedate {}: datetime.today().date(){} '.format(incident.duedate.date(), datetime.today().date()))
                    continue
                error = 0
                count_animals_deferred = 0
                count_animals_imported = 0
                initiator_mail = ""
                initiator_mail = incident.initiator.email
                # Import mice #
                animallist = WIncidentAnimals.objects.using(mousedb).filter(incidentid = incident.incidentid)
                for pyratmouse in animallist:
                    try:
                        if Animal.objects.filter(mouse_id=pyratmouse.animalid).exists():
                            datasetMouse = Mouse.objects.using(mousedb).get(id=pyratmouse.animalid)
                            send_mail("AniShare: Mouse already offered", 'You created a work request with the ID {} to add the mouse {} to AniShare. The mouse has already been offered. A second time is not possible'.format(incident.incidentid, datasetMouse.eartag), ADMIN_EMAIL, [initiator_mail,ADMIN_EMAIL])
                            count_animals_deferred = count_animals_deferred + 1
                            new_comment = WIncidentcomment()
                            new_comment.incidentid = incident
                            new_comment.comment = 'AniShare: Mouse {} already offered'.format(datasetMouse.eartag)
                            new_comment.save(using=mousedb_write)
                            new_comment.commentdate = new_comment.commentdate + timedelta(hours=TIMEDIFF)
                            new_comment.save(using=mousedb_write)
                            continue
                        new_mouse = Animal()
                        new_mouse.animal_type    = "mouse"
                        dataset = Mouse.objects.using(mousedb).get(id=pyratmouse.animalid)
                        try:
                            new_mouse.mouse_id       = dataset.id
                        except: # mouse has no licence
                            count_animals_deferred = count_animals_deferred + 1
                            new_comment = WIncidentcomment()
                            new_comment.incidentid = incident
                            new_comment.comment = 'AniShare: Mouse {} without licence can not be imported'.format(pyratmouse.eartag)
                            new_comment.save(using=mousedb_write)
                            new_comment.commentdate = new_comment.commentdate + timedelta(hours=TIMEDIFF)
                            new_comment.save(using=mousedb_write)
                            send_mail("AniShare: Mouse without license", 'You created a work request with the ID {} to add the mouse {} to AniShare. It is not possible to import a mouse without a license. '.format(incident.id, pyratmouse.eartag), ADMIN_EMAIL, [initiator_mail,ADMIN_EMAIL])
                            continue
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
                            if m.grade_name:   
                                new_mouse.mutations  = new_mouse.mutations + m.mutation_name + ' ' + m.grade_name + '; '
                            else:
                                new_mouse.mutations  = new_mouse.mutations + m.mutation_name +'; '
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
                        if dataset.sex == '?':
                            new_mouse.sex = 'u'
                        else:
                            new_mouse.sex = dataset.sex
                        try:
                            new_mouse.save()
                            count_animals_imported = count_animals_imported + 1
                            logger.debug('{}: Mouse with id {} has been imported by Script.'.format(datetime.now(), new_mouse.database_id))
                        except BaseException as e: 
                            error = 1
                            ADMIN_EMAIL = getattr(settings, "ADMIN_EMAIL", None)
                            send_mail("AniShare Importscriptfehler", 'Fehler beim Mouseimport von Maus {} mit Fehler {} in Zeile {}'.format(dataset.eartag, e,sys.exc_info()[2].tb_lineno ), ADMIN_EMAIL, [ADMIN_EMAIL])
                            #send_mail("AniShare Importscriptfehler", 'Fehler beim Mouseimport von Maus {} mit Fehler {} '.format(dataset.eartag, Exception), ADMIN_EMAIL, [ADMIN_EMAIL])
                    except BaseException as e: 
                        error = 1
                        ADMIN_EMAIL = getattr(settings, "ADMIN_EMAIL", None)
                        send_mail("AniShare Importscriptfehler", 'Fehler beim Mouseimport von Maus {} mit Fehler {} in Zeile {}'.format(pyratmouse.animalid, e,sys.exc_info()[2].tb_lineno ), ADMIN_EMAIL, [ADMIN_EMAIL])
                        #send_mail("AniShare Importscriptfehler", 'Fehler beim Mouseimport von Maus {} mit Fehler {} '.format(dataset.eartag, Exception), ADMIN_EMAIL, [ADMIN_EMAIL])   
                
                # Import pups #
                puplist = WIncidentPups.objects.using(mousedb).filter(incidentid = incident.incidentid)
                for pyratpup in puplist:
                    try:
                        dataset = Pup.objects.using(mousedb).get(id=pyratpup.pupid)
                        if Animal.objects.filter(pup_id=pyratpup.pupid).exists():
                            new_comment = WIncidentcomment()
                            new_comment.incidentid = incident
                            if dataset.eartag:
                                new_comment.comment = 'AniShare: Pup {} already offered'.format(dataset.eartag)
                                send_mail("AniShare: Pup already offered", 'You created a work request with the ID {} to add the pup {} to AniShare. The pup has already been offered. A second time is not possible'.format(incident.id, dataset.eartag), ADMIN_EMAIL, [initiator_mail,ADMIN_EMAIL])
                            else:
                                new_comment.comment = 'AniShare: Pup {} already offered'.format(pyratpup.pupid)
                                send_mail("AniShare: Pup already offered", 'You created a work request with the ID {} to add the pup {} to AniShare. The pup has already been offered. A second time is not possible'.format(incident.id, dataset.id), ADMIN_EMAIL, [initiator_mail,ADMIN_EMAIL])
                            new_comment.save(using=mousedb_write)
                            new_comment.commentdate = new_comment.commentdate + timedelta(hours=TIMEDIFF)
                            new_comment.save(using=mousedb_write) 
                            count_animals_deferred = count_animals_deferred + 1
                            # Benachrichtigung, dass Maus bereits angeboten wird?
                            continue
                        new_pup = Animal()
                        new_pup.animal_type    = "pup"
                        if dataset.licence == None:
                            new_comment = WIncidentcomment()
                            new_comment.incidentid = incident
                            if dataset.eartag:
                                new_comment.comment = 'Pup {} without licence can not be imported'.format(dataset.eartag)
                                send_mail("AniShare: Pup without license", 'You created a work request with the ID {} to add the pup {} to AniShare. It is not possible to import a pup without a license. '.format(incident.id, dataset.eartag), ADMIN_EMAIL, [initiator_mail,ADMIN_EMAIL])
                            else:
                                new_comment.comment = 'Pup {} without licence can not be imported'.format(pyratpup.pupid)
                                send_mail("AniShare: Pup without license", 'You created a work request with the ID {} to add the pup {} to AniShare. It is not possible to import a pup without a license. '.format(incident.id, dataset.id), ADMIN_EMAIL, [initiator_mail,ADMIN_EMAIL])
                            new_comment.save(using=mousedb_write)
                            new_comment.commentdate = new_comment.commentdate + timedelta(hours=TIMEDIFF)
                            new_comment.save(using=mousedb_write)
                            count_animals_deferred = count_animals_deferred + 1
                            continue
                        new_pup.pup_id       = dataset.id
                        if dataset.eartag:
                            new_pup.database_id    = dataset.eartag
                        else:
                            new_pup.database_id   = pyratpup.pupid
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
                        if dataset.sex == '?':
                            new_pup.sex = 'u'
                        else:
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
                            
                if (error == 0 and count_animals_deferred == 0):
                    incident_write = WIncident_write.objects.using(mousedb_write).get(incidentid=incident.incidentid)
                    incident_write.status = 5 # Added to AniShare
                    incident_write.save(using=mousedb_write)
                    logger.debug('{}: Incident status {} has been changed to 5.'.format(datetime.now(), incident.incidentid))
                    new_comment = WIncidentcomment()
                    new_comment.incidentid = incident
                    new_comment.comment = 'AniShare: Request status changed to Added to Anishare'
                    new_comment.save(using=mousedb_write)
                    new_comment.commentdate = new_comment.commentdate + timedelta(hours=TIMEDIFF)
                    new_comment.save(using=mousedb_write)
                elif (error == 0 and count_animals_deferred > 0 and count_animals_imported == 0):
                    incident_write = WIncident_write.objects.using(mousedb_write).get(incidentid=incident.incidentid)
                    incident_write.status = 6 # Deferred
                    incident_write.save(using=mousedb_write)
        except BaseException as e: 
            management.call_command("clearsessions")
            ADMIN_EMAIL = getattr(settings, "ADMIN_EMAIL", None)
            send_mail("AniShare Importscriptfehler hourly_insert_from_pyrat.py", '{}: Fehler {} in Zeile {}'.format(mousedb, e,sys.exc_info()[2].tb_lineno), ADMIN_EMAIL, [ADMIN_EMAIL])
        management.call_command("clearsessions")