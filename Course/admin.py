from django.contrib import admin

from Course.models import VideoCourse, VideoCourseObject, Category, VideoSeason, Exam, ExamUnit, Answer, ExamSection


@admin.register(VideoCourseObject)
class VideoCourseObjectAdmin(admin.ModelAdmin):
    list_display = ("title",)


@admin.register(VideoCourse)
class VideoCourseAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'category',
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


@admin.register(ExamUnit)
class ExamUnitAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {'slug': ('name',)}


class AnswerInline(admin.StackedInline):
    model = Answer
    extra = 1


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'total_duration', 'type', 'price', 'has_discount',
        'discount_percentage', 'price_after_discount'
    )

    prepopulated_fields = {'slug': ('name',)}

    inlines = [AnswerInline]

    def save_model(self, request, obj, form, change):
        if not obj.designer_id:
            obj.designer = request.user
        super().save_model(request, obj, form, change)


@admin.register(ExamSection)
class ExamSectionAdmin(admin.ModelAdmin):
    list_display = ("name",)
