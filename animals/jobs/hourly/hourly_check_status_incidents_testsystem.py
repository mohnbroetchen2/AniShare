from django_extensions.management.jobs import HourlyJob


class Job(HourlyJob):
    help = ""

    def execute(self):
        from django.core import management
        from ...models import WIncident, WIncident_write, WIncidentAnimals, Animal, Mouse, WIncidentcomment, WIncidentPups, Pup, WIncidentanimals_write, WIncidentpups_write
        from django.core.mail import EmailMultiAlternatives, send_mail
        from datetime import datetime, timedelta
        from django.conf import settings
        import logging
        import sys

        mousedb = 'mousedb_test'
        mousedb_write = 'mousedb_test_write'
        logger = logging.getLogger('myscriptlogger')
        TIMEDIFF = getattr(settings, "TIMEDIFF", 2)
        try:
            today = datetime.now().date()
            incidentlist = WIncident.objects.using(mousedb).all().filter(incidentclass=22).filter(status=5)
            for incident in incidentlist:
                skip = 0
                error = 0
                i = 0
                animallist = WIncidentAnimals.objects.using(mousedb).filter(incidentid = incident.incidentid)
                puplist = WIncidentPups.objects.using(mousedb).filter(incidentid = incident.incidentid)
                count_mice = animallist.count()
                count_pups = puplist.count()
                count_animals = count_mice + count_pups
                #logger.debug('{}: count_animals {}'.format(datetime.now(), count_animals))
                for pyratmouse in animallist:
                    i = i + 1
                    try:
                        animouseFilter = Animal.objects.filter(mouse_id=pyratmouse.animalid)
                        if len(animouseFilter) == 0:
                            continue
                        else:
                            animouse = Animal.objects.get(mouse_id=pyratmouse.animalid)
                        if (animouse.new_owner):
                            continue
                        if (animouse.available_to >= today):
                            skip = 1
                            break
                    except BaseException as e: 
                            error = 1
                            skip = 1
                            ADMIN_EMAIL = getattr(settings, "ADMIN_EMAIL", None)
                            send_mail("AniShare Check Status Error", 'Fehler {} bei der Statusüberprüfung des Auftrags {} (Maus) in Zeile {}'.format( e, incident.incidentid, sys.exc_info()[2].tb_lineno), ADMIN_EMAIL, [ADMIN_EMAIL])
                for pyratpup in puplist:
                    i = i + 1
                    try:
                        anipupFiler = Animal.objects.filter(pup_id=pyratpup.pupid)
                        if len(anipupFiler) == 0:
                            continue
                        anipup = Animal.objects.get(pup_id=pyratpup.pupid)
                        if (anipup.new_owner):
                            continue
                        if (anipup.available_to >= today):
                            skip = 1
                            break
                    except BaseException as e:  
                            error = 1
                            skip = 1
                            ADMIN_EMAIL = getattr(settings, "ADMIN_EMAIL", None)
                            send_mail("AniShare Check Status Error", 'Fehler {} bei der Statusüberprüfung des Auftrags {} (Pup) in Zeile {}'.format( e, incident.incidentid,sys.exc_info()[2].tb_lineno), ADMIN_EMAIL, [ADMIN_EMAIL])
                if (skip == 0 and i == count_animals):
                    incident_write = WIncident_write.objects.using(mousedb_write).get(incidentid=incident.incidentid)
                    incident_write.status = 1
                    incident_write.closedate = datetime.now()
                    incident_write.save(using=mousedb_write)
                    logger.debug('{}: Incident status {} has been changed to 1.'.format(datetime.now(), incident.incidentid))
                    new_comment = WIncidentcomment()
                    new_comment.incidentid = incident
                    new_comment.comment = 'AniShare: Request status changed to closed'
                    new_comment.save(using=mousedb_write) 
                    new_comment.commentdate = new_comment.commentdate + timedelta(hours=TIMEDIFF)
                    new_comment.save(using=mousedb_write)

                    new_sacrifice_incident                  =  WIncident_write()
                    new_sacrifice_incident.incidentclass    = 1
                    new_sacrifice_incident.initiator        = incident_write.initiator
                    new_sacrifice_incident.owner            = incident_write.owner
                    new_sacrifice_incident.responsible      = incident_write.responsible
                    new_sacrifice_incident.sacrifice_reason = incident_write.sacrifice_reason
                    new_sacrifice_incident.sacrifice_method = incident_write.sacrifice_method
                    new_sacrifice_incident.behavior_id      = 4 # Sacrifice
                    new_sacrifice_incident.priority         = 3
                    new_sacrifice_incident.status           = 2
                    new_sacrifice_incident.duedate          = datetime.now() + timedelta(hours=TIMEDIFF)
                    new_sacrifice_incident.approved         = 1
                    new_sacrifice_incident.save(using=mousedb_write)
                    
                    wincident_new_sacrifice_incident = WIncident.objects.using(mousedb).get(incidentid = new_sacrifice_incident.incidentid)

                    new_comment = WIncidentcomment()
                    new_comment.incidentid = wincident_new_sacrifice_incident
                    new_comment.comment = 'AniShare: Request created'
                    new_comment.save(using=mousedb_write) 
                    new_comment.commentdate = new_comment.commentdate + timedelta(hours=TIMEDIFF)
                    new_comment.save(using=mousedb_write)

                    for pyratmouse in animallist:
                        incident_mouse = WIncidentanimals_write()
                        incident_mouse.incidentid = wincident_new_sacrifice_incident
                        incident_mouse.animalid = pyratmouse.animalid
                        incident_mouse.save(using=mousedb_write)

                    for pyratpup in puplist:
                        incident_pup = WIncidentpups_write()
                        incident_pup.incidentid = wincident_new_sacrifice_incident
                        incident_pup.pupid = pyratpup.pupid
                        incident_pup.save(using=mousedb_write)
        except BaseException as e:  
            logger.error('{}: AniShare Importscriptfehler hourly_check_status_incidents.py: Fehler {} in Zeile {}'.format(datetime.now(),e, sys.exc_info()[2].tb_lineno)) 
            ADMIN_EMAIL = getattr(settings, "ADMIN_EMAIL", None)
            send_mail("AniShare Importscriptfehler hourly_check_status_incidents.py", 'Fehler {} in Zeile {}'.format(e,sys.exc_info()[2].tb_lineno), ADMIN_EMAIL, [ADMIN_EMAIL])
        management.call_command("clearsessions")