from django.contrib import admin

from Course.models import VideoCourse, VideoCourseObject, Category


class VideoCourseObjectTabularInline(admin.StackedInline):
    model = VideoCourseObject
    extra = 1


@admin.register(VideoCourse)
class VideoCourseAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', 'description', 'teacher')
    autocomplete_fields = ('teacher',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = [VideoCourseObjectTabularInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)