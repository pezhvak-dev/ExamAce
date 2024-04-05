from datetime import datetime

import pytz
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import uri_to_iri
from django.views.generic import ListView, DetailView, View

from Account.mixins import AuthenticatedUsersOnlyMixin
from Course.mixins import CanUserEnterExamMixin, CheckForExamTimeMixin, AllowedExamsOnlyMixin, \
    DownloadedQuestionsFileFirstMixin, AllowedFilesDownloadMixin
from Course.models import VideoCourse, Exam, ExamAnswer, DownloadedQuestionFile, EnteredExamUser
from Home.mixins import URLStorageMixin
from Home.models import Banner4, Banner5
from utils.useful_functions import get_time_difference


class AllVideoCourses(URLStorageMixin, ListView):
    model = VideoCourse
    context_object_name = 'courses'
    template_name = 'Course/all_video_courses.html'

    def get_queryset(self):
        video_courses = VideoCourse.objects.select_related('category', 'teacher').order_by('-created_at')

        return video_courses


class VideoCourseDetail(URLStorageMixin, DetailView):
    model = VideoCourse
    context_object_name = 'course'
    template_name = 'Course/video_course_detail.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('category', 'teacher')

    def get_object(self, queryset=None):
        slug = uri_to_iri(self.kwargs.get(self.slug_url_kwarg))
        queryset = self.get_queryset()
        return get_object_or_404(queryset, **{self.slug_field: slug})


class AllBookCourses(URLStorageMixin, ListView):
    pass


class AllExams(URLStorageMixin, ListView):
    model = Exam
    context_object_name = 'exams'
    template_name = 'Course/all_exams.html'

    def get_queryset(self):
        exams = Exam.objects.select_related('category', 'designer').order_by('-created_at')

        return exams


class ExamDetail(URLStorageMixin, DetailView):
    model = Exam
    context_object_name = 'exam'
    template_name = 'Course/exam_detail.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('category', 'designer')

    def get_object(self, queryset=None):
        slug = uri_to_iri(self.kwargs.get(self.slug_url_kwarg))
        queryset = self.get_queryset()
        return get_object_or_404(queryset, **{self.slug_field: slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        #  Checks if user can enter exam anymore or not. (Based on entrance time)
        is_time_up = False
        if EnteredExamUser.objects.filter(user=user, exam=self.object).exists():
            entered_exam_user = EnteredExamUser.objects.get(user=user, exam=self.object)

            date_1 = entered_exam_user.created_at
            date_2 = datetime.now(pytz.timezone('Iran'))

            total_duration = self.object.total_duration.total_seconds()

            difference = get_time_difference(date_1=date_1, date_2=date_2)

            time_left = int(total_duration - difference)

            if time_left < 0:
                is_time_up = True

        can_be_continued = False
        if EnteredExamUser.objects.filter(user=user, exam=self.object).exists():
            can_be_continued = True

        sections = ExamAnswer.objects.filter(exam=self.object)

        section_names = list(set(sections.values_list('section__name', flat=True)))
        banner_4 = Banner4.objects.filter(can_be_shown=True).last()
        banner_5 = Banner5.objects.filter(can_be_shown=True).last()

        try:
            is_user_registered = Exam.objects.filter(participated_users=user, slug=self.object.slug).exists()

        except TypeError:
            is_user_registered = False

        context['banner_4'] = banner_4  # Returns a single object
        context['banner_5'] = banner_5  # Returns a single object
        context['is_time_up'] = is_time_up  # Returns a boolean
        context['is_user_registered'] = is_user_registered  # Returns a boolean
        context['can_be_continued'] = can_be_continued  # Returns a boolean
        context['sections_names'] = section_names  # Returns a list

        return context


class RegisterExam(AuthenticatedUsersOnlyMixin, AllowedExamsOnlyMixin, URLStorageMixin, View):
    def get(self, request, *args, **kwargs):
        slug = kwargs.get("slug")
        user = request.user
        exam = Exam.objects.get(slug=slug)

        if exam.type == "F":
            exam.participated_users.add(user)
            messages.success(request, f"ثبت نام در آزمون {exam.name} با موفقیت انجام شد.")

        else:
            messages.warning(request, f"آزمون {exam.name} به سبد خرید شما افزوده شد.")

        return redirect(reverse("course:exam_detail", kwargs={"slug": slug}))


class ExamQuestionDownload(AuthenticatedUsersOnlyMixin, AllowedFilesDownloadMixin,
                           CanUserEnterExamMixin, URLStorageMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        slug = kwargs.get('slug')
        exam = Exam.objects.get(slug=slug)
        questions_file = exam.questions_file

        # Set headers for file download
        response = HttpResponse(questions_file, content_type='application/force-download')
        response['Content-Disposition'] = f'attachment; filename="{exam.question_file_name}.pdf"'

        if not DownloadedQuestionFile.objects.filter(exam=exam, user=user).exists():
            DownloadedQuestionFile.objects.create(exam=exam, user=user)

        return response


class EnterExam(AuthenticatedUsersOnlyMixin, CanUserEnterExamMixin, AllowedExamsOnlyMixin,
                CheckForExamTimeMixin, DownloadedQuestionsFileFirstMixin, URLStorageMixin, View):
    template_name = "Course/multiple_choice_exam.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        slug = kwargs.get('slug')

        exam = Exam.objects.get(slug=slug)

        if not EnteredExamUser.objects.filter(exam=exam, user=user).exists():
            EnteredExamUser.objects.create(exam=exam, user=user)

        entered_exam_user = EnteredExamUser.objects.get(exam=exam, user=user)

        date_1 = entered_exam_user.created_at
        date_2 = datetime.now(pytz.timezone('Iran'))

        total_duration = exam.total_duration.total_seconds()

        difference = get_time_difference(date_1=date_1, date_2=date_2)

        time_left = int(total_duration - difference)

        return render(request=request, template_name=self.template_name)
