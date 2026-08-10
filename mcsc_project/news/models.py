import os
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify

class NewsPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(help_text="Full news article content")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='news_posts', limit_choices_to={'is_staff': True})
    event = models.ForeignKey('events.Event', on_delete=models.SET_NULL, null=True, blank=True, related_name='news_posts', help_text="Optional linked event to share its poster image")
    poster_image = models.ImageField(upload_to='news_posters/', null=True, blank=True, help_text="Optional dedicated cover poster image for this news post")
    use_default_poster = models.BooleanField(default=False, verbose_name="Use general MCSC Logo as news poster/cover", help_text="Check to use the official MCSC Logo as the news cover.")
    is_published = models.BooleanField(default=True, db_index=True)
    published_at = models.DateTimeField(default=timezone.now, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_at']
        indexes = [
            models.Index(fields=['is_published', '-published_at']),
        ]

    @property
    def slug(self):
        s = slugify(self.title, allow_unicode=True)
        if not s or s.strip('-') == '':
            return str(self.id) if self.id else "news"
        return s

    @property
    def poster_url(self):
        if self.poster_image:
            try:
                return self.poster_image.url
            except Exception:
                pass
        if self.use_default_poster:
            try:
                from django.conf import settings
                return f"{settings.STATIC_URL}images/mcsc_logo.png"
            except Exception:
                return "/static/images/mcsc_logo.png"
        if self.event and self.event.poster_url:
            return self.event.poster_url
        return None

    def save(self, *args, **kwargs):
        if self.poster_image:
            self.use_default_poster = False
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class NewsAttachment(models.Model):
    FILE_TYPE_CHOICES = (
        ('image', 'Image'),
        ('document', 'Document'),
    )
    news_post = models.ForeignKey(NewsPost, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='news_attachments/')
    file_type = models.CharField(max_length=20, choices=FILE_TYPE_CHOICES, default='document')

    @property
    def generic_filename(self):
        ext = os.path.splitext(self.file.name)[1].lower() if self.file else ''
        if self.file_type == 'image':
            return f"image{ext}" if ext else "image.jpg"
        if ext in ['.pdf']:
            return "report.pdf"
        elif ext in ['.doc', '.docx']:
            return "report.docx"
        elif ext in ['.xls', '.xlsx']:
            return "report.xlsx"
        elif ext in ['.zip', '.rar']:
            return "document.zip"
        return f"document{ext}" if ext else "document"

    def save(self, *args, **kwargs):
        if self.file:
            ext = os.path.splitext(self.file.name)[1].lower()
            if ext in ['.jpg', '.jpeg', '.png', '.webp', '.gif']:
                self.file_type = 'image'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Attachment for {self.news_post.title} ({self.file_type})"
