from django.db import models
from django_jalali.db.models import jDateTimeField

from Home.variables import Numbers as HomeMaxAndMinLengthStrings
from Home.variables import MediaPaths as HomeModelMediaPath
from Home.variables import Strings as HomeModelVerboseNameStrings


class HeroBanner(models.Model):
    title = models.CharField(max_length=HomeMaxAndMinLengthStrings.title_max,
                             verbose_name=HomeModelVerboseNameStrings.title,
                             help_text=HomeModelVerboseNameStrings.needed)

    link = models.URLField(blank=True, null=True, verbose_name=HomeModelVerboseNameStrings.link, unique=True)

    file = models.FileField(upload_to=HomeModelMediaPath.hero_banner_files,
                            verbose_name=HomeModelVerboseNameStrings.file,
                            help_text=HomeModelVerboseNameStrings.needed)

    can_be_shown = models.BooleanField(default=True, verbose_name=HomeModelVerboseNameStrings.can_be_shown)

    created_at = jDateTimeField(auto_now_add=True, verbose_name=HomeModelVerboseNameStrings.created_at,
                                help_text=HomeModelVerboseNameStrings.needed)

    updated_at = jDateTimeField(auto_now=True, verbose_name=HomeModelVerboseNameStrings.updated_at)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = HomeModelVerboseNameStrings.hero_banner
        verbose_name_plural = HomeModelVerboseNameStrings.hero_banners
        ordering = ('-created_at',)
