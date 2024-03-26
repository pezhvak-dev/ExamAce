from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from ExamAce import settings

urlpatterns = ([
                   path('admin/', admin.site.urls),
                   path("ckeditor5/", include('django_ckeditor_5.urls'), name="ck_editor_5_upload_file"),
                   path('', include('Home.urls')),
                   path('account/', include('Account.urls')),
                   path('announcement/', include('Announcement.urls')),
               ]
               + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
