from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from ExamAce import settings

urlpatterns = ([
                   path('admin/', admin.site.urls),
                   path("ckeditor5/", include('django_ckeditor_5.urls'), name="ck_editor_5_upload_file"),
                   path("__debug__/", include("debug_toolbar.urls")),
                   path('ratings/', include('star_ratings.urls', namespace='ratings')),
                   path('', include('Home.urls')),
                   path('account/', include('Account.urls')),
                   path('course/', include('Course.urls')),
                   path('news/', include('News.urls')),
                   path('weblog/', include('Weblog.urls')),
                   path('us/', include('Us.urls')),
               ]
               + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
