from django.contrib import admin
from nested_inline.admin import NestedStackedInline, NestedModelAdmin

from Course.models import VideoCourse, VideoCourseObject, Category, VideoSeason, Exam, ExamAnswer, ExamSection, \
    DownloadedQuestionFile, EnteredExamUser, UserFinalAnswer, UserTempAnswer, ExamUnit


class UserFinalAnswerInline(admin.StackedInline):
    model = UserFinalAnswer
    extra = 1


class UserTempAnswerInline(admin.StackedInline):
    model = UserTempAnswer
    extra = 1


class DownloadedQuestionFileInline(admin.StackedInline):
    model = DownloadedQuestionFile
    extra = 1


class EnteredExamUserInline(admin.StackedInline):
    model = EnteredExamUser
    extra = 1


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


class ExamAnswerInline(NestedStackedInline):
    model = ExamAnswer
    extra = 1


class ExamUnitInline(NestedStackedInline):
    model = ExamUnit
    extra = 1
    inlines = [ExamAnswerInline]


class ExamSectionInline(NestedStackedInline):
    model = ExamSection
    extra = 1
    inlines = [ExamUnitInline]


class ExamAdmin(NestedModelAdmin):
    model = Exam
    list_display = (
        'name', 'total_duration', 'category', 'type', 'level',
        'price', 'has_discount', 'discount_percentage', 'price_after_discount'
    )

    prepopulated_fields = {'slug': ('name',)}

    inlines = [ExamSectionInline]

    def save_model(self, request, obj, form, change):
        if not obj.designer_id:
            obj.designer = request.user

        super().save_model(request, obj, form, change)


admin.site.register(Exam, ExamAdmin)