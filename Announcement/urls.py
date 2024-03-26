from django.urls import path
from Announcement import views

app_name = "announcement"

urlpatterns = [
    path("messages", views.AnnouncementListView.as_view(), name="messages"),

]
