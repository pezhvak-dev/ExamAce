from django.db.models import Q
from django.views.generic import TemplateView

from Course.models import VideoCourse


class HomeView(TemplateView):
    template_name = 'Home/index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        latest_video_courses = VideoCourse.objects.values("teacher__image", "category__name",
                                                          "cover_image", "teacher__username",
                                                          "teacher__slug", "teacher__full_name",
                                                          "total_sessions", "total_seasons",
                                                          "has_discount", "type", "price", "slug",
                                                          "price_after_discount", "total_duration",
                                                          "name", "status").order_by('-created_at').filter(
            Q(status="F") | Q(status="IP"))[:6]

        context['latest_video_courses'] = latest_video_courses

        return context


class TempInfo(TemplateView):
    template_name = "Home/temp_info.html"
