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

        mousedb = 'mousedb_test'
        mousedb_write = 'mousedb_test_write'
        logger = logging.getLogger('myscriptlogger')
        processedIncidents = []
        ADMIN_EMAIL = getattr(settings, "ADMIN_EMAIL", None)

        try:
            mouselist = Animal.objects.filter(available_to == datetime.today().date() + timedelta(days=2)).filter(animal_type == 'mouse').filter(mouse_id is not None)
            for mouse in mouselist: # Für jede Maus, die noch zwei Tage angeboten wird, und eine mouse_id besitzt
                incidentsWithMouse = WIncidentAnimals.objects.using(mousedb).filter(id=mouse.mouse_id) # überprüfe ob es Auftrage (Incidents) mit der Maus gibt
                for incidentWithMouse in incidentsWithMouse:
                    if (incidentWithMouse.incidentid in processedIncidents): # Wenn bereits eine Information zu diesem Auftrag rausgegangen ist  
                        continue;
                    incident = WIncident.objects.using(mousedb).get(incidentid = incidentWithMouse.incidentid)
                    if incident.status == 5: # wenn der Auftrag im Status "Added to Anishare" steht
                        initiator = incident.initiator
                        miceInIncident = WIncidentAnimals.objects.using(mousedb).filter(incidentid=incident.incidentid)
                        miceEartags=""
                        for mouse in miceInIncident: # Merke alle Eartags der Mäuse, die dem Auftrag zugeordnet sind.
                            pyratMouse = Mouse.objects.using(mousedb).get(id=mouse.animalid)
                            miceEartags = "{}, {}".format(miceEartags,pyratMouse.eartag)
                        # Nutzer informieren, dass Auftrag mit Id in zwei Tagen ausläuft
                        send_mail("Request Add to AniShare expires", 'The PyRAT request Add to AniShare with ID {} expires in two days. Following mice are affected: {}'.format(incident.incidentid, miceEartags), ADMIN_EMAIL, [initiator.email])
                        processedIncidents.insert(incidentWithMouse.incidentid) 
        except BaseException as e: 
            management.call_command("clearsessions")
            send_mail("AniShare inform initiator", '{}: Fehler {} in Zeile {}'.format(mousedb, e,sys.exc_info()[2].tb_lineno), ADMIN_EMAIL, [ADMIN_EMAIL])
        management.call_command("clearsessions")


                        
                        