from django.contrib import admin
from .models import NewsPost, NewsAttachment

class NewsAttachmentInline(admin.TabularInline):
    model = NewsAttachment
    extra = 1

@admin.register(NewsPost)
class NewsPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'event', 'use_default_poster', 'is_published', 'published_at')
    list_filter = ('is_published', 'use_default_poster', 'published_at', 'author', 'event')
    search_fields = ('title', 'content')
    inlines = [NewsAttachmentInline]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "author":
            from django.contrib.auth import get_user_model
            kwargs["queryset"] = get_user_model().objects.filter(is_staff=True)
        elif db_field.name == "event":
            from events.models import Event
            from django.db import models as db_models
            kwargs["queryset"] = Event.objects.filter(
                db_models.Q(use_default_poster=True) |
                (db_models.Q(poster_image__isnull=False) & ~db_models.Q(poster_image=''))
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
