from django_extensions.management.jobs import DailyJob


class Job(DailyJob):
    help = ""

    def execute(self):
        from django.core import management
        from ...models import WIncident, WIncident_write, WIncidentAnimals, Animal, Mouse, WIncidentcomment, WIncidentPups, Pup
        from django.core.mail import EmailMultiAlternatives, send_mail
        from datetime import datetime, timedelta
        from django.conf import settings
        import logging
        import sys

        mousedb = 'mousedb_test'
        mousedb_write = 'mousedb_test_write'
        logger = logging.getLogger('myscriptlogger')
        try:
            today = datetime.now().date()
            incidentlist = WIncident.objects.using(mousedb).all().filter(status=5)
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
                logger.debug('{}:skip {}, i {}, count_animals {}'.format(datetime.now(), skip,i, count_animals))
                if (skip == 0 and i == count_animals):
                    incident_write = WIncident_write.objects.using(mousedb_write).get(incidentid=incident.incidentid)
                    incident_write.status = 1
                    incident_write.save(using=mousedb_write)
                    logger.debug('{}: Incident status {} has been changed to 1.'.format(datetime.now(), incident.incidentid))
                    new_comment = WIncidentcomment()
                    new_comment.incidentid = incident
                    new_comment.comment = 'AniShare: Request status changed to closed'
                    new_comment.save(using=mousedb_write) 
                    new_comment.commentdate = new_comment.commentdate + timedelta(hours=TIMEDIFF)
                    new_comment.save(using=mousedb_write)
        except BaseException as e:  
            management.call_command("clearsessions")
            ADMIN_EMAIL = getattr(settings, "ADMIN_EMAIL", None)
            send_mail("AniShare Importscriptfehler hourly_check_status_incidents.py", 'Fehler {} in Zeile {}'.format(e,sys.exc_info()[2].tb_lineno), ADMIN_EMAIL, [ADMIN_EMAIL])
        management.call_command("clearsessions")