from django.urls import path

from Course import views

app_name = 'course'

urlpatterns = [
    path('videos', views.AllVideoCourses.as_view(), name='all_video_courses'),
    path('exams', views.AllExams.as_view(), name='all_exams'),
    path('video/<slug>', views.VideoCourseDetail.as_view(), name='video_course_detail'),
    path('exam/<slug>/question/download', views.ExamQuestionDownload.as_view(), name='download_questions'),
    path('exam/<slug>/enter', views.EnterExam.as_view(), name='enter_exam'),
    path('exam/<slug>/register', views.RegisterExam.as_view(), name='register_exam'),
    path('exam/<slug>', views.ExamDetail.as_view(), name='exam_detail'),
    path('books', views.AllBookCourses.as_view(), name='all_book_courses'),
    path('exam/<slug>/submit/final', views.FinalExamSubmit.as_view(), name='final_exam_submit'),
    path('exam/<slug>/submit/temp', views.TempExamSubmit.as_view(), name='temp_exam_submit'),
    path('exam/<slug>/calculate/result', views.CalculateExamResult.as_view(), name='calculate_exam_result'),
]
