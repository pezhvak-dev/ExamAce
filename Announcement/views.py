from django.views.generic import ListView

from Announcement.models import Announcement


class AnnouncementListView(ListView):
    model = Announcement
    template_name = "Announcement/announcements.html"
    context_object_name = "announcements"

    def get_queryset(self):
        user = self.request.user

        return Announcement.objects.filter(users=user).order_by("-created_at")
