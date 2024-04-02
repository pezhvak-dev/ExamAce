from django.contrib import admin

from Course.models import VideoCourse, VideoCourseObject, Category, VideoSeason, Exam


@admin.register(VideoCourseObject)
class VideoCourseObjectAdmin(admin.ModelAdmin):
    list_display = ("title",)


@admin.register(VideoCourse)
class VideoCourseAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'category', 'description',
        'status', 'type', 'price', 'has_discount',
        'discount_percentage', 'price_after_discount'
    )

    search_fields = ('name', 'description', 'teacher')

    autocomplete_fields = ('teacher',)

    prepopulated_fields = {'slug': ('name',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(VideoSeason)
class VideoSeasonAdmin(admin.ModelAdmin):
    list_display = ('course', 'number')
    list_filter = ('course',)
    search_fields = ('course__name',)


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'category', 'description',
        'type', 'price', 'has_discount',
        'discount_percentage', 'price_after_discount'
    )
