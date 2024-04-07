from django.urls import path

from Weblog import views

app_name = 'weblog'

urlpatterns = [
    path('list', views.AllWeblogs.as_view(), name='all'),
    path('detail/<slug>', views.WeblogDetail.as_view(), name='detail'),
    path('category/<slug>', views.WeblogsByCategory.as_view(), name='by_category'),
    path('add/comment/<slug>', views.AddComment.as_view(), name='add_comment'),
    path('like/comment/<slug>', views.AddComment.as_view(), name='like_comment'),
]
