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
            animals = Animal.objects.filter(entry_date__range=["2021-02-25", "2021-02-25"])
            dismiss_animals = []
            for a in animals:
                if a in dismiss_animals:
                    continue
                try:
                    original = Animal.objects.filter(database_id=a.database_id).exclude(entry_date__range=["2021-02-25", "2021-02-25"])
                    if len(original) == 1:
                        logger.debug('Doppelter Eintrag von {}'.format(a.database_id))
                        #a.delete()
                except BaseException as e:
                    logger.debug("Fehler {} in Zeile {}".format(e,sys.exc_info()[2].tb_lineno))
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