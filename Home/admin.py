from django.contrib import admin

from Home.models import (HeroBanner, Banner1, Banner2, Banner3, Banner4, Banner5)


@admin.register(HeroBanner)
class HeroBannerAdmin(admin.ModelAdmin):
    list_display = ("title", "link", "can_be_shown")

    list_editable = ("can_be_shown",)


@admin.register(Banner1)
class Banner1Admin(admin.ModelAdmin):
    list_display = ("title", "link", "can_be_shown")

    list_editable = ("can_be_shown",)


@admin.register(Banner2)
class Banner1Admin(admin.ModelAdmin):
    list_display = ("title", "link", "can_be_shown")

    list_editable = ("can_be_shown",)


@admin.register(Banner3)
class Banner1Admin(admin.ModelAdmin):
    list_display = ("title", "link", "can_be_shown")

    list_editable = ("can_be_shown",)


@admin.register(Banner4)
class Banner1Admin(admin.ModelAdmin):
    list_display = ("title", "link", "can_be_shown")

    list_editable = ("can_be_shown",)


@admin.register(Banner5)
class Banner1Admin(admin.ModelAdmin):
    list_display = ("title", "link", "can_be_shown")

    list_editable = ("can_be_shown",)
