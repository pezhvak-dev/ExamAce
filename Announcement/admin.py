from django.contrib import admin

from Announcement.models import Announcement


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'title', 'created_at', 'mode', 'visibility', 'has_been_read')
