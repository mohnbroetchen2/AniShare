from django_extensions.management.jobs import DailyJob


class Job(HourlyJob):
    help = ""

    def execute(self):
        from django.core import management
        from ...models import WIncident, WIncidentAnimals, Animal, Mouse, WIncidentcomment
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
        management.call_command("clearsessions")