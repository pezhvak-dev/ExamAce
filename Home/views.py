from django.db.models import Q
from django.views.generic import TemplateView

from Course.models import VideoCourse, Exam
from Home.mixins import URLStorageMixin
from Home.models import HeroBanner, Banner1, Banner2, Banner3
from News.models import News
from Us.models import Message
from Weblog.models import Weblog


class HomeView(URLStorageMixin, TemplateView):
    template_name = 'Home/index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        latest_video_courses = VideoCourse.objects.values("teacher__image",
                                                          "category__name",
                                                          "cover_image",
                                                          "teacher__username",
                                                          "teacher__slug",
                                                          "teacher__full_name",
                                                          "total_sessions",
                                                          "total_seasons",
                                                          "has_discount",
                                                          "type",
                                                          "price",
                                                          "slug",
                                                          "price_after_discount",
                                                          "total_duration",
                                                          "name",
                                                          "status").order_by('-created_at').filter(
            Q(status="F") | Q(status="IP"))[:6]

        latest_exams_1 = Exam.objects.values(
            "name",
            "slug",
            "designer__image",
            "designer__full_name",
            "designer__slug",
            "category__name",
            "cover_image",
            "type",
            "price",
            "has_discount",
            "discount_percentage",
            "price_after_discount",
            "total_duration",
            "created_at",
        ).order_by('-created_at')[:2]

        latest_exams_2 = Exam.objects.values(
            "name",
            "slug",
            "designer__image",
            "designer__full_name",
            "designer__slug",
            "category__name",
            "cover_image",
            "type",
            "price",
            "has_discount",
            "discount_percentage",
            "price_after_discount",
            "total_duration",
            "created_at",
        ).order_by('-created_at')[2:4]

        latest_news = News.objects.all().order_by('-created_at')

        latest_weblogs = Weblog.objects.all().order_by('-created_at')

        hero_banners = HeroBanner.objects.filter(can_be_shown=True).order_by('-created_at')

        banner_1 = Banner1.objects.filter(can_be_shown=True).order_by('-created_at')[:2]

        banner_2 = Banner2.objects.filter(can_be_shown=True).last()

        banner_3 = Banner3.objects.filter(can_be_shown=True).order_by('-created_at')[:2]

        attitudes = Message.objects.filter(can_be_shown=True).order_by('-created_at')

        context['latest_video_courses'] = latest_video_courses  # Is a queryset
        context['latest_exams_1'] = latest_exams_1  # Is a queryset
        context['latest_exams_2'] = latest_exams_2  # Is a queryset
        context['latest_news'] = latest_news  # Is a queryset
        context['latest_weblogs'] = latest_weblogs  # Is a queryset
        context['hero_banners'] = hero_banners  # Is a queryset
        context['banner_1'] = banner_1  # Is a queryset
        context['banner_2'] = banner_2  # Is a single object
        context['banner_3'] = banner_3  # Is a queryset
        context['attitudes'] = attitudes  # Is a queryset

        return context
