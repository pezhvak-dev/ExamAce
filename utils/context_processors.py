from Account.models import CustomUser
from Course.filters import ExamFilter
from Course.models import Category as CourseCategory, Exam
from Us.models import SocialMedia, AboutUs
from Weblog.models import Category as WeblogCategory
from News.models import Category as NewsCategory

def social_media(request):
    social_media = SocialMedia.objects.last()
    about_us = AboutUs.objects.last()

    context = {
        'social_media': social_media,
        'about_us': about_us,
    }

    return context


def custom_user_info(request):
    user = request.user

    if user.is_authenticated:
        custom_user = CustomUser.objects.get(username=user.username)

        return {
            'custom_user': custom_user
        }

    else:
        return {
            'custom_user': None
        }


def filter_categories(request):
    categories = CourseCategory.objects.all()

    context = {
        'filter_categories': categories
    }

    return context


def filter_exams(request):
    exams = Exam.objects.all()

    exam_filter = ExamFilter(request.GET, queryset=exams)

    context = {
        'exam_filter_form': exam_filter.form
    }

    return context


def weblog_categories(request):
    categories = WeblogCategory.objects.filter(parent=None, show=True)

    context = {
        'weblog_categories': categories
    }
    return context


def news_categories(request):
    categories = NewsCategory.objects.filter(parent=None, show=True)

    context = {
        'news_categories': categories
    }
    return context
