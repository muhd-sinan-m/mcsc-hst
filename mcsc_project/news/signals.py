from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from django.core.cache import cache
from .models import NewsAttachment, NewsPost

@receiver(post_save, sender=NewsPost)
def invalidate_news_poster_cache(sender, instance, **kwargs):
    """Evict cached presigned URL when a new poster is saved so the new image appears immediately."""
    if instance.poster_image:
        cache.delete(f"supabase_url:{instance.poster_image.name}")

@receiver(pre_delete, sender=NewsAttachment)
def delete_news_attachment_file(sender, instance, **kwargs):
    if instance.file:
        try:
            instance.file.delete(save=False)
        except Exception:
            pass

@receiver(pre_delete, sender=NewsPost)
def delete_news_post_attachments(sender, instance, **kwargs):
    if instance.poster_image:
        try:
            instance.poster_image.delete(save=False)
        except Exception:
            pass
    for attachment in instance.attachments.all():
        if attachment.file:
            try:
                attachment.file.delete(save=False)
            except Exception:
                pass

