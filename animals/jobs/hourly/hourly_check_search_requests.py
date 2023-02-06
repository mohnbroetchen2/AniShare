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
        from django.template.loader import render_to_string
        


        logger = logging.getLogger('myscriptlogger')
        ADMIN_EMAIL = getattr(settings, "ADMIN_EMAIL", None)
        DOMAIN = getattr(settings, "DOMAIN", None)
        TIMEDIFF = getattr(settings, "TIMEDIFF", 2)
        wild_type_lines = getattr(settings, "LINES_PROHIBIT_SACRIFICE", None)

        try:
            today = datetime.now().date()
            srequests = SearchRequestAnimal.objects.filter(active_from__lte = today).filter(active_until__gte = today)
            for sr in srequests:
                animallist = Animal.objects.filter(animal_type=sr.animal_type).filter(available_from__lte = today).filter(available_to__gte = today)
                if sr.fish_specie:
                    animallist= animallist.filter(fish_specie=sr.fish_specie)
                if sr.sex:
                    animallist = animallist.filter(sex=sr.sex)
                animallist = animallist.exclude(pk__in = sr.found_animals.all().values('pk'))
              
                if sr.age_min:
                    animallist= animallist.filter(age__gte=sr.age_min)
                if sr.age_max:
                    animallist= animallist.filter(age__lte=sr.age_max)

                if sr.wild_type:
                    for animal in animallist:
                        found_wild_type_line = 0
                        lines = list(animal.line.split(";"))
                        for line in lines:
                            if line in wild_type_lines:
                                found_wild_type_line = 1
                        if found_wild_type_line == 0:
                            animallist = animallist.remove(animal)

                if animallist:
                    print(animallist.values_list)
                    subject = "AniShare found animals"
                    message = render_to_string('email_search_request.html', {'first_name': sr.user.first_name, 'animals': animallist, 'domain':DOMAIN})
                    sender_address = getattr(settings, "SEND_EMAIL_ADDRESS ", 'noreply@anishare.leibniz-fli.de')
                    send_mail(subject, message, sender_address, [sr.user.email],html_message=message)
                    for animal in animallist:
                        sr.found_animals.add(animal)

                    
                
        except BaseException as e: 
            management.call_command("clearsessions")
            ADMIN_EMAIL = getattr(settings, "ADMIN_EMAIL", None)
            send_mail("AniShare Importscriptfehler hourly_check_search_requests.py", 'Fehler {} in Zeile {}'.format(e,sys.exc_info()[2].tb_lineno), ADMIN_EMAIL, [ADMIN_EMAIL])
        management.call_command("clearsessions")