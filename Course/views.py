from django.shortcuts import get_object_or_404
from django.utils.encoding import uri_to_iri
from django.views.generic import ListView, DetailView

from Course.models import VideoCourse, Exam


class AllVideoCourses(ListView):
    model = VideoCourse
    context_object_name = 'courses'
    template_name = 'Course/all_video_courses.html'

    def get_queryset(self):
        video_courses = VideoCourse.objects.select_related('category', 'teacher').order_by('-created_at')

        return video_courses


class VideoCourseDetail(DetailView):
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


class AllBookCourses(ListView):
    pass


class AllExams(ListView):
    model = Exam
    context_object_name = 'exams'
    template_name = 'Course/all_exams.html'

    def get_queryset(self):
        exams = Exam.objects.select_related('category', 'designer').order_by('-created_at')

        return exams


class ExamDetail(DetailView):
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
