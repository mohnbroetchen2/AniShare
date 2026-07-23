from django_extensions.management.jobs import HourlyJob


class Job(HourlyJob):
    help = ""

    def execute(self):
        from django.core import management
        from ...models import WIncident, WIncident_write, WIncidentAnimals, Animal, Mouse, WIncidentPups, Pup, WIncidentanimals_write, WIncidentpups_write
        from ...models import SacrificeIncidentToken, Comment, Comment_work_request_ref, PyratUser
        from django.core.mail import EmailMultiAlternatives, send_mail
        from datetime import datetime, timedelta
        from django.conf import settings
        from django.core.signing import Signer
        from django.core.mail import EmailMultiAlternatives, send_mail
        from django.template.loader import render_to_string
        from django.core.mail import EmailMessage
        from django.conf import settings
        import logging
        import sys

        mousedb = 'mousedb'
        mousedb_write = 'mousedb_write'
        LINES_PROHIBIT_SACRIFICE = getattr(settings, "LINES_PROHIBIT_SACRIFICE", None)
        logger = logging.getLogger('myscriptlogger')
        TIMEDIFF = getattr(settings, "TIMEDIFF", 2)
        try:
            today = datetime.now().date() # Gets today's date
            incidentlist = WIncident.objects.using(mousedb).all().filter(incidentid=70278) # Retrieves all incidents of class 22 (AddToAniShare) with status 5 (AddedToAniShare) from the database
            for incident in incidentlist: # for each incident
                i = 0
                animallist = WIncidentAnimals.objects.using(mousedb).filter(incidentid = incident.incidentid) # Retrieves all animals for the incident

                incident_write = WIncident_write.objects.using(mousedb_write).get(incidentid=incident.incidentid)
                incident_write.status = 1
                incident_write.closedate = datetime.now()
                incident_write.save(using=mousedb_write)
                logger.debug('{}: Incident status {} has been changed to 1.'.format(datetime.now(), incident.incidentid))

                incident_animals = WIncidentanimals_write.objects.using(mousedb_write).filter(incidentid = incident_write.incidentid)
                for entry in incident_animals:
                    entry.perform_status = 'performed'
                    entry.save()
                incident_pups = WIncidentpups_write.objects.using(mousedb_write).filter(incidentid = incident_write.incidentid)
                for entry in incident_pups:
                    entry.perform_status = 'performed'
                    entry.save()

                # add a comment to the incident
                comment = Comment()
                anishareuser = PyratUser.objects.using(mousedb).get(username='AniShare')
                comment.creator_id = anishareuser
                comment.content = 'AniShare: Request status changed to closed'
                comment.save(using=mousedb_write)
                comment.created = comment.created + timedelta(hours=TIMEDIFF)
                comment.save(using=mousedb_write)

                comment_work_request_ref = Comment_work_request_ref()
                comment_work_request_ref.comment_id = comment.id
                comment_work_request_ref.work_request_id = incident.incidentid
                comment_work_request_ref.save(using=mousedb_write)

                if incident.sacrifice_reason:

                    
                    # Send email to initiator to confirm sacrifice request
                    animallist = Animal.objects.filter(pyrat_incidentid = incident.incidentid)
                    i = 0
                    for animal in animallist:
                        if animal.new_owner:
                            animallist = animallist.exclude(pk=animal.pk)
                        if animal.line in LINES_PROHIBIT_SACRIFICE and incident_write.sacrifice_reason != 7:
                            animallist = animallist.exclude(pk=animal.pk) 
                        i = i + 1
                    if len(animallist) > 0:
                        # save token and send to Add to AniShare initiator to create sacrifice request
                        new_sacrifice_incident_token            = SacrificeIncidentToken()
                        new_sacrifice_incident_token.initiator  = incident.initiator.username
                        new_sacrifice_incident_token.incidentid = incident.incidentid
                        signer = Signer()
                        new_sacrifice_incident_token.urltoken   = signer.sign("{}".format(incident.incidentid))
                        new_sacrifice_incident_token.save()

                        initiator_name = "{} {}".format(incident.initiator.firstname,incident.initiator.lastname)
                        sacrifice_link = "{}/{}/{}".format(settings.DOMAIN,"confirmsacrificerequest",new_sacrifice_incident_token.urltoken)
                        message = render_to_string('email_animals_sacrifice.html',{'animals':animallist, 'initiator':initiator_name, 'sacrifice_link':sacrifice_link})
                        subject = "Confirmation sacrifice request"
                        recipient = incident.initiator.email
                        msg = EmailMessage(subject, message, "tierschutz@leibniz-fli.de", [recipient])
                        msg.content_subtype = "html"
                        msg.send()
                        logger.debug('Mail Confirmation sacrifice request an {} mit Link {} gesendet'.format(recipient,sacrifice_link))
                
        except BaseException as e:  
            logger.error('{}: AniShare Importscriptfehler hourly_check_status_incidents.py: Fehler {} in Zeile {}'.format(datetime.now(),e, sys.exc_info()[2].tb_lineno)) 
            ADMIN_EMAIL = getattr(settings, "ADMIN_EMAIL", None)
            send_mail("AniShare Importscriptfehler hourly_check_status_incidents.py", 'Fehler {} in Zeile {}'.format(e,sys.exc_info()[2].tb_lineno), ADMIN_EMAIL, [ADMIN_EMAIL])
        management.call_command("clearsessions")