from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.encoding import uri_to_iri
from django.views.generic import ListView, DetailView, View

from Account.mixins import AuthenticatedUsersOnlyMixin
from Course.mixins import CanUserEnterExamMixin
from Course.models import VideoCourse, Exam, ExamSection, ExamAnswer
from Home.mixins import URLStorageMixin
from Home.models import Banner4, Banner5


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

        sections = ExamAnswer.objects.filter(exam=self.object)
        section_names = list(set(sections.values_list('section__name', flat=True)))

        banner_4 = Banner4.objects.filter(can_be_shown=True).last()  # Returns a single object
        banner_5 = Banner5.objects.filter(can_be_shown=True).last()  # Returns a single object
        is_user_registered = Exam.objects.filter(participated_users=user, slug=self.object.slug).exists()

        context['banner_4'] = banner_4
        context['banner_5'] = banner_5
        context['is_user_registered'] = is_user_registered
        context['sections_names'] = section_names

        return context


class EnterExam(AuthenticatedUsersOnlyMixin, CanUserEnterExamMixin, View):
    def get(self, request, *args, **kwargs):
        pass


class RegisterExam(AuthenticatedUsersOnlyMixin, View):
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
