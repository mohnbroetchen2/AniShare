from django_extensions.management.jobs import DailyJob


class Job(DailyJob):
    help = ""

    def execute(self):
        from django.core import management
        from ...models import WIncident, WIncidentAnimals, Animal, Mouse, WIncidentcomment, WIncidentPups, Pup
        from django.core.mail import EmailMultiAlternatives, send_mail
        from datetime import datetime, timedelta
        from django.conf import settings
        import logging

        mousedb = 'mousedb_test'
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
                logger.debug('{}: count_animals {}'.format(datetime.now(), count_animals))
                for pyratmouse in animallist:
                    i = i + 1
                    try:
                        animouse = Animal.objects.get(mouse_id=pyratmouse.animalid)
                        if (animouse.new_owner):
                            continue
                        if (animouse.available_to >= today):
                            skip = 1
                            break
                    except Exception: 
                            error = 1
                            skip = 1
                            ADMIN_EMAIL = getattr(settings, "ADMIN_EMAIL", None)
                            send_mail("AniShare Check Status Error", 'Fehler {} bei der Statusüberprüfung des Auftrags {} (Maus)'.format( Exception, incident.incidentid), ADMIN_EMAIL, [ADMIN_EMAIL])
                
                for pyratpup in puplist:
                    i = i + 1
                    try:
                        anipup = Animal.objects.get(pup_id=pyratpup.pupid)
                        if (anipup.new_owner):
                            continue
                        if (anipup.available_to >= today):
                            skip = 1
                            break
                    except Exception: 
                            error = 1
                            skip = 1
                            ADMIN_EMAIL = getattr(settings, "ADMIN_EMAIL", None)
                            send_mail("AniShare Check Status Error", 'Fehler {} bei der Statusüberprüfung des Auftrags {} (Pup)'.format( Exception, incident.incidentid), ADMIN_EMAIL, [ADMIN_EMAIL])
                logger.debug('{}:skip {}, i {}, count_animals {}'.format(datetime.now(), skip,i, count_animals))
                if (skip == 0 and i == count_animals):
                    incident.status = 1
                    incident.save()
                    logger.debug('{}: Incident status {} has been changed to 1.'.format(datetime.now(), incident.incidentid))
                    new_comment = WIncidentcomment()
                    new_comment.incidentid = incident
                    new_comment.comment = 'AniShare: Request status changed to closed'
                    new_comment.save() 
        except Exception: 
            management.call_command("clearsessions")
            ADMIN_EMAIL = getattr(settings, "ADMIN_EMAIL", None)
            send_mail("AniShare Importscriptfehler hourly_check_status_incidents.py", 'Fehler {} '.format(Exception), ADMIN_EMAIL, [ADMIN_EMAIL])
        management.call_command("clearsessions")