from django_extensions.management.jobs import HourlyJob


class Job(HourlyJob):
    help = ""

    def execute(self):
        from django.core import management
        from ...models import  SearchRequestAnimal, Animal
        from django.contrib.auth.models import User
        from django.core.mail import EmailMultiAlternatives, send_mail
        from datetime import datetime, timedelta
        from django.conf import settings
        import logging
        import sys


        logger = logging.getLogger('myscriptlogger')
        ADMIN_EMAIL = getattr(settings, "ADMIN_EMAIL", None)
        TIMEDIFF = getattr(settings, "TIMEDIFF", 2)

        try:
            today = datetime.now().date()
            srequests = SearchRequestAnimal.objects.filter(active_from__lte = today).filter(active_until__gte = today)
            for sr in srequests:
                print(sr.animal_type)
                if sr.animal_type == "mouse" or sr.animal_type == "pup" :
                    if sr.sex:
                        animallist = Animal.objects.filter(type=sr.animal_type).filter(sex=sr.sex)
                    else:
                        animallist = Animal.objects.filter(type=sr.animal_type)
                if sr.animal_type == "fish":
                    animallist = Animal.objects.filter(animal_type=sr.animal_type).filter(available_from__lte = today).filter(available_to__gte = today)
                    if sr.sex:
                        animallist = animallist.filter(sex=sr.sex)
                    print(animallist)
                    #animallist = filter(lambda animallist:)

                    
                
        except BaseException as e: 
            management.call_command("clearsessions")
            ADMIN_EMAIL = getattr(settings, "ADMIN_EMAIL", None)
            send_mail("AniShare Importscriptfehler hourly_check_search_requests.py", 'Fehler {} in Zeile {}'.format(e,sys.exc_info()[2].tb_lineno), ADMIN_EMAIL, [ADMIN_EMAIL])
        management.call_command("clearsessions")