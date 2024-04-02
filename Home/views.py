from django.db.models import Q
from django.views.generic import TemplateView

from Course.models import VideoCourse
from Home.mixins import URLStorageMixin
from News.models import News
from Weblog.models import Weblog


class HomeView(URLStorageMixin, TemplateView):
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

        latest_news = News.objects.all().order_by('-created_at')

        latest_weblogs = Weblog.objects.all().order_by('-created_at')

        context['latest_video_courses'] = latest_video_courses
        context['latest_news'] = latest_news
        context['latest_weblogs'] = latest_weblogs

        return context
