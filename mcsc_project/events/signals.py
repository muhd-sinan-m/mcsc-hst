from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Event

@receiver(pre_delete, sender=Event)
def delete_event_poster(sender, instance, **kwargs):
    if instance.poster_image:
        try:
            instance.poster_image.delete(save=False)
        except Exception:
            pass
