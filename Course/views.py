from django.views.generic import ListView

from Course.models import VideoCourse


class AllVideoCourses(ListView):
    model = VideoCourse
    context_object_name = 'courses'
    template_name = 'Course/all_courses.html'
