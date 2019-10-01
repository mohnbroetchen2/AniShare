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
        processedIncidents = []
        ADMIN_EMAIL = getattr(settings, "ADMIN_EMAIL", None)

        try:
            mouselist = Animal.objects.filter(available_to = datetime.today().date() + timedelta(days=2)).filter(animal_type = 'mouse')
            for mouse in mouselist: # Für jede Maus, die noch zwei Tage angeboten wird, und eine mouse_id besitzt
                logger.debug('{}: Maus mit ID {} wird noch zwei Tage ageboten'.format(datetime.now(), mouse.lab_id))
                if mouse.mouse_id is None:
                    continue
                incidentsWithMouse = WIncidentAnimals.objects.using(mousedb).filter(animalid=mouse.mouse_id) # überprüfe ob es Auftrage (Incidents) mit der Maus gibt
                for incidentWithMouse in incidentsWithMouse:
                    logger.debug('{}: Incident {} wird überprüft'.format(datetime.now(), incidentWithMouse.id))
                    if (incidentWithMouse.incidentid in processedIncidents): # Wenn bereits eine Information zu diesem Auftrag rausgegangen ist  
                        continue;
                    incidentFilter = WIncident.objects.using(mousedb).filter(incidentid = incidentWithMouse.incidentid)
                    if len(incidentFilter) == 0:
                        continue
                    incident = WIncident.objects.using(mousedb).get(incidentid = incidentWithMouse.incidentid)

                    if incident.status == 5: # wenn der Auftrag im Status "Added to Anishare" steht
                        initiator = incident.initiator
                        miceInIncident = WIncidentAnimals.objects.using(mousedb).filter(incidentid=incident.incidentid)
                        miceEartags=""
                        countmice = 0
                        for mouse in miceInIncident: # Merke alle Eartags der Mäuse, die dem Auftrag zugeordnet sind.
                            pyratMouse = Mouse.objects.using(mousedb).get(id=mouse.animalid)
                            if countmice == 0:
                                miceEartags = "{}".format(pyratMouse.eartag)
                            else:
                                miceEartags = "{}, {}".format(miceEartags,pyratMouse.eartag)
                            countmice = countmice +1
                        # Nutzer informieren, dass Auftrag mit Id in zwei Tagen ausläuft
                        send_mail("Request Add to AniShare expires", "The PyRAT request Add to AniShare with ID {} expires in two days. Following mice are affected: {}".format(incident.incidentid, miceEartags), "tierschutz@leibniz-fli.de", [initiator.email])
                        processedIncidents.append(incidentWithMouse.incidentid) 
            puplist = Animal.objects.filter(available_to = datetime.today().date() + timedelta(days=2)).filter(animal_type = 'pup')
            for pup in puplist: # Für jede Maus, die noch zwei Tage angeboten wird, und eine mouse_id besitzt
                logger.debug('{}: Pup mit ID {} wird noch zwei Tage ageboten'.format(datetime.now(), pup.lab_id))
                if pup.pup_id is None:
                    continue
                incidentsWithPup = WIncidentPups.objects.using(mousedb).filter(pupid=pup.pup_id) # überprüfe ob es Auftrage (Incidents) mit der Maus gibt
                for incidentWithPup in incidentsWithPup:
                    logger.debug('{}: Incident {} wird überprüft (Pups)'.format(datetime.now(), incidentWithPup.id))
                    if (incidentWithPup.incidentid in processedIncidents): # Wenn bereits eine Information zu diesem Auftrag rausgegangen ist  
                        continue;
                    incidentFilter = WIncident.objects.using(mousedb).filter(incidentid = incidentWithPup.incidentid)
                    if len(incidentFilter) == 0:
                        continue
                    incident = WIncident.objects.using(mousedb).get(incidentid = incidentWithPup.incidentid)

                    if incident.status == 5: # wenn der Auftrag im Status "Added to Anishare" steht
                        initiator = incident.initiator
                        pupInIncidentList = WIncidentPups.objects.using(mousedb).filter(incidentid=incident.incidentid)
                        pupEartags=""
                        countpups = 0
                        for pupInInciden in pupInIncidentList: # Merke alle Eartags der Mäuse, die dem Auftrag zugeordnet sind.
                            pyratPup = Pup.objects.using(mousedb).get(id=pupInInciden.pupid)
                            if countpups == 0:
                                pupEartags = "{}".format(pyratPup.eartag)
                            else:
                                pupEartags = "{}, {}".format(pupEartags,pyratPup.eartag)
                            countpups = countpups +1
                        # Nutzer informieren, dass Auftrag mit Id in zwei Tagen ausläuft
                        send_mail("Request Add to AniShare expires", "The PyRAT request Add to AniShare with ID {} expires in two days. Following pups are affected: {}".format(incident.incidentid, pupEartags), "tierschutz@leibniz-fli.de", [initiator.email])
                        processedIncidents.append(incidentWithPup.incidentid) 
        except BaseException as e: 
            management.call_command("clearsessions")
            send_mail("AniShare inform initiator", '{}: Fehler {} in Zeile {}'.format(mousedb, e,sys.exc_info()[2].tb_lineno), ADMIN_EMAIL, [ADMIN_EMAIL])
        management.call_command("clearsessions")


                        
                        