from django.urls import path

from Us import views

app_name = 'us'

urlpatterns = [
    path('about', views.About.as_view(), name='about')
]