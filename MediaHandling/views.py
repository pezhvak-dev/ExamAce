import os

from django.conf import settings
from django.contrib import messages
from django.http import FileResponse
from django.shortcuts import redirect

from Course.models import Exam



def serve_protected_media(request, filepath):
    user = request.user

    full_filepath = os.path.join(settings.MEDIA_ROOT, filepath)
    if not os.path.exists(full_filepath):
        messages.error(request, f"چنین فایلی در دیتابیس وجود ندارد!")

        redirect_url = request.session.get('current_url')

        if redirect_url is not None:
            return redirect(redirect_url)

        return redirect("home:home")

    try:
        if "Course/Exam/pdf" in filepath:
            exam = Exam.objects.get(questions_file=filepath)
            print(exam.designer)

            has_user_participated_in_exam = user in exam.participated_users.all()

            if user.is_authenticated:
                if has_user_participated_in_exam is False:
                    messages.error(request, f"شما مجوز مشاهده این فایل را ندارید!")

                    redirect_url = request.session.get('current_url')

                    if redirect_url is not None:
                        return redirect(redirect_url)

                    return redirect("home:home")

            else:
                messages.error(request, f"شما مجوز مشاهده این فایل را ندارید!")

                redirect_url = request.session.get('current_url')

                if redirect_url is not None:
                    return redirect(redirect_url)

                return redirect("home:home")

        full_filepath = os.path.join(settings.MEDIA_ROOT, filepath)

        return FileResponse(open(full_filepath, 'rb'))

    except:
        messages.error(request, f"مشکلی از سمت سرور رخ داده است!")

        redirect_url = request.session.get('current_url')

        if redirect_url is not None:
            return redirect(redirect_url)

        return redirect("home:home")