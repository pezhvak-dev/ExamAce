from django.urls import path

from Course import views

app_name = 'course'

urlpatterns = [
    path('videos', views.AllVideoCourses.as_view(), name='all_video_courses'),
    path('exam/register/', views.RegisterInExam.as_view(), name='register_exam'),
    path('exams', views.AllExams.as_view(), name='all_exams'),
    path('exams/category/<slug>', views.ExamsByCategory.as_view(), name='exams_by_category'),
    path('video/<slug>', views.VideoCourseDetail.as_view(), name='video_course_detail'),
    path('videos/category/<slug>', views.VideoCourseByCategory.as_view(), name='videos_by_category'),
    path('exam/<slug>/question/download', views.ExamQuestionDownload.as_view(), name='download_questions'),
    path('exam/<slug>/answer/download', views.ExamAnswerDownload.as_view(), name='download_answers'),
    path('exam/<slug>/enter', views.EnterExam.as_view(), name='enter_exam'),
    path('exam/<slug>', views.ExamDetail.as_view(), name='exam_detail'),
    path('books', views.AllBookCourses.as_view(), name='all_book_courses'),
    path('exam/<slug>/calculate/result', views.CalculateExamResult.as_view(), name='calculate_exam_result'),
    path('exams/filter', views.ExamFilterView.as_view(), name='filter_exams'),
    path('exam/favorite/toggle/', views.ToggleFavorite.as_view(), name='toggle_favorite'),
    path('exam/<slug>/submit/temp/', views.TempExamSubmit.as_view(),name='submit_pdf_exam_temp_answer'),
    path('report_card/<int:exam_id>/', views.ReportCardView.as_view(), name='report_card'),

]
