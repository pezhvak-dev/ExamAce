from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from jdatetime import datetime

from Account.models import CustomUser
from Course.models import Exam, EnteredExamUser, DownloadedQuestionFile


class CanUserEnterExamMixin:
    def dispatch(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        user = request.user

        user = CustomUser.objects.get(username=user.username)
        can_user_participate = Exam.objects.filter(slug=slug, participated_users=user).exists()

        if not can_user_participate:
            redirect_url = request.session.get('current_url')

            messages.error(request, f"جهت ورود به آزمون، ابتدا باید در آن ثبت نام کنید.")

            if redirect_url is not None:
                return redirect(redirect_url)

            return redirect("home:home")

        return super().dispatch(request, *args, **kwargs)


class CheckForExamTimeMixin:
    def dispatch(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        user = request.user

        exam = Exam.objects.get(slug=slug)
        downloaded_question_file = DownloadedQuestionFile.objects.get(exam=exam, user=user)
        start = downloaded_question_file.created_at
        delta = timezone.now() - start

        if delta.total_seconds() > exam.total_duration.total_seconds():
            # Print a message if time is up
            messages.error(request, f"متاسفانه زمان شما به اتمام رسیده و امکان شرکت در آزمون برای شما فراهم نیست.")

            return redirect(reverse("course:exam_detail", kwargs={"slug": slug}))

        return super().dispatch(request, *args, **kwargs)


class AllowedExamsOnlyMixin:
    def dispatch(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        exam = Exam.objects.get(slug=slug)

        if not exam.is_entrance_allowed:
            messages.error(request, f"با عرض پوزش، در حال حاضر شرکت در آزمون {exam.name} امکان پذیر نیست.")

        return super().dispatch(request, *args, **kwargs)
