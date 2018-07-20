from django.apps import AppConfig


class AnimalsConfig(AppConfig):
    name = 'animals'

@receiver(post_save, sender=Organ)
def update_killing_person(sender, instance, created, **kwargs):
    if (instance.killing_person == None):
        instance.killing_person = instance.responsible_person__email
        instance.killing_person.save()