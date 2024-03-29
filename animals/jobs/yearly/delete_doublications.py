from django_extensions.management.jobs import YearlyJob


class Job(YearlyJob):
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

        logger = logging.getLogger('myscriptlogger')

        ADMIN_EMAIL = getattr(settings, "ADMIN_EMAIL", None)

        #ids = range(16075,26053)
        #ids = range(7100,7143)
        try:
            animals = Animal.objects.all()
            dismiss_animals = []
            for a in animals:
                if a in dismiss_animals:
                    continue
                try:
                    doubles = Animal.objects.filter(database_id=a.database_id)
                    for double in doubles:
                        if double.id == a.id:
                            dismiss_animals.append(double)
                            continue
                        else:
                            if double in dismiss_animals:
                                continue
                            else:
                                dismiss_animals.append(double)
                                double.delete()
                except:
                    continue
            #animals = Animal.objects.all()
            #for a in animals:
            #    if a.pk in ids:
            #        a.delete() 
        except BaseException as e: 
            management.call_command("clearsessions")
            ADMIN_EMAIL = getattr(settings, "ADMIN_EMAIL", None)
            send_mail("AniShare Importscriptfehler delete_doubles", ': Fehler {} in Zeile {}'.format( e,sys.exc_info()[2].tb_lineno), ADMIN_EMAIL, [ADMIN_EMAIL])
        management.call_command("clearsessions")