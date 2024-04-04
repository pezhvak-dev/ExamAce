from django.urls import path

from Course import views

app_name = 'course'

urlpatterns = [
    path('videos', views.AllVideoCourses.as_view(), name='all_video_courses'),
    path('exams', views.AllExams.as_view(), name='all_exams'),
    path('video/<slug>', views.VideoCourseDetail.as_view(), name='video_course_detail'),
    path('exam/<slug>', views.ExamDetail.as_view(), name='exam_detail'),
    path('books', views.AllBookCourses.as_view(), name='all_book_courses'),
]
