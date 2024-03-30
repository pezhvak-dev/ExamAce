from django.urls import path

from News import views

app_name = 'news'

urlpatterns = [
    path('list', views.AllNews.as_view(), name='all'),
    path('detail/<slug>', views.NewDetail.as_view(), name='detail')
]