from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from django.core.cache import cache
from .models import Event

@receiver(post_save, sender=Event)
def invalidate_event_poster_cache(sender, instance, **kwargs):
    """Evict cached presigned URL when a new poster is saved so the new image appears immediately."""
    if instance.poster_image:
        cache.delete(f"supabase_url:{instance.poster_image.name}")

@receiver(pre_delete, sender=Event)
def delete_event_poster(sender, instance, **kwargs):
    if instance.poster_image:
        try:
            instance.poster_image.delete(save=False)
        except Exception:
            pass
