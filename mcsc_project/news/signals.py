from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import NewsAttachment, NewsPost

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
