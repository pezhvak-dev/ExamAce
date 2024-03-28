from django.urls import path

from Course import views

app_name = 'course'

urlpatterns = [
    path('', views.AllVideoCourses.as_view(), name='all_video_courses')
]
