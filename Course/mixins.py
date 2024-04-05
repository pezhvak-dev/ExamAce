from django.contrib import messages
from django.shortcuts import redirect

from Account.models import CustomUser
from Course.models import Exam


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
